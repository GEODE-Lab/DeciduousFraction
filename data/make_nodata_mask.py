from geosoup import Raster, Handler, Opt, GDAL_FIELD_DEF
import numpy as np
import sys

if __name__ == '__main__':

    script, infile, outfile = sys.argv
    '''
    infile = "D:/temp/ABoVE_median_SR_NDVI_1_2015-0000000000-0000079360.tif"
    outfile = "D:/temp/ABoVE_median_SR_NDVI_1_2015-0000000000-0000079360_mask.tif"
    '''
    band_id = 14
    bad_values = [0, -9999]

    raster = Raster(infile)
    raster.initialize()

    Opt.cprint(raster)
    Opt.cprint(raster.bnames[band_id])

    raster.read_array(band_order=[band_id])
    arr = raster.array

    outarr = np.zeros(arr.shape, dtype=np.int8) + 1

    for bad_value in bad_values:
        outarr[np.where(arr == bad_value)] = 0

    raster.array = outarr

    raster.dtype = GDAL_FIELD_DEF['byte']
    raster.nodatavalue = 0
    raster.bnames = ['mask']
    
    Handler(outfile).file_delete()
    raster.write_to_file(outfile)






