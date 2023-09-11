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
    train_samp.save_to_file(Handler(sampfile).add_to_filename('_training'))

    Handler(Handler(sampfile).add_to_filename('_validation')).file_delete()
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

    sampfile = "C:/shared/projects/NAU/landsat_deciduous/data/samples/"\
               "hansen_tc_mosaic_2010_coll1_samp_v1_corrected_useful.csv"
    sampfile_summer = "C:/shared/projects/NAU/landsat_deciduous/data/samples/"\
                      "hansen_tc_mosaic_2010_coll1_samp_v1_corrected_useful_summer.csv"

    main_reg = {'min_samples_split': 4,
                'max_features': 12,
                'n_estimators': 2000,
                'min_samples_leaf': 2,
                'max_depth': 24}

    summer_reg = {'min_samples_split': 12,
                  'max_features': 8,
                  'n_estimators': 1200,
                  'min_samples_leaf': 4,
                  'max_depth': 16}

    regressor_main = make_regressor(sampfile,
                                    'tree_cover',
                                    True,
                                    **main_reg)

    regressor_summer = make_regressor(sampfile_summer,
                                      'tree_cover',
                                      True,
                                      **summer_reg)

    print(regressor_main)
    print(regressor_summer)
