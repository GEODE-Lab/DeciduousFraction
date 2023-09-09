from geosoup import Handler, Opt, Vector
from geosoupML import RFRegressor, Samples
import multiprocessing as mp
from sys import argv

"""
This script initializes and fits training data to random forest regressors 
to find the optimum set of parameters. The data is used from a pre-pared csv file.
The number of folds used is 5 by default.
"""


def fit_regressor(parameter_dict,
                  iterations=1,
                  n_folds=5):
    """
    Method to find the best model
    :param parameter_dict:
    :param iterations: Number of repetitions for averaging the final results
    :param n_folds: Number of folds to evaluate the model on
    :return: dictionary
    """

    reg = RFRegressor
    cv_out_list = [{} for _ in range(iterations)]

    for indx in range(iterations):
        cv_out_list[indx].update(reg.cv_result(reg,
                                               parameter_dict['samples'],
                                               parameter_dict,
                                               n_folds=n_folds))
        param_copy = dict([(k, parameter_dict[k]) for k in parameter_dict.keys() if k != 'samples'])
        cv_out_list[indx].update(param_copy)

    return cv_out_list


def make_param_list(samp_file,
                    label_colname):
    """
    Method to yield a paramter dictionary for RF Regressor
    :param samp_file: Sample csv file
    :yields: Dictionary
    """

    samples = Samples(samp_file,
                      label_colname=label_colname)

    param_dict_list = RFRegressor.param_grid(param_grid_dict)

    for param_dict in param_dict_list:
        param_dict.update({'samples': samples})
        yield param_dict


# main program
if __name__ == '__main__':

    '''
    script, infile, outfile, label_colname, zone, ncpus = argv

    /scratch/rm885/gdrive/sync/decid/excel/samp/



    param_grid_dict = {"min_samples_split": list(range(2, 52, 2)),
                       "max_features": list(range(2, 32, 2)),
                       "n_estimators": list(range(100, 2100, 100)),
                       "min_samples_leaf": list(range(1, 56, 5))}

    param_grid_dict = {"min_samples_split": list(range(2, 6, 2)),
                       "max_features": list(range(10, 20, 10)),
                       "n_estimators": list(range(800, 1600, 800)),
                       "min_samples_leaf": list(range(1, 2, 1))}


    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
             "gee_extract_6_17_2020_formatted_md_only_data.csv"    
    '''

    label_colname = 'tree_cover'
    codename = "east_canada_v1_test"
    pickledir = "D:/temp/tree_cover/"
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
             "hansen_tc_mosaic_2010_samp4_samp_tc_useful_east_canada.csv"
    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
             "hansen_tc_mosaic_2010_samp4_samp_tc_useful_{}.csv".format(codename)
    ncpus = 3

    param_grid_dict = {"min_samples_split": list(range(2, 8, 4)),
                       "max_features": list(range(2, 10, 4)),
                       "n_estimators": list(range(100, 500, 200)),
                       "min_samples_leaf": list(range(1, 12, 5))}

    samp = Samples(infile, label_colname=label_colname)

    print(samp)

    Opt.cprint('\n')

    for param, param_vals in param_grid_dict.items():
        Opt.cprint(str(param) + ' : ' + str(param_vals))

    Opt.cprint('\n========= RESULTS ==========\n')

    pool = mp.Pool(int(ncpus) - 1)
    first = True
    for result in pool.imap_unordered(fit_regressor,
                                      make_param_list(infile, label_colname)):
        Opt.cprint(result)
        if first:
            first = False
            Handler.write_to_csv(result, outfile=outfile, append=False, header=True)
        else:
            Handler.write_to_csv(result, outfile=outfile, append=True, header=False)

    pool.close()
    pool.join()

    exit(0)
