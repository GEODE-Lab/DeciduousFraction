from geosoup import Raster, Handler, Opt, MultiRaster, Vector
from osgeo import gdal_array
import multiprocessing as mp
import numpy as np
import json
import sys

"""
This script is used to layer stack Bluesky albedo data from
https://daac.ornl.gov/ABOVE/guides/Albedo_Boreal_North_America.html
using valid quality flags corresponding to the following:

Minimum number of pixels with valid QA flags = 1 (default)

sza_above_70 flag values: 0 
mcd43a2_qflag flag values: 0 or 1
snow_flag: ignored
aod_data_source: ignored

"""

MIN_QA_PIXELS = 1
TILE_SIZE = (128, 128)
IMAGE_BOUNDS = (-179.999, -50.0, 30.0, 75.0)  # x min, x max, y min, y max
VALID_QA = [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23]
VALID_QA2 = list(range(0, 64))


def tile_process(args):
    """
    Method to run tile by tile processing in parallel
    :param args: tile_dictionary, main_arr, qa_arr, tile_nodata, qa_nodata
    :return: y_start, y_end, x_start, x_end, temp_arr, tile_dictionary
    """

    tile_dictionary, main_arr, qa_arr, tile_nodata, qa_nodata, reducer = args

    _x, _y, _cols, _rows = tile_dictionary['block_coords']
    _xmin, _ymin = tile_dictionary['first_pixel']

    y_start, y_end, x_start, x_end = \
        (_y - _ymin), ((_y - _ymin) + _rows), (_x - _xmin), ((_x - _xmin) + _cols)

    temp_arr = np.zeros(_cols * _rows,
                        dtype=np.array([tile_nodata]).dtype)

    tile = main_arr.reshape([main_arr.shape[0], _cols * _rows])
    qa = qa_arr.reshape([qa_arr.shape[0], _cols * _rows])

    tile[np.isnan(tile)] = tile_nodata
    tile[np.isinf(tile)] = tile_nodata
    qa[np.isnan(tile)] = qa_nodata
    qa[np.isinf(tile)] = qa_nodata

    for indx in range(_cols * _rows):
        temp_arr[indx] = qa_compare(tile[:, indx],
                                    qa[:, indx],
                                    nodata=tile_nodata,
                                    reducer=reducer)

    temp_arr = temp_arr.reshape([_rows, _cols])

    return y_start, y_end, x_start, x_end, temp_arr, tile_dictionary


def get_tiles(multiras, qual_multiras, reducer):
    """
    Method to yield tile array of the main raster and quality raster tile array

    """
    for tile_dictionary in multiras.tile_grid:
        tile_coordinates = tile_dictionary['block_coords']

        yield tile_dictionary, \
            multiras.get_tile(band_order, tile_coordinates), \
            qual_multiras.get_tile(band_order, tile_coordinates), \
            multiras.nodatavalue, \
            qual_multiras.nodatavalue, \
            reducer


def bounds2wkt(x_min, x_max, y_min, y_max):
    """
    Method to convert bounds in image coordinate system to wkt geometry
    :param x_min: float
    :param x_max: float
    :param y_min: float
    :param y_max: float
    :return: string
    """
    return Vector.wkt_from_coords([(x_min, y_max),
                                   (x_max, y_max),
                                   (x_max, y_min),
                                   (x_min, y_min),
                                   (x_min, y_max)],
                                  geom_type='polygon')


def qa_compare(pixel_vec,
               qa_vec,
               nodata=-9999.0,
               min_num=MIN_QA_PIXELS,
               reducer='mean'):
    """
    Method to take mean of pixels taht have a valid QA flag and are non-nodata pixels
    :param pixel_vec: Pixel array
    :param qa_vec: QA flag array
    :param nodata: No data value
    :param min_num: Minimum number of pixels with valid qa flag
    :param reducer: Method to reduce the pixel vector with (mean, median, pctl_xx)
    :return: Scalar
    """
    good_pixel_location = ~(np.isnan(pixel_vec) |
                            np.isinf(pixel_vec) |
                            np.isnan(qa_vec) |
                            np.isinf(qa_vec) |
                            np.isin(pixel_vec, [nodata]))

    pixel_vec = pixel_vec[np.where(good_pixel_location)]
    qa_vec = qa_vec[np.where(good_pixel_location)]

    if pixel_vec.size == 0:
        return nodata
    else:
        valid_qa_px = np.isin(qa_vec, VALID_QA)

        if np.count_nonzero(valid_qa_px) >= min_num:
            valid_locs = np.where(valid_qa_px)
        else:
            valid_locs = np.where(np.isin(qa_vec, VALID_QA2))

        if reducer == 'mean':
            out_val = np.mean(pixel_vec[valid_locs]) * (valid_locs[0].size > 0) + \
                nodata * (valid_locs[0].size == 0)
        elif reducer == 'median':
            out_val = np.median(pixel_vec[valid_locs]) * (valid_locs[0].size > 0) + \
                      nodata * (valid_locs[0].size == 0)
        elif 'pctl' in reducer:
            pctl = int(reducer.replace('pctl_', ''))
            out_val = np.percentile(pixel_vec[valid_locs], pctl, interpolation='nearest') * (valid_locs[0].size > 0) + \
                nodata * (valid_locs[0].size == 0)
        else:
            out_val = nodata * (valid_locs[0].size == 0)

        return out_val if not (np.isnan(out_val) | np.isinf(out_val)) else nodata


if __name__ == '__main__':

    script, file_folder, outdir, startyear, endyear, startdate, enddate, ver, reducer_name, nprocs = sys.argv

    '''
    file_folder = 'D:/temp/albedo/geographic_clip/'
    outdir = 'D:/temp/albedo/geo_out/'
    ver = 2
    startyear = 2000
    endyear = 2002
    startdate = 150
    enddate = 240
    reducer = pctl_90
    '''

    nprocs = int(nprocs)
    startyear = int(startyear)
    endyear = int(endyear)
    startdate = int(startdate)
    enddate = int(enddate)

    # find albedo files
    albedo_files = Handler(dirname=file_folder).find_all('*_albedo.tif')

    # list of quality files
    quality_files = [elem.replace('_albedo.tif', '_quality.tif') for elem in albedo_files]

    # list of date and year
    num_list = np.array(list(list(int(elem_) for elem_
                                  in Handler(elem).basename
                                  .replace('_albedo.tif', '')
                                  .replace('bluesky_albedo_', '')
                                  .split('_'))
                             for elem in albedo_files))

    Opt.cprint((startdate, enddate))
    Opt.cprint((startyear, endyear))
    Opt.cprint(len(albedo_files))

    # sort files by date and year to composite
    file_loc_on_list = np.where((num_list[:, 0] >= startyear) & (num_list[:, 0] <= endyear) &
                                (num_list[:, 1] >= startdate) & (num_list[:, 1] <= enddate))[0]

    # make list of files
    filelist = list(albedo_files[i] for i in file_loc_on_list.tolist())
    qa_list = list(quality_files[i] for i in file_loc_on_list.tolist())

    for file_ in filelist:
        Opt.cprint(file_)

    outfile = outdir + '/albedo_composite_{}_{}_{}_{}_{}_v{}.tif'.format(reducer_name,
                                                                         str(startyear),
                                                                         str(endyear),
                                                                         str(startdate),
                                                                         str(enddate),
                                                                         str(ver))

    qa_file = outdir + '/quality_composite_{}_{}_{}_{}_{}_v{}.tif'.format(reducer_name,
                                                                          str(startyear),
                                                                          str(endyear),
                                                                          str(startdate),
                                                                          str(enddate),
                                                                          str(ver))

    Opt.cprint('Output file: {}'.format(outfile))

    # Multi raster objects for layer stacking
    lraster = MultiRaster(filelist=filelist)
    qraster = MultiRaster(filelist=qa_list)

    Opt.cprint(lraster)

    # layer stack VRTs
    ls_vrt = lraster.layerstack(return_vrt=True, outfile=outfile)
    qa_vrt = qraster.layerstack(return_vrt=True, outfile=qa_file)

    # albedo layer stack Raster object
    lras = Raster('alb_layerstack')
    lras.datasource = ls_vrt
    lras.initialize()

    # albedo QA flag layerstack Raster object
    qras = Raster('qa_layerstack')
    qras.datasource = qa_vrt
    qras.initialize()

    lras_bound_geom = Vector.get_osgeo_geom(Vector.wkt_from_coords(lras.bounds, geom_type='polygon'))
    max_outer_bounds = Vector.get_osgeo_geom(bounds2wkt(*IMAGE_BOUNDS))

    bounds_intersection = lras_bound_geom.Intersection(max_outer_bounds)
    bounds_json = json.loads(bounds_intersection.ExportToJson())
    bounds_coords = np.array(bounds_json['coordinates'][0])

    xmin, xmax, ymin, ymax = (bounds_coords[:, 0].min(),
                              bounds_coords[:, 0].max(),
                              bounds_coords[:, 1].min(),
                              bounds_coords[:, 1].max())

    pixel_xmin, pixel_xmax, pixel_ymin, pixel_ymax = lras.get_pixel_bounds(bound_coords=(xmin, xmax, ymin, ymax),
                                                                           coords_type='crs')
    lras.shape = [1, (pixel_ymax - pixel_ymin), (pixel_xmax - pixel_xmin)]

    tile_specs = (TILE_SIZE[0], TILE_SIZE[1], (xmin, xmax, ymin, ymax), 'crs')

    # make tiles for the Raster objects
    lras.make_tile_grid(*tile_specs)
    qras.make_tile_grid(*tile_specs)

    Opt.cprint(len(lras.tile_grid))
    Opt.cprint(lras)

    band_order = list(range(1, len(lraster.rasters) + 1))

    # output raster array
    out_arr = np.zeros((1, lras.shape[1], lras.shape[2]),
                       dtype=gdal_array.GDALTypeCodeToNumericTypeCode(lras.dtype)) + lras.nodatavalue

    Opt.cprint('Input transform: {}'.format(str(lras.transform)),
               newline='\n\n')

    # output transform
    lras.transform = (xmin,
                      lras.transform[1],
                      lras.transform[2],
                      ymax,
                      lras.transform[4],
                      lras.transform[5])

    Opt.cprint('output transform: {}'.format(str(lras.transform)),
               newline='\n\n')

    result_count = 0

    print('Tile count: {}'.format(str(lras.ntiles)))

    pool = mp.Pool(nprocs-1)

    for out_args in pool.imap_unordered(tile_process, get_tiles(lras, qras, reducer_name)):
        y_s, y_e, x_s, x_e, tile_arr, tile_dict = out_args

        Opt.cprint((result_count + 1,
                    tile_dict['tie_point'],
                    tile_dict['block_coords'],
                    y_s, y_e, x_s, x_e))

        # assign computed tiles to output array
        out_arr[0, y_s:y_e, x_s:x_e] = tile_arr

        result_count += 1

    pool.close()

    # assign output array to output raster
    lras.array = out_arr
    lras.shape = out_arr.shape

    Handler(outfile).file_delete()

    # write raster
    lras.write_to_file(outfile,
                       add_overview=True)

    Opt.cprint('Written {}'.format(outfile))
