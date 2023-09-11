from geosoup import *
from geosoupML import *
import sys
import os


if __name__ == '__main__':

    
    script, infile, outdir, picklefile, band_name = sys.argv
    
    # ------------------------------------------------------------------------------------------

    outfile = Handler(infile).add_to_filename('_{}'.format(band_name))
    Handler(outfile).file_remove_check()

    # infile contains five bands: 1) decid
    #                             2) decid uncertainty
    #                             3) tree cover
    #                             4) tree cover uncertainty
    #                             5) land extent mask.
    # All the bands are in integer format
    # The uncertainty bands are std dev values around the mean value


    raster = Raster(infile)
    raster.initialize()
    Opt.cprint(raster.bnames)
    raster.bnames = ['decid', 'decidu', 'treecover', 'treecoveru', 'land']
    Opt.cprint(raster.bnames)
    raster.get_stats(True)

    Opt.cprint(raster.shape)

    regressor = RFRegressor.load_from_pickle(picklefile)

    Opt.cprint(regressor)

    data = regressor.data

    labels = data['labels']
    features = data['features']
    label_name = data['label_name']
    feature_names = data['feature_names']

    print(labels.shape)
    print(features.shape)


    out_raster = RFRegressor.regress_raster(regressor,
                                            raster,
                                            outfile=outfile,
                                            band_name=band_name,
                                            output_type='median',
                                            mask_band='land',
                                            tile_size=min(raster.shape[1], raster.shape[2]),
                                            array_multiplier=0.01,
                                            nodatavalue=0,
                                            verbose=True)

    Opt.cprint(out_raster)

    out_raster.write_to_file(compress='lzw', bigtiff='yes')

    uncert_dir = outdir[:-1] + '_uncert/'

    Handler(dirname=uncert_dir).dir_create()

    outfile = uncert_dir + Handler(infile).basename

    Handler(outfile).file_remove_check()

    out_raster = RFRegressor.regress_raster(regressor,
                                            raster,
                                            output_type='sd',
                                            mask_band='land',
                                            outfile=outfile,
                                            band_name=band_name,
                                            array_multiplier=0.01,
                                            internal_tile_size=512000,
                                            nodatavalue=0,
                                            verbose=True)

    Opt.cprint(out_raster)

    out_raster.write_to_file(compress='lzw', bigtiff='yes')
