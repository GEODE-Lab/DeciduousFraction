from geosoup import Raster, Sublist, Opt, Vector, Handler
import numpy as np
import multiprocessing as mp
from sys import argv


"""
This script extracts stratified random samples from single band rasters,  
sample location at pixel centers. The attribute name in the shapefile 
that represents the class value is 'value'. this script only extracts
sample locations with the class attribute. Boundary is specified separately in
this script. 
"""

SAMP_PER_LEVEL = 5000
SAMP_PER_TILE_PER_LEVEL = 200
TILE_SIZE = 1024


def tile_process(args):
    """
    Method to provide coordinates of all the levels (max limit: nsamp)
    :param args: levels, tie_pt, tile_arr, pixel_size, nsamp
    :return: dictionary
    """

    if args is not None:
        _tile_id, _levels, _tie_pt, _tile_arr, _pixel_size, _nsamp = args
        _level_dict = dict()

        for _level in _levels:
            _zlocs, _ylocs, _xlocs = np.where(_tile_arr == _level)
            if _xlocs.shape[0] > 0:
                _locs = Raster.get_coords(list(zip(list(_xlocs),
                                                   list(_ylocs))),
                                          pixel_size=_pixel_size,
                                          tie_point=_tie_pt,
                                          pixel_center=True)

                if len(_locs) > _nsamp:
                    _locs = Sublist(_locs).random_selection(num=_nsamp)
                    _level_dict[_level] = _locs
        if len(_level_dict) > 0:
            return _level_dict
    else:
        return


def get_tile_data(raster_obj,
                  bound_wkt_str=None,
                  strata_levels=None):
    """
    Generator to yield a tuple of raster tile parameters for tile_process() function.
    To be used with imap or imap_nordered in multiprocessing
    :param raster_obj: Raster object
    :param bound_wkt_str: Boundary WKT string
    :param strata_levels: Strata/pixel values used in sampling
    :return: Tuple
    """
    bound_geom = Vector.get_osgeo_geom(bound_wkt_str)
    bound_geom.CloseRings()

    tile_count = 1
    for tie_pt, tile_arr in raster_obj.get_next_tile():
        tile_bands, tile_rows, tile_cols = tile_arr.shape

        tile_coords = [tie_pt,
                       [tie_pt[0] + raster_obj.metadict['xpixel'] * tile_cols, tie_pt[1]],
                       [tie_pt[0] + raster_obj.metadict['xpixel'] * tile_cols,
                        tie_pt[1] - raster_obj.metadict['ypixel'] * tile_rows],
                       [tie_pt[0], tie_pt[1] - raster_obj.metadict['ypixel'] * tile_rows],
                       tie_pt]

        tile_wkt = Vector.wkt_from_coords(tile_coords,
                                          geom_type='polygon')
        tile_geom = Vector.get_osgeo_geom(tile_wkt)

        if tile_geom.Intersects(bound_geom):
            Opt.cprint('Reading tile: {} of {}'.format(str(tile_count),
                                                       str(raster_obj.ntiles)))
            yield (tile_count,
                   strata_levels,
                   tie_pt,
                   tile_arr,
                   pixel_size,
                   SAMP_PER_TILE_PER_LEVEL)
        else:
            Opt.cprint('Omitting tile: {} of {}'.format(str(tile_count),
                                                        str(raster_obj.ntiles)))
        tile_count += 1


if __name__ == '__main__':

    script, infile, outfile, nprocs, level, attr = argv

    # ------------------------------------------------------------------------------------------------------

    bound_coords = None

    # -------------------------------------------------------------------------------------------------------
    levels = [int(level)]

    nprocs = int(nprocs)

    out_attr_name = attr

    temp_file = outfile.replace('.shp', '_alldicts.csv')
    Handler(temp_file).file_delete()

    raster = Raster(infile)
    raster.initialize()
    raster.make_tile_grid(tile_xsize=TILE_SIZE,
                          tile_ysize=TILE_SIZE)

    Opt.cprint(raster)

    if bound_coords is not None:
        bound_wkt = Vector.wkt_from_coords(bound_coords,
                                           geom_type='polygon')
    else:
        bound_wkt = Vector.wkt_from_coords(raster.get_bounds(),
                                           geom_type='polygon')

    pixel_size = (raster.transform[1], raster.transform[5])

    result_dicts = []

    pool = mp.Pool(nprocs-1)
    for result in pool.imap_unordered(tile_process,
                                      get_tile_data(raster, bound_wkt, levels)):

        if result is not None:
            if not isinstance(result, list):
                result = [result]

            if Handler(temp_file).file_exists():
                Handler.write_to_csv(result, outfile=temp_file, append=True)
            else:
                Handler.write_to_csv(result, outfile=temp_file, append=False)

            result_dicts += result

    pool.close()

    Opt.cprint('All tiles completed - Recording levels')

    out_coord_list = list()
    out_attr_list = list()
    level_dict = dict()

    for level in levels:
        Opt.cprint('Recording level: {}'.format(str(level)))

        for elem_dict in result_dicts:
            if level in elem_dict:
                if level in level_dict:
                    level_dict[level] += elem_dict[level]
                else:
                    level_dict[level] = elem_dict[level]

    for level in levels:
        if level in level_dict:
            loc = level_dict[level]

            if len(loc) > 0:
                out_loc = Sublist(loc).random_selection(SAMP_PER_LEVEL)

                out_coord_list += out_loc
                out_attr_list += list({out_attr_name: level,
                                       'longitude': loc_tuple[0],
                                       'latitude': loc_tuple[1]} for loc_tuple in out_loc)

    vec_wkts = list(Vector.wkt_from_coords(coords) for coords in out_coord_list)

    vec = Vector(in_memory=True,
                 geom_type='point',
                 primary_key=None,
                 spref_str=raster.crs_string,
                 attr_def={out_attr_name: 'str'})

    for i, wkt in enumerate(vec_wkts):
        vec.add_feat(Vector.get_osgeo_geom(wkt),
                     primary_key=None,
                     attr=out_attr_list[i])

    vec.write_vector(outfile)

    Opt.cprint(vec)
    Opt.cprint('Written : {}'.format(outfile))
