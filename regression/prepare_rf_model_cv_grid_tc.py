from geosoup import Handler, Opt
from geosoupML import RFRegressor, Samples
import multiprocessing as mp
import numpy as np
from sys import argv

"""
This script initializes and fits training data to random forest regressors 
to find the optimum set of parameters. The data is used from a pre-pared csv file.
The number of folds used is 5 by default.
"""


def fit_regressor(parameter_dict,
                  iterations=3,
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
                                               output_type='median',
                                               n_folds=n_folds))
        param_copy = dict([(k, parameter_dict[k]) for k in parameter_dict.keys() if k != 'samples'])
        cv_out_list[indx].update(param_copy)

    return cv_out_list


def fit_regressor_mean(parameter_dict,
                       iterations=3,
                       n_folds=5):
    """
    Method to find the best model
    :param parameter_dict:
    :param iterations: Number of repetitions for averaging the final results
    :param n_folds: Number of folds to evaluate the model on
    :return: dictionary
    """

    reg = RFRegressor
    cv_list = [{} for _ in range(iterations)]

    for indx in range(iterations):
        cv_list[indx].update(reg.cv_result(reg,
                                           parameter_dict['samples'],
                                           parameter_dict,
                                           output_type='mean',
                                           n_folds=n_folds))
        param_copy = dict([(k, parameter_dict[k]) for k in parameter_dict.keys() if k != 'samples'])
        cv_list[indx].update(param_copy)

    return {key: np.mean([cv_dict[key] for cv_dict in cv_list]) for key in cv_list[0].keys()}


def make_param_list(samp_file, labelname):
    """
    Method to yield a paramter dictionary for RF Regressor
    :param samp_file: Sample csv file
    :param labelname: Name of label in tthe samples csv file
    :yields: Dictionary
    """

    samples = Samples(samp_file,
                      label_colname=labelname)

    param_dict_list = RFRegressor.param_grid(param_grid_dict)

    for param_dict in param_dict_list:
        param_dict.update({'samples': samples})
        yield param_dict


# main program
if __name__ == '__main__':
    
    script, infile, outfile, label_colname, ncpus = argv
                       
    param_grid_dict = {"min_samples_split": [2, 4, 8, 12, 16, 20],
                       "max_features": [2, 4, 8, 12, 16, 20, 24, 28, 32, 36],
                       "n_estimators": [200, 400, 800, 1200, 1600, 2000],
                       "min_samples_leaf": [1, 2, 4, 8, 12],
                       "max_depth": [12,16,20,24,30]}

    samp = Samples(infile, label_colname=label_colname)

    Opt.cprint(samp)
    Opt.cprint(samp.x_name)

    Opt.cprint('\n')

    for param, param_vals in param_grid_dict.items():
        Opt.cprint(str(param) + ' : ' + str(param_vals))

    n_runs = np.product([len(elem_list) for _, elem_list in param_grid_dict.items()])
    Opt.cprint('Number of runs: {}'.format(str(n_runs)))

    Opt.cprint('\n========= RESULTS ==========\n')

    pool = mp.Pool(int(ncpus) - 1)
    first = True
    for result in pool.imap_unordered(fit_regressor_mean,
                                      make_param_list(infile, label_colname)):
        Opt.cprint(result)
        if first:
            first = False
            Handler.write_to_csv(result, outfile=outfile, append=False)
        else:
            Handler.write_to_csv(result, outfile=outfile, append=True)

    pool.close()
    pool.join()

    exit(0)
