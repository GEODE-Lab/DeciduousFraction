from geosoup import *
from geosoupML import *

import os
import numpy as np
import multiprocessing
from sys import argv
import sys
import time


"""
This script fits training data to RF models and validates them using the validation data.
The RF models are pickled. The outputs of all models are stored as 
R2, rmse, slope, and intercept values in an output text file as 
list of dictionaries.
"""


def fit_regressor(args):

    """
    Method to train and validate classification models

    :param args: Tuple of args represents the following in the given order:

    (name: Name of the model,
    train_samp: Samples object for training the classifier,
    val_samp: Samples object for validating the classifier,
    param: parameter dictionary)

    :returns: tuple (r-squared*100, rmse, slope, intercept, model_name)
    """

    name, train_samp, valid_samp, param = args

    # initialize RF classifier
    model = RFRegressor(**param)
    model.time_it = True

    # fit RF classifier using training data
    model.fit_data(train_samp.format_data())

    # predict using held out samples and print to file
    pred = model.sample_predictions(valid_samp.format_data(),
                                    regress_limit=[0.0, 1.0])

    res = {'name': name,
           'rsq': pred['rsq'] * 100.0,
           'slope': pred['slope'],
           'intercept': pred['intercept'],
           'rmse': pred['rmse']}

    res.update(param)
    return res


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
    result = list()

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
                result.append("{v} {n}".format(v=value,
                                               n=name))
        else:
            value = "{:.{p}f}".format(seconds,
                                      p=precision)
            result.append("{v} {n}".format(v=value,
                                           n=name))

    # join output
    return ' '.join(result)


# main program
if __name__ == '__main__':

    # script, samp_file, param_file, out_dir, n_iterations, array_id = argv
    samp_file = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/" + \
                    "gee_data_clean_v13.csv"
                # "gee_data_clean_1998_2012_L57_short_v11.csv"
    param_file = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/" + \
                 "rf_param_v7.csv"
    out_dir = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_test"
    n_iterations = 500
    array_id = 21832  # 21832, 21833, 21813, 21835, 21715, 21912, 23945, 21780, 21846
    version = 5

    n_proc = 6

    t = time.time()
    sep = Handler().sep

    out_file = out_dir + sep + 'RF_param_test_' + str(array_id) + '_' + str(version) + '.csv'

    Opt.cprint(out_file)

    label_colname = 'decid_frac'

    sample_partition = 70
    display = 10

    cpus = multiprocessing.cpu_count()

    if n_proc <= 0:
        pool = multiprocessing.Pool(processes=1)
        n_proc = 1
    elif n_proc >= cpus:
        pool = multiprocessing.Pool(processes=cpus)
        n_proc = cpus
    else:
        pool = multiprocessing.Pool(processes=n_proc)

    print('Number of CPUs used: {}'.format(str(n_proc)))

    # prepare training samples
    samp = Samples(csv_file=samp_file,
                   label_colname=label_colname)

    param_dicts = Handler(param_file).read_from_csv(return_dicts=True)
    param = param_dicts[int(array_id)-1]

    print(param)

    samp_list = list()

    Opt.cprint('Randomizing samples...')

    for i in range(0, int(n_iterations)):

        model_name = 'RF_param_{}_{}'.format(array_id,
                                             str(i+1))

        trn_samp, val_samp = samp.random_partition(sample_partition)

        samp_list.append([model_name,
                          trn_samp,
                          val_samp,
                          param])

    Opt.cprint('Number of elements in sample list : {}'.format(str(len(samp_list))))

    results = pool.map(fit_regressor,
                       samp_list)

    Opt.cprint('Top {} models:'.format(str(display)))
    Opt.cprint('')
    Opt.cprint('R-sq, Model name')

    out_list = list()
    if len(results) > 0:
        results.sort(reverse=True, key=lambda elem: elem['rsq'])

        for result in results[0: (display-1)]:
            Opt.cprint(result)

    if len(results) > 0:
        Handler.write_to_csv(results,
                             out_file)
    else:
        Opt.cprint('No results to summarize!')

    print('Time taken: {}'.format(display_time(time.time() - t)))
