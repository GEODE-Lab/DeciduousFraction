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

# main program
if __name__ == '__main__':

    # read in the input files
    script, infile, outdir, rf_picklefile = argv

    Opt.cprint('-----------------------------------------------------------------')
    # print('Script: ' + script)
    Opt.cprint('Random Forest file: ' + rf_picklefile)
    Opt.cprint('Raster: ' + infile)
    Opt.cprint('Outdir: ' + outdir)
    Opt.cprint('-----------------------------------------------------------------')

    # load classifier from file
    rf_regressor = RFRegressor.load_from_pickle(rf_picklefile)
    Opt.cprint(rf_regressor)

    bandnames_ = rf_regressor.features
    Opt.cprint('Bands : ')
    Opt.cprint(bandnames_)

    # get raster metadata
    ras = Raster(infile)
    ras.initialize()

    Opt.cprint(ras.shape)
    Opt.cprint(ras)

    bandnames = ras.bnames
    Opt.cprint('Raster bands: "' + '", "'.join(bandnames) + '"')

    band_order = Sublist(bandnames).sublistfinder(bandnames_)
    Opt.cprint('Band order: ' + ', '.join([str(b) for b in band_order]))

    # re-initialize raster
    ras.initialize(get_array=True,
                   band_order=band_order)

    multipliers = {'slope': 0.0001, 'swir1_2': 0.0001, 'blue_3': 0.0001, 'swir1_1': 0.0001, 'ndvi_3': 0.0001,
                   'nir_3': 0.0001, 'elevation': 1.0, 'nir_2': 0.0001, 'nir_1': 0.0001, 'vari_3': 0.0001,
                   'vari_2': 0.0001, 'vari_1': 0.0001, 'nbr_2': 0.0001, 'nbr_3': 0.0001, 'aspect': 1.0,
                   'nbr_1': 0.0001, 'red_1': 0.0001, 'red_3': 0.0001, 'red_2': 0.0001, 'swir1_3': 0.0001,
                   'ndvi_2': 0.0001, 'blue_2': 0.0001, 'blue_1': 0.0001, 'ndvi_1': 0.0001}

    Opt.cprint('Multipliers: {}\n'.format(str(multipliers)))

    Opt.cprint(ras)

    # classify raster and write to file
    classif = RFRegressor.regress_raster(rf_regressor,
                                         ras,
                                         output_type='pred',
                                         band_name='prediction',
                                         outdir=outdir,
                                         out_data_type=6,  # float32
                                         nodatavalue=-9999.0,
                                         band_multipliers=multipliers)
    Opt.cprint(classif)

    classif.write_to_file()

    uncert = RFRegressor.regress_raster(rf_regressor,
                                        ras,
                                        output_type='sd',
                                        band_name='uncertainty',
                                        outdir=outdir,
                                        out_data_type=6,  # float32
                                        intvl=95,
                                        nodatavalue=-9999.0,
                                        band_multipliers=multipliers)

    Opt.cprint(uncert)

    uncert.write_to_file()

    Opt.print_memory_usage()

    Opt.cprint('Done!')


