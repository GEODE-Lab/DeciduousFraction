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
                                               output_type='median',
                                               adjust=False,
                                               n_folds=n_folds))
        param_copy = dict([(k, parameter_dict[k]) for k in parameter_dict.keys() if k != 'samples'])
        cv_out_list[indx].update(param_copy)

    return cv_out_list


def make_param_list(sampfile, labelcolname, params):
    """
    Method to yield a paramter dictionary for RF Regressor
    :param sampfile: Sample csv file
    :param labelcolname:
    :param params:
    :yields: Dictionary
    """

    samples = Samples(sampfile,
                      label_colname=labelcolname)

    param_dict_list = RFRegressor.param_grid(params)

    for param_dict in param_dict_list:
        param_dict.update({'samples': samples})
        yield param_dict


# main program
if __name__ == '__main__':

    # script, infile, outfile, label_colname, ncpus = argv
    infile = "D:/temp/albedo/albedo_decid_tc_samp_v2/training_samp_useful/" \
             "albedo_training_samples_sum.csv"
    outfile = "D:/temp/albedo/albedo_decid_tc_samp_v2/training_samp_useful/" \
              "albedo_training_samples_sum_cv_grid.csv"
    label_colname = 'albedo'
    ncpus = 1

    Opt.cprint('\n')

    param_grid_dict = {"min_samples_split": [2, 4, 8, 16, 32, 64, 128, 256, 512],
                       "max_features": [2],
                       "n_estimators": list(range(100, 2500, 400)),
                       "min_samples_leaf": list(range(10, 500, 20))}

    for param, param_vals in param_grid_dict.items():
        Opt.cprint(str(param) + ' : ' + str(param_vals))

    Opt.cprint('\n========= RESULTS ==========\n')

    samp = Samples(infile, label_colname=label_colname)

    print(samp)
    print(samp.x_name)

    hist_y = np.histogram(samp.y, bins=10)
    print(hist_y)
    #exit()

    # pool = mp.Pool(int(ncpus))
    first = True
    # for result in pool.imap_unordered(fit_regressor,
    #                                   make_param_list(infile, label_colname, param_grid_dict)):
    for params in make_param_list(infile, label_colname, param_grid_dict):
        print(params)
        result = fit_regressor(params)

        Opt.cprint(result)
        if first:
            first = False
            Handler.write_to_csv(result, outfile=outfile, append=False)
        else:
            Handler.write_to_csv(result, outfile=outfile, append=True)

    # pool.close()
    # pool.join()
    Opt.cprint('\n========= COMPLETED ==========\n')
