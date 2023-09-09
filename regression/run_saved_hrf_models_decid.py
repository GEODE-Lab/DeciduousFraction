from geosoup import Handler, Opt, Raster, Vector
from geosoupML import RFRegressor, HRFRegressor
import datetime
from sys import argv


"""
Script to implement random forest regression using HRFRegressor object.
The script checks if the raster lies within a specified boundary first before implementation.
"""


# main program
if __name__ == '__main__':

    time1 = datetime.datetime.now()
    '''
    script, pickle_file_full, pickle_file_summer, boundary_file, region, raster_file, out_folder = argv

    '''
    raster_file = "C:/temp/Boreal_NA_pctl50_95_50_SR_NDVI_zone4_2010-0000039680-0000039680.tif"
    boundary_file = "C:/Shared/projects/NAU/landsat_deciduous/data/STUDY_AREA/"\
        "buffered_CAN_AK.shp"
    out_folder = "C:/temp/output/"

    pickle_file_full = "C:/shared/projects/NAU/landsat_deciduous/data/samples/" \
                       "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_" \
                       "west_boreal_samp_useful_uniform_dist67_reduced_nir.pickle"
    pickle_file_summer = "C:/shared/projects/NAU/landsat_deciduous/data/samples/" \
                         "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_" \
                         "west_boreal_samp_useful_uniform_dist67_summer_reduced_nir.pickle"
    region = 'west'

    ras = Raster(raster_file)
    ras.initialize()
    ras.nodatavalue = -9999
    ras_bounds = ras.get_bounds()
    ras_bounds_wkt = Vector.wkt_from_coords(ras_bounds, 'polygon')
    ras_bounds_geom = Vector.get_osgeo_geom(ras_bounds_wkt)
    Opt.cprint(ras)
    Opt.cprint(ras.bnames)

    bounds_vec = Vector(boundary_file)

    if region == 'west':
        bounds_geom = Vector.get_osgeo_geom(bounds_vec.wktlist[1])
    elif region == 'east':
        bounds_geom = Vector.get_osgeo_geom(bounds_vec.wktlist[0])
    else:
        raise ValueError('Invalid region')

    Opt.cprint(bounds_vec)

    if bounds_geom.Intersects(ras_bounds_geom):

        Opt.cprint('Raster inside boundary\n\n')

        reg_full = RFRegressor.load_from_pickle(pickle_file_full)
        reg_summer = RFRegressor.load_from_pickle(pickle_file_summer)
        reg = HRFRegressor(regressor=[reg_full, reg_summer])
        reg.data = reg_full.data

        Opt.cprint(reg_full)
        Opt.cprint(reg_summer)
        Opt.cprint(reg)

        ras.make_tile_grid(256, 256)

        outras_file = out_folder + Handler(raster_file).basename.replace('.tif', '_median_output_{}.tif'.format(region))
        outuncert_file = out_folder + Handler(raster_file).basename.replace('.tif', '_uncert_{}.tif'.format(region))

        Handler(outras_file).file_delete()
        Handler(outuncert_file).file_delete()

        Opt.cprint('Outfile: {}'.format(outras_file))
        Opt.cprint('Uncertainty: {}'.format(outuncert_file))

        outras = reg.regress_raster(ras, output_type='median', band_name='prediction',
                                    outfile=outras_file, verbose=True, nodatavalue=ras.nodatavalue)
        outras.write_to_file(compress='lzw')

        time2 = datetime.datetime.now()
        Opt.cprint('Time taken for regression: {} seconds'.format(str(round((time2-time1).total_seconds(), 1))))

        outuncert = reg.regress_raster(ras, output_type='sd', half_range=True, band_name='uncertainty',
                                       outfile=outuncert_file, verbose=True, nodatavalue=ras.nodatavalue)
        outuncert.write_to_file(compress='lzw')

        time3 = datetime.datetime.now()
        Opt.cprint('Time taken for uncertainty : {} seconds'.format(str(round((time3-time1).total_seconds(), 1))))

    else:
        Opt.cprint('Raster outside boundary')

    ras.close()
