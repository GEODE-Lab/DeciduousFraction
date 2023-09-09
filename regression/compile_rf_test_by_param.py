from geosoup import *
from geosoupML import *
import sys
import os
import numpy as np


def get_rows(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            yield row
            count += 1


if __name__ == '__main__':

    param_file = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_param_v7.csv"
    csv_file = "C:/temp/rf_pickle_test_v13_compilation.csv"

    outfile = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_param_v7_results.csv"

    Opt.cprint('\nReading parameter file: {}\n'.format(param_file))
    param_list = Handler(param_file).read_from_csv(return_dicts=True)

    for elem in param_list:
        elem['rmse'] = list()
        elem['rsq'] = list()

    Opt.cprint('\nReading RF model outputs file: {}\n'.format(csv_file))
    rf_result_list = Handler(csv_file).read_from_csv(return_dicts=True)

    Opt.cprint('\nClassifying each result in RF file and obtaining median result - R-sq ...\n')

    header = list()
    for i, elem_dict in enumerate(rf_result_list):
        for param in param_list:
            if (param['samp_split'] == int(elem_dict['samp_split'])) and \
                    (param['max_feat'] == int(elem_dict['max_feat'])) and \
                    (param['trees'] == int(elem_dict['trees'])) and \
                    (param['samp_leaf'] == int(elem_dict['samp_leaf'])):

                param['rmse'].append(float(elem_dict['rmse']))
                param['rsq'].append(float(elem_dict['rsq']))

    #        Opt.cprint('Classifying {}'.format(str(i+1)))
    """
    for i, elem in enumerate(get_rows(csv_file)):
        if i == 0:
            header = elem
        else:
            elem_dict = dict(zip(header, elem))

            for param in param_list:
                if (param['samp_split'] == int(elem_dict['samp_split'])) and \
                        (param['max_feat'] == int(elem_dict['max_feat'])) and \
                        (param['trees'] == int(elem_dict['trees'])) and \
                        (param['samp_leaf'] == int(elem_dict['samp_leaf'])):

                    param['rmse'].append(float(elem_dict['rmse']))
                    param['rsq'].append(float(elem_dict['rsq']))

            Opt.cprint('Classifying {}'.format(str(i+1)))
    """

    for param in param_list:

        param['rmse'] = Sublist(param['rmse']).median()
        param['rsq'] = Sublist(param['rsq']).median()

        print(param)

    Opt.cprint('\nWriting parameter values to {}\n'.format(outfile))
    Handler(outfile).write_to_csv(param_list)




