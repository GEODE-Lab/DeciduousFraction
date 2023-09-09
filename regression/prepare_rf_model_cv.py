from geosoup import Handler, Opt, Sublist
from geosoupML import RFRegressor, Samples
import multiprocessing
from sys import argv
import sys
import time

"""
This script initializes and fits training data to prepare models.
The data is pre prepared using analysis_initiate.py. The RF models are then
pickled and saved for later use. In addition this script also generates outputs
by classifying held-out samples using the RF model.
"""

# global param
rsq_limit = 60.0
clip = 0.01
n_folds = 5
method = 'mean'
over_adjust = 1.01


def fit_regressor(args):
    """
    Method to train and validate classification models
    and if the R-squared is > 0.5 then store the model and its
    properties in a pickled file and csv file respectively

    :param args: List of list of args represents the following in the given order:

    (name: Name of the model,
    train_samp: Samples object for training the classifier,
    val_samp: Samples object for validating the classifier,
    infile: input file containing the samples
    pickle_dir: folder to store the pickled classifier in)

    :returns: tuple (r-squared*100 , model_name)
    """
    sep = Handler().sep

    name, cut_samp, in_file, pickle_dir, llim, ulim, param = args

    regress_limit = [llim + clip * (ulim - llim),
                     ulim - clip * (ulim - llim)]

    samp_folds = cut_samp.make_folds(n_folds)

    model_list = list()

    for train_samp, valid_samp in samp_folds:
        # initialize RF classifier
        model = RFRegressor(**param)
        model.time_it = True

        # fit RF classifier using training data
        model.fit_data(train_samp.format_data())
        model.vdata = valid_samp.format_data()

        model.get_adjustment_param(clip=clip,
                                   data_limits=[llim, ulim],
                                   over_adjust=over_adjust)

        # predict using held out samples and print to file
        pred = model.sample_predictions(valid_samp.format_data(),
                                        regress_limit=regress_limit,
                                        output_type=method)

        out_dict = dict()
        out_dict['name'] = Handler(in_file).basename.split('.')[0] + name
        out_dict['rsq'] = pred['rsq'] * 100.0
        out_dict['slope'] = pred['slope']
        out_dict['intercept'] = pred['intercept']
        out_dict['rmse'] = pred['rmse']
        out_dict['criteria'] = 'non_match'

        model.output = out_dict

        model_list.append(model)

    rsq_list = list(model.output['rsq'] for model in model_list)

    best_fold_model = model_list[0]
    for model in model_list:
        if model.output['rsq'] == Sublist(rsq_list).max():
            best_fold_model = model

    best_fold_model.all_cv_results = list(model.output for model in model_list)
    best_fold_model.output['fold_sd'] = Sublist.std_dev(list(model.output['rsq'] for model in model_list))

    Opt.cprint(best_fold_model.output)

    if Sublist(rsq_list).median() >= rsq_limit:
        best_fold_model.output['criteria'] = 'match'

        best_fold_model.get_training_fit()

        best_fold_model.output['regress_low_limit'] = regress_limit[0]
        best_fold_model.output['regress_up_limit'] = regress_limit[1]

        best_fold_model.output['var_importance'] = ';'.join(list('{}:{}'.format(elem[0], str(elem[1]))
                                                                 for elem in best_fold_model.var_importance()))

        # file to write the model run output to
        outfile = pickle_dir + sep + Handler(in_file).basename.split('.')[0] + name + '.txt'
        outfile = Handler(filename=outfile).file_remove_check()

        # save RF classifier using pickle
        picklefile = pickle_dir + sep + Handler(in_file).basename.split('.')[0] + name + '.pickle'
        picklefile = Handler(filename=picklefile).file_remove_check()

        best_fold_model.pickle_it(picklefile)

    return best_fold_model.output


def find_best_model(results_array,
                    n_elem=None):
    """
    Method to find the best model
    :param results_array: array of results
    :param n_elem: Number of best results to return
    :return:
    """

    sd_wt = 5.0
    rsq_wt = 1.0
    if n_elem is None:
        n_elem = len(results_array)

    res = zip(list(result_['fold_sd'] * sd_wt for result_ in results_array),
              list(result_['rsq'] * rsq_wt for result_ in results_array))

    res_ = list(elem[1] - elem[0] for elem in res)

    _sorted_res = list(reversed(list(ii[0] for ii in sorted(enumerate(res_),
                                                            key=lambda x: x[1]))))

    return list(results_array[ii] for ii in _sorted_res[0: n_elem])


def display_time(seconds,
                 precision=1):
    """
    method to display time in human readable format
    :param seconds: Number of seconds
    :param precision: Decimal precision
    :return: String
    """

    # define denominations
    intervals = [('weeks', 604800),
                 ('days', 86400),
                 ('hours', 3600),
                 ('minutes', 60),
                 ('seconds', 1)]

    # initialize list
    _result = list()

    # coerce to float
    dtype = type(seconds).__name__
    if dtype != 'int' or dtype != 'long' or dtype != 'float':
        try:
            seconds = float(seconds)
        except (TypeError, ValueError, NameError):
            sys.stdout.write("Type not coercible to Float")

    # break denominations
    for name, count in intervals:
        if name != 'seconds':
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                value = str(int(value))
                _result.append("{v} {n}".format(v=value,
                                                n=name))
        else:
            value = "{:.{p}f}".format(seconds,
                                      p=precision)
            _result.append("{v} {n}".format(v=value,
                                            n=name))

    # join output
    return ' '.join(_result)


# main program
if __name__ == '__main__':
    '''
    script, infile, pickledir, codename, n_iterations, cpus = argv
    '''

    pickledir = "D:/temp/decid/"
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
             "gee_extract_6_17_2020_formatted_md_only_data.csv"
    codename = "v32_median1_2"

    n_iterations = 10
    n_iterations = int(n_iterations)
    cpus = 3  # multiprocessing.cpu_count() - 2

    param = {"samp_split": 10, "max_feat": 27, "trees": 1000, "samp_leaf": 10}
    # param = {"samp_split": 10, "max_feat": 16, "trees": 500, "samp_leaf": 10}
    # param = {"samp_split": 10, "max_feat": 15, "trees": 400, "samp_leaf": 5}
    # param = {"samp_split": 9, "max_feat": 17, "trees": 200, "samp_leaf": 2}

    min_decid = 0.0
    max_decid = 1.0

    label_colname = 'decid_frac'
    model_initials = 'RF'

    bootstrap_partition = 95
    display = 20

    t = time.time()

    Handler(dirname=pickledir).dir_create()

    Opt.cprint(infile)
    Opt.cprint(pickledir)
    Opt.cprint(codename)

    sep = Handler().sep

    cpus = int(cpus)

    print('Number of CPUs: {}'.format(str(cpus)))

    Handler(dirname=pickledir).dir_create()

    # prepare training samples
    samp = Samples(csv_file=infile, label_colname=label_colname)

    print(samp)

    samp_list = list()

    Opt.cprint('Randomizing samples...')

    counter = 0
    perc = 0
    for i in range(0, n_iterations):

        model_name = '_{}_{}'.format(model_initials,
                                     str(i + 1))

        reduced_samp, _ = samp.random_partition(bootstrap_partition)
        samp_list.append([model_name,
                          reduced_samp,
                          infile,
                          pickledir,
                          min_decid,
                          max_decid,
                          param])

        counter += 1

        if counter > int((float(perc) / 100.0) * float(n_iterations)):
            sys.stdout.write('{}..'.format(str(perc)))
            sys.stdout.flush()
            perc += 10
    sys.stdout.write('100!\n')

    Opt.cprint('Number of elements in sample list : {}'.format(str(len(samp_list))))

    pool = multiprocessing.Pool(processes=cpus)

    results = pool.map(fit_regressor,
                       samp_list)

    Opt.cprint('Results:----------------------------------')

    Opt.cprint('\nLength of results: {}\n'.format(len(results)))

    if len(results) > 0:
        for result in results:
            Opt.cprint(result)
        Opt.cprint('------------------------------------------')
        Opt.cprint('\nTop {} models:'.format(str(display)))
        Opt.cprint('')
        Opt.cprint('R-sq, Model name')

        results = list(result_ for result_ in results
                       if result_['criteria'] == 'match')

        out_list_ = find_best_model(results,
                                    n_elem=display)

        for output in out_list_:
            Opt.cprint(output)

        sep = Handler().sep

        Opt.cprint('------------------------------------------')

        summary_file = pickledir + 'results_summary_' + codename + '.csv'
        Opt.cprint('\nSummary file: {}\n'.format(summary_file))

        if len(results) > 0:
            Handler.write_to_csv(results,
                                 outfile=summary_file,
                                 delimiter=',')
        else:
            Opt.cprint("No results in the specified range of rsq > {}!".format(str(rsq_limit)))

    else:
        Opt.cprint('\nNo results to summarize!\n')

    print('Time taken: {}'.format(display_time(time.time() - t)))
