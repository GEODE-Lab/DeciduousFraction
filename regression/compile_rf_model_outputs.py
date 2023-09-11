"""
This code compiles all the outputs from saved (pickled) RF models
applied on held out (25%) samples. The compiled outputs are used to 
generate a scaling factor tau (t). Tau is used for scaling standard 
deviation of tree outputs of a selected RF model to per-pixel uncertainty. 
"""

import sys
import os
from geosoup import *
from geosoupML import *
import numpy as np

if __name__ == '__main__':


    # import file names from commandline args
    # script, y_files_dir, var_y_file, y_hat_bar_file, y_obs_file = argv
    script, y_files_dir, tau_outfile = sys.argv

    print('Searching in {} ...'.format(y_files_dir))
    print('')

    # find all y value files
    filenames = Handler(dirname=y_files_dir).find_all('.csv')

    # number of files
    n = Sublist.list_size(filenames)

    print('{} Files found'.format(n))
    print('')

    # initialize arrays
    # var_y = np.array((n, 2000), dtype=float) - 99.0
    # y_hat_bar = np.zeros((n, 2000), dtype=float) - 99.0
    # y = np.zeros((n, 2000), dtype=float) - 99.0
    # tau = np.zeros((n, 2000), dtype=float) - 99.0
    tau_hat = np.zeros(n, dtype=float)

    # read data
    for i in range(0, n):
        print('Processing file ' + str(i+1) + ': ' + filenames[i])

        # read file as dictionary
        temp_dict = read_y_param_from_summary(filenames[i])

        # number of samples
        n_temp_samp = Sublist.list_size(temp_dict['obs_y'])

        # assign samples to array
        # y[0:n_temp_samp] = temp_dict['obs_y']
        # var_y[0:n_temp_samp] = temp_dict['var_y']
        # y_hat_bar[0:n_temp_samp] = temp_dict['mean_y']

        # calculate the 95 percentile tau value for each sample set
        tau_hat[i] = np.percentile(np.sqrt(((np.array(temp_dict['obs_y']) -
                                            np.array(temp_dict['mean_y']))*(np.array(temp_dict['obs_y']) -
                                           np.array(temp_dict['mean_y']))) / np.array(temp_dict['var_y'])),
                                   95, interpolation='nearest')

    # calculate the overall tau value
    tau = np.mean(tau_hat)
    print('')
    print('~~Calculation complete!~~')
    print('Tau value: ' + str(tau))

    # output list
    outlist = ['tau', str(tau)]

    # write to out file
    Handler(filename=tau_outfile).write_list_to_file(outlist)

    print('Done!')

