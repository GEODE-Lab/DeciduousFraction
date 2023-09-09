from geosoup import Handler, Opt, Raster, GDAL_FIELD_DEF
from geosoupML import RFRegressor
from sys import argv


if __name__ == '__main__':
    '''
    script, infile, outdir, picklefile, band_name = argv
    '''
    # infile = "C:/temp/decid_tc_2000_layerstack-0000026880-0000161280.tif"
    infile = "D:/temp/albedo/decid_tc_2000-0000098304-0000425984_clip_1deg_1deg.tif"
    outdir = "D:/temp/albedo/"

    pickle_dir = "d:/shared/Dropbox/projects/NAU/landsat_deciduous/data/albedo_data/"
    picklefiles = ("RFalbedo_deciduous_fraction_treecover_50000_cutoff_5_deg1_20200501T185635_spring.pickle",
                   "RFalbedo_deciduous_fraction_treecover_50000_cutoff_5_deg1_20200501T185635_summer.pickle",
                   "RFalbedo_deciduous_fraction_treecover_50000_cutoff_5_deg1_20200501T185635_fall.pickle")

    picklefiles = [pickle_dir + picklefile for picklefile in picklefiles]

    band_name = 'spr_albedo'


    outfile = outdir + Handler(Handler(infile).basename).add_to_filename('_output3')

    Handler(outfile).file_remove_check()

    # raster contains three bands: 1) decid 2) tree cover 3) land extent mask.
    # all the bands are in integer format
    raster = Raster(infile)
    raster.initialize()
    raster.bnames = ['decid', 'treecover']

    raster.get_stats(True)

    Opt.cprint(raster.shape)

    regressor = RFRegressor.load_from_pickle(picklefiles[0])

    Opt.cprint(regressor)

    Opt.cprint(regressor.adjustment)

    out_raster = RFRegressor.regress_raster(regressor,
                                            raster,
                                            output_type='mean',
                                            outfile=outfile,
                                            band_name=band_name,
                                            array_multiplier=0.01,
                                            nodatavalue=0.0,
                                            tile_size=1024,
                                            check_bands=1,
                                            verbose=True)

    Opt.cprint(out_raster)

    out_raster.write_to_file(compress='lzw', bigtiff='yes')

    outfile = outdir + Handler(Handler(infile).basename).add_to_filename('_uncert3')

    Handler(outfile).file_remove_check()

    out_raster = RFRegressor.regress_raster(regressor,
                                            raster,
                                            output_type='sd',
                                            outfile=outfile,
                                            band_name=band_name,
                                            array_multiplier=0.01,
                                            nodatavalue=0.0,
                                            check_bands=1,
                                            tile_size=1024,
                                            out_data_type=GDAL_FIELD_DEF['float'],
                                            verbose=True)

    Opt.cprint(out_raster)

    out_raster.write_to_file(compress='lzw', bigtiff='yes')
