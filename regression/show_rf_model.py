from geosoup import *
from geosoupML import *
import sys
import os
import numpy as np

"""
This script is used to classify a raster using a selected RF model.
This script also generates the uncertainty raster.
"""

# main program
if __name__ == '__main__':

    # read in the input files
    # script, infile, outdir, rf_picklefile1, rf_picklefile2 = argv

    ulim = 1.0
    llim = 0.0

    regress_limit = [llim, ulim]

    output_type = 'median'

    working_dir = '/scratch/rm885/gdrive/sync/decid/RF_model_pickles/working/'

    outfile_train = working_dir + 'gee_data_cleaning_v28_median2_RF_106_training_samp.csv'
    outfile_valid = working_dir + 'gee_data_cleaning_v28_median2_RF_106_validation_samp.csv'

    rf_picklefile1 = working_dir + 'gee_data_cleaning_v28_median2_RF_106.pickle'
    #    'gee_data_cleaning_v28_median2_summer_RF_6478.pickle'

    # ------------------common parameters-----------------

    Opt.cprint('-----------------------------------------------------------------')

    Opt.cprint('Random Forest file 1: ' + rf_picklefile1)

    Opt.cprint('Outdir: ' + working_dir)
    Opt.cprint('-----------------------------------------------------------------')

    # load classifier from file
    regressor = RFRegressor.load_from_pickle(rf_picklefile1)

    data = regressor.data

    list_dicts = list()
    for i, elem in enumerate(data['features']):
        samp = dict()
        for j, elem_name in enumerate(data['feature_names']):
            samp[elem_name] = elem[j]
        samp[data['label_name']] = data['labels'][i]
        list_dicts.append(samp)

    vdata = regressor.vdata

    vlist_dicts = list()
    for i, elem in enumerate(vdata['features']):
        samp = dict()
        for j, elem_name in enumerate(vdata['feature_names']):
            samp[elem_name] = elem[j]
        samp[vdata['label_name']] = vdata['labels'][i]
        vlist_dicts.append(samp)

    all_data = dict()

    all_data['feature_names'] = data['feature_names']
    all_data['label_name'] = data['label_name']
    all_data['labels'] = list()
    all_data['features'] = list()

    for i, label in enumerate(data['labels']):
        all_data['labels'].append(label)
        all_data['features'].append(data['features'][i])

    for i, label in enumerate(vdata['labels']):
        all_data['labels'].append(label)
        all_data['features'].append(vdata['features'][i])

    param = {'trees': regressor.trees,
             'samp_split': regressor.samp_split,
             'samp_leaf': regressor.samp_leaf,
             'max_feat': regressor.max_feat}

    print(param)

    print(regressor)
    print(regressor.adjustment)
    print('\n')

    pred_all = regressor.sample_predictions(all_data,
                                            regress_limit=regress_limit,
                                            output=output_type)

    # print(all_data)
    print('Samples: {}; N_Features:  {}; Features: {}'.format(str(len(all_data['labels'])),
                                                              str(len(all_data['feature_names'])),
                                                              all_data['feature_names']))
    for elem in ['rsq', 'rmse', 'slope', 'intercept']:
        print('{} : {}'.format(elem, pred_all[elem]))
    print('\n')

    pred_train = regressor.sample_predictions(data,
                                              regress_limit=regress_limit,
                                              output=output_type)

    for i, elem in enumerate(pred_train['pred_y']):
        list_dicts[i]['output_' + data['label_name']] = elem

    # print(data)
    print('Samples: {}; N_Features:  {}; Features: {}'.format(str(len(data['labels'])),
                                                              str(len(data['feature_names'])),
                                                              data['feature_names']))
    for elem in ['rsq', 'rmse', 'slope', 'intercept']:
        print('{} : {}'.format(elem, pred_train[elem]))
    print('\n')

    pred_valid = regressor.sample_predictions(vdata,
                                              regress_limit=regress_limit,
                                              output=output_type)

    for i, elem in enumerate(pred_valid['pred_y']):
        vlist_dicts[i]['output_' + data['label_name']] = elem

    # print(vdata)
    print('Samples: {}; N_Features:  {}; Features: {}'.format(str(len(vdata['labels'])),
                                                              str(len(vdata['feature_names'])),
                                                              vdata['feature_names']))
    for elem in ['rsq', 'rmse', 'slope', 'intercept']:
        print('{} : {}'.format(elem, pred_valid[elem]))
    print('\n')

    Handler.write_to_csv(list_dicts,
                         outfile=outfile_train)

    Handler.write_to_csv(vlist_dicts,
                         outfile=outfile_valid)

    Opt.print_memory_usage()

    Opt.cprint('Done!')


