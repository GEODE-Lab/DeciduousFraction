from modules import *
import multiprocessing as mp
from osgeo import gdal, gdal_array
import numpy as np


def _tile_process_(args):

    _tie_pt, _tile_coords, _tile_arr, _nodatavalue, _composite_type = args
    _x, _y, _cols, _rows = _tile_coords

    if _composite_type == 'mean':
        _temp_arr = np.apply_along_axis(lambda x: np.mean(x[x != _nodatavalue]) if (x[x != _nodatavalue]).shape[0] > 0
                                        else _nodatavalue, 0, _tile_arr)
    elif _composite_type == 'median':
        _temp_arr = np.apply_along_axis(lambda x: np.median(x[x != _nodatavalue]) if (x[x != _nodatavalue]).shape[0] > 0
                                        else _nodatavalue, 0, _tile_arr)
    elif 'pctl' in _composite_type:
        pctl = int(_composite_type.split('_')[1])
        _temp_arr = np.apply_along_axis(lambda x: np.percentile(x[x != _nodatavalue], pctl) if (x[x != _nodatavalue]).shape[0] > 0
                                        else _nodatavalue, 0, _tile_arr)
    else:
        _temp_arr = None

    return _y, (_y + _rows), _x, (_x + _cols), _temp_arr


def _get_tile_data_(_layerstack_vrt, _band_order, _tile_size, _composite_type):

    _lras = Raster('_tmp_layerstack')
    _lras.datasource = _layerstack_vrt
    _lras.initialize()
    _lras.make_tile_grid(*_tile_size)

    tile_count = 0
    for _tie_pt, _tile_arr in _lras.get_next_tile(bands=_band_order):

        _tile_coords = _lras.tile_grid[tile_count]['block_coords']

        yield _tie_pt, _tile_coords, _tile_arr, _lras.nodatavalue, _composite_type
        tile_count += 1


if __name__ == '__main__':

    nthreads = 6
    thread_offset = 1
    file_folder = 'c:/temp/albedo'
    tile_size = (1024, 1024)
    composite_type = 'median'

    outfile = file_folder + '/layerstack1.tif'

    filelist = Handler(dirname=file_folder).find_all('*.tif')
    mraster = MultiRaster(filelist=filelist)

    print(mraster)

    ls_vrt = mraster.layerstack(return_vrt=True)
    lras = Raster('tmp_layerstack')
    lras.datasource = ls_vrt
    lras.initialize()

    print(lras)

    band_order = list(range(1, len(mraster.rasters) + 1))

    out_arr = np.zeros((lras.shape[1], lras.shape[2]),
                       dtype=gdal_array.GDALTypeCodeToNumericTypeCode(lras.dtype))

    if nthreads is None:
        nthreads = mp.cpu_count() - thread_offset
    elif nthreads > (mp.cpu_count() - 1):
        nthreads = mp.cpu_count() - 1
    elif nthreads < 1:
        nthreads = 1
    pool = mp.Pool(processes=nthreads)

    result_count = 0
    for result in pool.imap_unordered(_tile_process_,
                                      _get_tile_data_(ls_vrt, band_order, tile_size, composite_type)):
        y_s, y_e, x_s, x_e, temp_arr = result
        print(result_count + 1, y_s, y_e, x_s, x_e)
        out_arr[y_s:y_e, x_s:x_e] = temp_arr
        result_count += 1

    lras.array = out_arr
    lras.write_to_file(outfile)

    print(outfile)

