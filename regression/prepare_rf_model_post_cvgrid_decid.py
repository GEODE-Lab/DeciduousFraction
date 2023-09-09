from geosoup import Handler
from geosoupML import RFRegressor, Samples


"""
This script initializes and fits training data to random forest regressors 
to find the optimum set of parameters. The data is used from a pre-pared csv file.
The number of folds used is 5 by default.
"""


# main program
if __name__ == '__main__':

    # input csv files
    infile_full_east = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                       "decid_pre_v1_tile_extracted_v3_east_boreal_samp_uniform_dist75_useful_feat.csv"

    infile_full_west = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                       "decid_pre_v1_tile_extracted_v3_west_boreal_samp_uniform_dist75_useful_feat.csv"

    infile_summer_east = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                         "decid_pre_v1_tile_extracted_v3_east_boreal_samp_uniform_dist75_useful_feat_summer.csv"

    infile_summer_west = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                         "decid_pre_v1_tile_extracted_v3_west_boreal_samp_uniform_dist75_useful_feat_summer.csv"

    # output pickle files and parameters
    outfile_full_east = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                        "decid_pre_v1_tile_extracted_v3_east_boreal_samp_uniform_dist75_useful_feat.pickle"
    regress_full_east_param = {"min_samples_split": 8,
                               "max_features": 12,
                               "n_estimators": 500,
                               "min_samples_leaf": 3}

    outfile_full_west = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                        "decid_pre_v1_tile_extracted_v3_west_boreal_samp_uniform_dist75_useful_feat.pickle"
    regress_full_west_param = {"min_samples_split": 4,
                               "max_features": 24,
                               "n_estimators": 800,
                               "min_samples_leaf": 3}

    outfile_summer_east = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                          "decid_pre_v1_tile_extracted_v3_east_boreal_samp_uniform_dist75_useful_feat_summer.pickle"
    regress_summer_east_param = {"min_samples_split": 22,
                                 "max_features": 6,
                                 "n_estimators": 200,
                                 "min_samples_leaf": 8}

    outfile_summer_west = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/" \
                          "decid_pre_v1_tile_extracted_v3_west_boreal_samp_uniform_dist75_useful_feat_summer.pickle"
    regress_summer_west_param = {"min_samples_split": 2,
                                 "max_features": 12,
                                 "n_estimators": 500,
                                 "min_samples_leaf": 3}

    label_colname = 'decid_frac'

    # east full -----------------------------------------------------------

    reg_east_full = RFRegressor(**regress_full_east_param)
    samp_east = Samples(infile_full_east, label_colname=label_colname)
    trn_samp, val_samp = samp_east.random_partition(70)
    east_full_holdout_samp_file = outfile_full_east.replace('.pickle', '_holdout.csv')
    Handler(east_full_holdout_samp_file).file_delete()
    val_samp.save_to_file(east_full_holdout_samp_file)

    print(reg_east_full)
    print(samp_east)
    print(trn_samp)
    print(val_samp)

    reg_east_full.fit_data(trn_samp)
    reg_east_full.get_adjustment_param()
    reg_east_full.get_training_fit(val_samp)
    Handler(outfile_full_east).file_delete()
    reg_east_full.pickle_it(outfile_full_east)

    print(reg_east_full)
    print(reg_east_full.training_results)

    # west full -----------------------------------------------------------

    reg_west_full = RFRegressor(**regress_full_west_param)
    samp_west = Samples(infile_full_west, label_colname=label_colname)
    trn_samp, val_samp = samp_west.random_partition(70)
    west_full_holdout_samp_file = outfile_full_west.replace('.pickle', '_holdout.csv')
    Handler(west_full_holdout_samp_file).file_delete()
    val_samp.save_to_file(west_full_holdout_samp_file)

    print(reg_west_full)
    print(samp_west)
    print(trn_samp)
    print(val_samp)

    reg_west_full.fit_data(trn_samp)
    reg_west_full.get_adjustment_param()
    reg_west_full.get_training_fit(val_samp)
    Handler(outfile_full_west).file_delete()
    reg_west_full.pickle_it(outfile_full_west)

    print(reg_west_full)
    print(reg_west_full.training_results)

    # east summer -----------------------------------------------------------

    reg_east_summer = RFRegressor(**regress_summer_east_param)
    samp_east = Samples(infile_summer_east, label_colname=label_colname)
    trn_samp, val_samp = samp_east.random_partition(70)
    east_summer_holdout_samp_file = outfile_summer_east.replace('.pickle', '_holdout.csv')
    Handler(east_summer_holdout_samp_file).file_delete()
    val_samp.save_to_file(east_summer_holdout_samp_file)

    print(reg_east_summer)
    print(samp_east)
    print(trn_samp)
    print(val_samp)

    reg_east_summer.fit_data(trn_samp)
    reg_east_summer.get_adjustment_param()
    reg_east_summer.get_training_fit(val_samp)
    Handler(outfile_summer_east).file_delete()
    reg_east_summer.pickle_it(outfile_summer_east)

    print(reg_east_summer)
    print(reg_east_summer.training_results)

    # west summer -----------------------------------------------------------

    reg_west_summer = RFRegressor(**regress_summer_west_param)
    samp_west = Samples(infile_summer_west, label_colname=label_colname)
    trn_samp, val_samp = samp_west.random_partition(70)
    west_summer_holdout_samp_file = outfile_summer_west.replace('.pickle', '_holdout.csv')
    Handler(west_summer_holdout_samp_file).file_delete()
    val_samp.save_to_file(west_summer_holdout_samp_file)

    print(reg_west_summer)
    print(samp_west)
    print(trn_samp)
    print(val_samp)

    reg_west_summer.fit_data(trn_samp)
    reg_west_summer.get_adjustment_param()
    reg_west_summer.get_training_fit(val_samp)
    Handler(outfile_summer_west).file_delete()
    reg_west_summer.pickle_it(outfile_summer_west)

    print(reg_west_summer)
    print(reg_west_summer.training_results)
