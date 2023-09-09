"""
This script initializes and fits training data to prepare models.
The data is pre prepared using analysis_initiate.py. The RF models are then
pickled and saved for later use if they meet a certain criteria (Rsq > 0.60).
In addition this script also generates outputs by classifying held-out samples 
using the RF model. This script is run in parallel using MPI libraries. 
"""

if __name__ == '__main__':
    import sys
    import os

    module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(module_path)
    from modules import *
    from modules.classification import _Regressor
    from mpi4py import MPI

    script, infile, pickledir, codename, n_iterations = sys.argv

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    min_decid = 0
    max_decid = 10000

    label_colname = 'DECID_FRAC'
    model_initials = 'RF'
    sample_partition = 70
    n_iterations = int(n_iterations)
    display = 10
    param = {"samp_split": 10, "max_feat": 19, "trees": 500, "samp_leaf": 1}

    if rank == 0:

        Opt.cprint('Number of CPUs : {} '.format(str(size)))

        Handler(dirname=pickledir).dir_create()

        # prepare training samples
        samp = Samples(csv_file=infile, label_colname=label_colname)

        # limit int values to 16 bit
        corr_samp = list()
        for elem in samp.x:
            corr_elem = list()
            for number in elem:
                if number < -32767:
                    number = -32767
                elif number > 32767:
                    number = 32767

                corr_elem.append(number)
            corr_samp.append(corr_elem)

        samp.x = corr_samp

        samp_list = list()

        Opt.cprint('Randomizing samples...')

        for i in range(0, n_iterations):
            model_name = '_{}_{}'.format(model_initials,
                                         str(i + 1))

            trn_samp, val_samp = samp.random_partition(sample_partition)

            samp_list.append([model_name,
                              trn_samp,
                              val_samp,
                              infile,
                              pickledir,
                              min_decid,
                              max_decid,
                              param])

        Opt.cprint('Number of elements in sample list : {}'.format(str(len(samp_list))))

        sample_chunks = [samp_list[i::size] for i in range(size)]

        chunk_length = list(str(len(chunk)) for chunk in sample_chunks)

        Opt.cprint(' Distribution of chunks : {}'.format(', '.join(chunk_length)))

    else:
        sample_chunks = None

    try:
        samples = comm.scatter(sample_chunks,
                               root=0)
    except OverflowError:
        Opt.cprint('Overflow error while scattering samples at rank {}'.format(rank))
        samples = None

    result = _Regressor.fit_regressor(samples, rank)

    result_array = comm.gather(result,
                               root=0)

    if rank == 0:

        results = [item for sublist in result_array for item in sublist if item is not None]

        if len(results) > 0:

            Opt.cprint('Results:----------------------------------')
            for result in results:
                Opt.cprint(result)
            Opt.cprint('------------------------------------------')
            Opt.cprint('\nLength of results: {}\n'.format(len(results)))

            sep = Handler().sep

            Opt.cprint('Top {} models:'.format(str(display)))
            Opt.cprint('')
            Opt.cprint('R-sq, Model name')

            out_list = sorted(results,
                              key=lambda elem: elem['rsq'],
                              reverse=True)

            for output in out_list[0: (display - 1)]:
                Opt.cprint(output)

            summary_file = pickledir + sep + 'results_summary_' + codename + '.csv'
            Opt.cprint('\nSummary file: {}\n'.format(summary_file))

            Handler.write_to_csv(out_list,
                                 outfile=summary_file,
                                 delimiter=',')

        else:
            Opt.cprint('\nNo results to summarize!\n')
