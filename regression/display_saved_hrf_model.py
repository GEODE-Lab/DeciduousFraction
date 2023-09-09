from geosoupML import RFRegressor
from geosoup import Opt, Handler


"""
This script is used to display a selected RF model.
"""


# main program
if __name__ == '__main__':

    file1 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
            "decid_pre_v1_tile_extracted_v3_west_boreal_samp_uniform_dist75_useful_feat.pickle"

    file2 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
            "decid_pre_v1_tile_extracted_v3_east_boreal_samp_uniform_dist75_useful_feat.pickle"

    file3 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
            "decid_pre_v1_tile_extracted_v3_west_boreal_samp_uniform_dist75_useful_feat_summer.pickle"

    file4 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
            "decid_pre_v1_tile_extracted_v3_east_boreal_samp_uniform_dist75_useful_feat_summer.pickle"

    picklefiles = [file1, file2, file3, file4]

    for rf_picklefile in picklefiles:

        Opt.cprint('Random Forest file 1: ' + Handler(rf_picklefile).basename)

        # load classifier from file
        regressor = RFRegressor.load_from_pickle(rf_picklefile)

        data = regressor.data
        bandnames = regressor.features
        param = {'n_estimators': regressor.n_estimators,
                 'min_samples_split': regressor.min_samples_split,
                 'min_samples_leaf': regressor.min_samples_leaf,
                 'max_features': regressor.max_features}
        feat_imp = regressor.var_importance()
        feat_imp.sort(key=lambda x: x[1], reverse=True)
        Opt.cprint(regressor)
        for k, v in param.items():
            Opt.cprint('{}: {}'.format(str(k), str(v)))
        Opt.cprint(data)
        Opt.cprint('Adjustment:')
        Opt.cprint(regressor.adjustment)
        Opt.cprint('Feature importance:')
        for k, v in feat_imp:
            Opt.cprint('{}: {:.2f}'.format(str(k), v*100.0))

        Opt.cprint('-----------------------------------------------------------------')
