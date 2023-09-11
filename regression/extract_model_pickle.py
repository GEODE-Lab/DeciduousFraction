# from geosoupML import RFRegressor, HRFRegressor
# from geosoup import Opt, Handler, Raster, Sublist
import sys
import os
from geosoup import *
import numpy as np
from geosoupML import *


"""
This script is used to extract a pickled RF regressor from a previous python version 2.7.15
Use this script to extract RF model data only after switching to a python 2.7.15 environment
"""


def make_final_regressor(pickle_file,
                         llim_,
                         ulim_,
                         over_adjust=1.0,
                         clip=0.01):

    # load classifier from file
    regressor = RFRegressor.load_from_pickle(pickle_file)

    data = regressor.data
    vdata = regressor.vdata

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

    # initialize RF classifier
    model = RFRegressor(**param)

    # fit RF classifier using training data
    model.fit_data(all_data)

    model.get_adjustment_param(clip=clip,
                               data_limits=[llim_, ulim_],
                               over_adjust=over_adjust)

    return model


# main program
if __name__ == '__main__':


    ulim = 1.0
    llim = 0.0
    over_adjust_ = 1.0
    clip_ = 0.01

    active_dir = "D:/temp/pickle_dir/working/"

    outdir = active_dir + "out/"

    rf_file_list = Handler(dirname=active_dir).find_all('*.pickle')

    '''
    rf_file_list = list(active_dir + filename for filename in
                        ["out_tc_2010_samp_v1_summer_RF_772.pickle",
                         "out_tc_2010_samp_v1_RF_59.pickle"])
    '''
    outfiles = list(filename.replace('.pickle', '.txt') for filename in rf_file_list)

    for i, filename in enumerate(rf_file_list):

        print('-----------------------------------------------------------------')
        print('Random Forest file {}: {}'.format(str(i+1), filename))
        print('Output text file {}'.format(outfiles[i]))
        print('-----------------------------------------------------------------')

        try:
            '''
            regressor = make_final_regressor(filename,
                                             float(llim),
                                             float(ulim),
                                             over_adjust=over_adjust_,
                                             clip=clip_)
            '''
            regressor = RFRegressor.load_from_pickle(filename)

            data = np.hstack([regressor.data['features'],
                              regressor.data['labels'][:, np.newaxis]])
            colnames = regressor.data['feature_names'] + [regressor.data['label_name']]

            datafile = outfiles[i].replace('.txt', '_data.csv')

            Handler(datafile).write_numpy_array_to_file(data,
                                                        colnames=colnames)

            vdata = np.hstack([regressor.vdata['features'],
                               regressor.vdata['labels'][:, np.newaxis]])
            vcolnames = regressor.vdata['feature_names'] + [regressor.vdata['label_name']]

            vdatafile = outfiles[i].replace('.txt', '_vdata.csv')

            Handler(vdatafile).write_numpy_array_to_file(vdata,
                                                         colnames=vcolnames)

            with open(outfiles[i], 'w') as outf:
                outf.write(regressor.__repr__() + "\n")

                for key in dir(regressor):
                    outf.write('{} : {}\n'.format(str(key), str(getattr(regressor, key, None))))

        except Exception as e:
            print(e)
            continue
