from geosoup import *
import multiprocessing


def compile_test_res(filename):
    print(filename)
    return Handler(filename).read_from_csv(return_dicts=True)


if __name__ == '__main__':
    result_dir = "/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v13"
    out_file = "/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v13_compilation.csv"

    file_list = Handler(dirname=result_dir).find_all(pattern='.csv')

    cpus = multiprocessing.cpu_count()
    n_proc = 4

    if n_proc <= 0:
        pool = multiprocessing.Pool(processes=1)
        n_proc = 1
    elif n_proc >= cpus:
        pool = multiprocessing.Pool(processes=cpus)
        n_proc = cpus
    else:
        pool = multiprocessing.Pool(processes=n_proc)

    print('Number of CPUs used: {}'.format(str(n_proc)))
    print('Number of files: {}'.format(len(file_list)))

    res = pool.map(compile_test_res,
                   file_list)
    flat_res = list(elem for sublist in res for elem in sublist)

    res_sorted = sorted(flat_res, reverse=True, key=lambda x: x['rsq'])

    print('Top 100:')
    print(res_sorted[:100])

    Handler.write_to_csv(res_sorted,
                         outfile=out_file)

    print('Written file {}'.format(out_file))
