from geosoup import *
from geosoupML import *
import sys
import os
import numpy as np
from sys import argv


"""
This script is used to classify a raster using a selected RF model.
This script also generates the uncertainty raster.
"""


def make_final_regressor(pickle_file,
                         llim_,
                         ulim_,
                         over_adjust=1.025,
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

    # read in the input files
    script, infile, outdir, rf_picklefile1, rf_picklefile2 = argv

    # ------------------common parameters-----------------
    ulim = 100.0
    llim = 0.0

    over_adjust_ = 1.01
    clip_ = 0.01

    nodatavalue = -9999.0
    tile_size_multiplier = 10

    band_multipliers = {'slope': 0.0001, 'swir1_2': 0.0001, 'blue_3': 0.0001, 'swir1_1': 0.0001, 'ndvi_3': 0.0001,
                        'swir2_1': 0.0001, 'swir2_2': 0.0001, 'nir_3': 0.0001, 'elevation': 1.0, 'nir_2': 0.0001,
                        'nir_1': 0.0001, 'savi_1': 0.0001, 'savi_2': 0.0001, 'savi_3': 0.0001, 'vari_3': 0.0001,
                        'vari_2': 0.0001, 'vari_1': 0.0001, 'nbr_2': 0.0001, 'nbr_3': 0.0001, 'aspect': 1.0,
                        'ndwi_1': 0.0001, 'nbr_1': 0.0001, 'red_1': 0.0001, 'red_3': 0.0001, 'red_2': 0.0001,
                        'green_1': 0.0001, 'ndwi_3': 0.0001, 'green_3': 0.0001, 'ndwi_2': 0.0001, 'green_2': 0.0001,
                        'swir1_3': 0.0001, 'ndvi_2': 0.0001, 'blue_2': 0.0001, 'blue_1': 0.0001, 'ndvi_1': 0.0001,
                        'swir2_3': 0.0001}

    Opt.cprint('-----------------------------------------------------------------')
    # print('Script: ' + script)
    Opt.cprint('Random Forest file 1: ' + rf_picklefile1)
    Opt.cprint('Random Forest file 2: ' + rf_picklefile2)

    Opt.cprint('Raster: ' + infile)
    Opt.cprint('Outdir: ' + outdir)
    Opt.cprint('-----------------------------------------------------------------')

    # load classifier from file
    rf_regressor1 = make_final_regressor(rf_picklefile1,
                                         float(llim),
                                         float(ulim),
                                         over_adjust=over_adjust_,
                                         clip=clip_)

    rf_regressor2 = make_final_regressor(rf_picklefile2,
                                         float(llim),
                                         float(ulim),
                                         over_adjust=over_adjust_,
                                         clip=clip_)
    Opt.cprint(rf_regressor1)
    Opt.cprint(rf_regressor2)

    bandnames1_ = rf_regressor1.features
    Opt.cprint('Bands 1 : ')
    Opt.cprint(bandnames1_)

    bandnames2_ = rf_regressor2.features
    Opt.cprint('Bands 2 : ')
    Opt.cprint(bandnames2_)

    bandnames_all = bandnames1_ + bandnames2_

    # get raster metadata
    ras = Raster(infile)
    ras.initialize()

    tile_size = ras.shape[2] * tile_size_multiplier

    Opt.cprint(ras)
    Opt.cprint(ras.bnames)

    bandnames = ras.bnames
    Opt.cprint('Raster bands: "' + '", "'.join(bandnames) + '"')

    band_order = Sublist(bandnames).sublistfinder(bandnames_all)
    Opt.cprint('Band order: ' + ', '.join([str(b) for b in band_order]))

    Opt.cprint('Multipliers: {}\n'.format(str(band_multipliers)))

    hierarchical_regressor = HRFRegressor(regressor=(rf_regressor1, rf_regressor2))

    Opt.cprint(hierarchical_regressor)

    # classify raster and write to file

    classif_outfile = Handler(ras.name).add_to_filename('_prediction')
    if not Handler(classif_outfile).file_exists():
        classif = hierarchical_regressor.regress_raster(ras,
                                                        tile_size=tile_size,
                                                        output_type='median',
                                                        band_name='prediction',
                                                        outdir=outdir,
                                                        nodatavalue=nodatavalue,
                                                        band_multipliers=band_multipliers)
        Opt.cprint(classif)

        classif.write_to_file(compress='lzw', bigtiff='yes')

    uncert_outfile = Handler(ras.name).add_to_filename('_uncertainty')
    if not Handler(uncert_outfile).file_exists():
        uncert = hierarchical_regressor.regress_raster(ras,
                                                       tile_size=tile_size,
                                                       output_type='sd',
                                                       band_name='uncertainty',
                                                       outdir=outdir,
                                                       nodatavalue=nodatavalue,
                                                       band_multipliers=band_multipliers)

        Opt.cprint(uncert)

        uncert.write_to_file(compress='lzw', bigtiff='yes')

    Opt.print_memory_usage()

    Opt.cprint('Done!')


