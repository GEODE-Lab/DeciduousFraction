from modules import *
import numpy as np
from sys import argv
from osgeo import gdal_array


if __name__ == '__main__':

    script, rasfile1, rasfile2, outrasfile = argv

    '''
    rasfile1 = "C:/temp/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis_nd.tif"
    rasfile2 = "C:/temp/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd.tif"

    outrasfile = 'C:/temp/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis_nd_low_res.tif'
    '''

    thresh = 20

    out_nodata = 255
    out_dtype = np.float32

    out_resx = 0.0168
    out_resy = 0.0168

    tile_size = (1024, 1024)
    image_bounds = (-162.0, -135.0, 59.0, 68.0)  # xmin, xmax, ymin, ymax

    ras1 = Raster(rasfile1)
    ras2 = Raster(rasfile2)

    ras1.initialize()
    ras2.initialize()

    tile_specs = (tile_size[0], tile_size[1], image_bounds, 'crs')

    mraster = MultiRaster(filelist=[rasfile1, rasfile2])

    Opt.cprint(mraster)

    ls_vrt = mraster.layerstack(return_vrt=True, outfile=outrasfile)

    lras = Raster('tmp_layerstack')
    lras.datasource = ls_vrt
    lras.initialize()

    xmin, xmax, ymin, ymax = lras.get_pixel_bounds(image_bounds, 'crs')

    lras.shape = [1, (ymax - ymin), (xmax - xmin)]

    lras.make_tile_grid(*tile_specs)

    Opt.cprint(len(lras.tile_grid))
    Opt.cprint(lras)

    band_order = list(range(1, len(mraster.rasters) + 1))

    out_arr = np.zeros((lras.shape[1], lras.shape[2]),
                       dtype=gdal_array.GDALTypeCodeToNumericTypeCode(lras.dtype)) + lras.nodatavalue

    Opt.cprint('Input transform: {}'.format(str(lras.transform)),
               newline='\n\n')

    # output transform
    lras.transform = (image_bounds[0],
                      lras.transform[1],
                      lras.transform[2],
                      image_bounds[3],
                      lras.transform[4],
                      lras.transform[5])

    Opt.cprint('output transform: {}'.format(str(lras.transform)),
               newline='\n\n')

    result_count = 0

    for tile_dict in lras.tile_grid:

        tile_coords = tile_dict['block_coords']
        _x, _y, _cols, _rows = tile_coords
        _xmin, _ymin = tile_dict['first_pixel']

        tile_arr = lras.get_tile(band_order, tile_coords).copy()

        if reducer == 'mean':
            temp_arr = np.apply_along_axis(lambda x: np.mean(x[x != lras.nodatavalue])
                                           if (x[x != lras.nodatavalue]).shape[0] > 0
                                           else lras.nodatavalue, 0, tile_arr)

        elif reducer == 'median':
            temp_arr = np.apply_along_axis(lambda x: np.median(x[x != lras.nodatavalue])
                                           if (x[x != lras.nodatavalue]).shape[0] > 0
                                           else lras.nodatavalue, 0, tile_arr)

        elif reducer == 'max':
            temp_arr = np.apply_along_axis(lambda x: np.max(x[x != lras.nodatavalue])
                                           if (x[x != lras.nodatavalue]).shape[0] > 0
                                           else lras.nodatavalue, 0, tile_arr)

        elif reducer == 'min':
            temp_arr = np.apply_along_axis(lambda x: np.min(x[x != lras.nodatavalue])
                                           if (x[x != lras.nodatavalue]).shape[0] > 0
                                           else lras.nodatavalue, 0, tile_arr)

        elif 'pctl' in reducer:
            pctl = int(reducer.split('_')[1])
            temp_arr = np.apply_along_axis(lambda x: np.percentile(x[x != lras.nodatavalue], pctl)
                                           if (x[x != lras.nodatavalue]).shape[0] > 0
                                           else lras.nodatavalue, 0, tile_arr)

        else:
            temp_arr = None

        y_s, y_e, x_s, x_e = (_y-_ymin), ((_y-_ymin) + _rows), (_x-_xmin), ((_x-_xmin) + _cols)

        Opt.cprint((result_count + 1, tile_dict['tie_point'], tile_dict['block_coords'], y_s, y_e, x_s, x_e))

        if temp_arr is not None:
            out_arr[y_s:y_e, x_s:x_e] = temp_arr

        result_count += 1

    lras.array = out_arr
    lras.write_to_file(outfile)

    Opt.cprint('Written {}'.format(outfile))
















