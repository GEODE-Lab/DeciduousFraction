from geosoupML import RFRegressor, Samples
from geosoup import Handler, Opt
import numpy as np
from sys import argv


def make_regressor(sampfile,
                   label_colname,
                   verbose=True,
                   multiplier=10000,
                   **kwparam):

    samp = Samples(sampfile, label_colname=label_colname)
    train_samp, valid_samp = samp.random_partition(80)

    if verbose:
        Opt.cprint(samp)
        Opt.cprint(train_samp)
        Opt.cprint(valid_samp)

    Handler(Handler(sampfile).add_to_filename('_training')).file_delete()
    train_samp.x = (train_samp.x * 10000.0).astype(np.int16)
    train_samp.save_to_file(Handler(sampfile).add_to_filename('_training'))

    Handler(Handler(sampfile).add_to_filename('_validation')).file_delete()
    valid_samp.x = (valid_samp.x * 10000.0).astype(np.int16)
    valid_samp.save_to_file(Handler(sampfile).add_to_filename('_validation'))

    regressor = RFRegressor(**kwparam)
    regressor.fit_data(train_samp, output_type='mean')

    regressor.get_adjustment_param()
    pred = regressor.sample_predictions(valid_samp)

    var_imp = regressor.var_importance()
    sorted_var_imp = reversed(sorted(var_imp, key=lambda x: x[1]))

    if verbose:
        Opt.cprint(regressor)
        Opt.cprint(regressor.training_results)
        Opt.cprint(regressor.adjustment)
        Opt.cprint('\nValidation samp:')
        disp_elem = ['rsq', 'slope', 'intercept']
        for elem in disp_elem:
            Opt.cprint("{} - {:.2f}".format(elem, pred[elem]))
        Opt.cprint('--------------------------------------------------\n')
        for elem in sorted_var_imp:
            Opt.cprint("{} - {:.2f}".format(elem[0], elem[1]*100))
        Opt.cprint('==================================================\n')

    Handler(Handler(sampfile).add_to_filename(new_extension='.pickle')).file_delete()
    regressor.pickle_it(Handler(sampfile).add_to_filename(new_extension='.pickle'))

    return regressor


if __name__ == '__main__':

    # script, sampfile_main, sampfile_summer = argv

    sampfile_west = "C:/shared/projects/NAU/landsat_deciduous/data/samples/"\
                    "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_" \
                    "west_boreal_samp_useful_uniform_dist67_reduced.csv"
    sampfile_summer = "C:/shared/projects/NAU/landsat_deciduous/data/samples/"\
                      "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_" \
                      "west_boreal_samp_useful_uniform_dist67_summer_reduced.csv"
    sampfile_east = "C:/shared/projects/NAU/landsat_deciduous/data/samples/"\
                    "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_" \
                    "east_boreal_samp_useful_uniform_dist67_reduced.csv"
    sampfile_east_summer = "C:/shared/projects/NAU/landsat_deciduous/data/samples/"\
                           "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_" \
                           "east_boreal_samp_useful_uniform_dist67_summer_reduced.csv"

    '''
    < 20 % diff between training and val
    west_reg = {min_samples_split=16, max_features=16, n_estimators=800, min_samples_leaf=4, max_depth=20}
    west_summer = {min_samples_split=20, max_features=7, n_estimators=1600, min_samples_leaf=4, max_depth=16}
    east_reg = {min_samples_split=8, max_features=16, n_estimators=1200, min_samples_leaf=12, max_depth=12}
    east_summer = {min_samples_split=2, max_features=7, n_estimators=1600, min_samples_leaf=1, max_depth=8}  
    '''

    west_reg = {'min_samples_split': 2,
                'max_features': 4,
                'n_estimators': 800,
                'min_samples_leaf': 1,}
                #  'max_depth': 20}

    west_summer = {'min_samples_split': 2,
                   'max_features': 2,
                   'n_estimators': 800,
                   'min_samples_leaf': 1,}
                   #  'max_depth': 20}

    east_reg = {'min_samples_split': 2,
                'max_features': 4,
                'n_estimators': 800,
                'min_samples_leaf': 1,}
                #  'max_depth': 12}

    east_summer = {'min_samples_split': 8,
                   'max_features': 2,
                   'n_estimators': 800,
                   'min_samples_leaf': 1,}
                   #  'max_depth': 8}

    regressor_west = make_regressor(sampfile_west,
                                    'decid_frac',
                                    True,
                                    **west_reg)

    regressor_summer = make_regressor(sampfile_summer,
                                      'decid_frac',
                                      True,
                                      **west_summer)

    regressor_east = make_regressor(sampfile_east,
                                    'decid_frac',
                                    True,
                                    **east_reg)

    regressor_east_summer = make_regressor(sampfile_east_summer,
                                           'decid_frac',
                                           True,
                                           **east_summer)

    # print(regressor_west)
    # print(regressor_summer)
    print(regressor_east)
    print(regressor_east_summer)
