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

SAMP_PER_LEVEL = 500
SAMP_PER_TILE_PER_LEVEL = 100
TILE_SIZE = 1024
START_LEVEL = 0
END_LEVEL = 1000
STEP_LEVEL = 1


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

    """    
    infile: Input raster tif file
    outfile: Output shapefile
    nsamp: Number of samples per class to be extracted
    start_level and end level: Classification levels from where to extract the samples
    step_level: Increments between start_level and end_level
    nprocs: Number of processes to use for sample extraction    

    --------------------------------------------
    examples:
    infile = "D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw.tif"
    outfile = "D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_samp.shp"
    nsamp = 10
    start_level = 0
    end_level = 100
    step_level = 10
    nprocs = 1
    attr = 'tree_cover'
    """

    script, infile, outfile, nprocs, attr = argv

    # ------------------------------------------------------------------------------------------------------

    """
    replace with the following if no boundary needed:

    bound_coords = None 

    """

    bound_coords = [[-169.15996093750002, 59.81428022698168], [-166.34746093750002, 58.918656670521514],
                    [-164.06230468750002, 57.671671035154304], [-166.96269531250002, 55.74238728768902],
                    [-171.97246093750002, 55.09389730946914], [-171.62089843750002, 51.74383216286852],
                    [-166.52324218750002, 52.3921609944055], [-153.86699218750002, 55.29456733056491],
                    [-150.17558593750002, 58.09222100336203], [-144.90214843750002, 59.503499039497434],
                    [-141.38652343750002, 59.279744845369336], [-137.51933593750002, 57.95258384916048],
                    [-133.30058593750002, 52.6595247589874], [-129.96074218750002, 49.45719776213093],
                    [-125.7419921875, 47.29763431423617], [-119.5017578125, 48.12554644388249],
                    [-113.7009765625, 48.066845889196145], [-106.3181640625, 48.066845889196145],
                    [-98.5837890625, 47.8903420148682], [-91.90410156250002, 47.11851225665645],
                    [-86.80644531250002, 46.81863082379309], [-83.29082031250002, 44.60978736008787],
                    [-84.34550781250002, 41.26517132419739], [-80.30253906250002, 41.66035345299038],
                    [-77.13847656250002, 42.960199948729866], [-73.97441406250002, 44.3589686591478],
                    [-70.63457031250002, 44.3589686591478], [-68.87675781250002, 45.66373462232505],
                    [-66.94316406250002, 43.088706965961116], [-62.19707031250001, 43.088706965961116],
                    [-56.22050781250001, 43.85409660151231], [-50.06816406250001, 44.3589686591478],
                    [-51.82597656250001, 48.824730809629756], [-54.11113281250001, 53.13668636242484],
                    [-56.92363281250001, 54.79099337232696], [-59.64824218750001, 56.86380728954889],
                    [-62.10917968750001, 58.918656670521514], [-63.60332031250001, 60.68646587483211],
                    [-63.80107421875001, 60.900898697772135], [-64.35039062500002, 61.1138992429737],
                    [-69.88750000000002, 61.910356471023945], [-73.84257812500002, 62.967557980145465],
                    [-77.35820312500002, 63.91066619210739], [-79.37968750000002, 65.04651031522775],
                    [-78.76445312500002, 67.24855755395396], [-80.78593750000002, 69.57469743952159],
                    [-84.12578125000002, 69.99981753173893], [-87.81718750000002, 69.75794127868839],
                    [-90.10234375000002, 69.99981753173893], [-95.02421875, 69.26575776636543],
                    [-95.287890625, 68.5702995878685], [-97.13359375, 68.5702995878685],
                    [-101.440234375, 68.37680225566801], [-106.537890625, 69.01539454813513],
                    [-113.30546875, 68.05060589346397], [-114.8875, 69.01539454813513],
                    [-125.25859375, 70.85357417781019], [-130.79570312500002, 70.41644456151228],
                    [-144.68242187500002, 70.76690594146278], [-159.62382812500002, 71.58910348583488],
                    [-166.21562500000002, 69.63595450924004], [-168.67656250000002, 66.48903497336569],
                    [-167.44609375000002, 64.48448450226549], [-166.39140625000002, 61.61929667771038]]

    # -------------------------------------------------------------------------------------------------------
    levels = list(range(START_LEVEL, END_LEVEL, STEP_LEVEL)) + [END_LEVEL]

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
