from geosoup import Handler, Opt, Raster
from geosoupML import RFRegressor, HRFRegressor
import datetime
from sys import argv


"""
Script to implement random forest regression using HRFRegressor object.
The script checks if the raster lies within a specified boundary first before implementation.
"""


# main program
if __name__ == '__main__':

    script, pickle_file_full, pickle_file_summer, raster_file, out_folder = argv

    time1 = datetime.datetime.now()

    ras = Raster(raster_file)
    ras.initialize()
    ras.nodatavalue = -9999

    Opt.cprint(ras)
    Opt.cprint(ras.bnames)

    reg_full = RFRegressor.load_from_pickle(pickle_file_full)
    reg_summer = RFRegressor.load_from_pickle(pickle_file_summer)
    reg = HRFRegressor(regressor=[reg_full, reg_summer])
    reg.data = reg_full.data

    Opt.cprint(reg_full)
    Opt.cprint(reg_summer)
    Opt.cprint(reg)

    ras.make_tile_grid(256, 256)

    outras_file = out_folder + Handler(raster_file).basename.replace('.tif', '_median_output.tif')
    outuncert_file = out_folder + Handler(raster_file).basename.replace('.tif', '_uncert.tif')

    Handler(outras_file).file_delete()
    Handler(outuncert_file).file_delete()

    Opt.cprint('Outfile: {}'.format(outras_file))
    Opt.cprint('Uncertainty: {}'.format(outuncert_file))

    outras = reg.regress_raster(ras, output_type='mean', band_name='prediction',
                                outfile=outras_file, verbose=True, nodatavalue=ras.nodatavalue)
    outras.write_to_file(compress='lzw')

    time2 = datetime.datetime.now()
    Opt.cprint('Time taken for regression: {} seconds'.format(str(round((time2-time1).total_seconds(), 1))))

    outuncert = reg.regress_raster(ras, output_type='sd', half_range=True, band_name='uncertainty',
                                   outfile=outuncert_file, verbose=True, nodatavalue=ras.nodatavalue)
    outuncert.write_to_file(compress='lzw')

    time3 = datetime.datetime.now()
    Opt.cprint('Time taken for uncertainty : {} seconds'.format(str(round((time3-time1).total_seconds(), 1))))

    ras.close()
    outras.close()
    outuncert.close()
