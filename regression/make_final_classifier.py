from geosoupML import *
from sys import argv

if __name__ == '__main__':

    script, pickle_file, out_file = argv

    # load classifier from file
    regressor = RFRegressor.load_from_pickle(pickle_file)
    print(regressor)

    data = regressor.data
    vdata = regressor.vdata

    print('Training samples: {}'.format(str(len(data['features']))))
    print('Validation samples: {}'.format(str(len(vdata['features']))))

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

    ulim = 1.0
    llim = 0.0

    # initialize RF classifier
    model = RFRegressor(**param)

    print(model)

    # fit RF classifier using training data
    model.fit_data(all_data)

    model.get_adjustment_param(clip=0.01,
                               data_limits=[ulim, llim],
                               over_adjust=1.05)

    model.get_training_fit()

    print(model)
    print(model.training_results)

    out_file = Handler(filename=out_file).file_remove_check()
    print(out_file)

    model.pickle_it(out_file)
