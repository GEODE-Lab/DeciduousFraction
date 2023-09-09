from geosoup import *
import numpy as np
import multiprocessing as mp
from sys import argv


def tile_process(args):
    """
    Method to provide coordinates of all the levels (max limit: nsamp)
    :param args: levels, tie_pt, tile_arr, pixel_size, nsamp
    :return: dictionary
    """

    if args is not None:
        tile_id, levels, tie_pt, tile_arr, pixel_size, nsamp = args

        level_dict = dict()

        for level in levels:
            xlocs, ylocs = np.where(tile_arr == level)

            if len(xlocs) > 0 and len(ylocs) > 0:
                locs = Raster.get_coords(zip(list(ylocs),
                                             list(xlocs)),
                                         pixel_size=pixel_size,
                                         tie_point=tie_pt,
                                         pixel_center=True)
                if len(locs) > nsamp:
                    locs = Sublist(locs).random_selection(num=nsamp)
                    level_dict[level] = locs

        if len(level_dict) > 0:
            return level_dict
    else:
        return


def get_tile_data(raster,
                  bound_wkt,
                  levels):
    """
    Generator to yield a tuple of raster tile parameters for tile_process() function.
    To be used with imap or imap_nordered in multiprocessing
    :param raster: Raster object
    :param bound_wkt: Boundary WKT string
    :param levels: Strata/pixel values used in sampling
    :return: Tuple
    """

    bound_geom = Vector.get_osgeo_geom(bound_wkt)

    pixel_size = (raster.transform[1], raster.transform[5])

    tile_count = 1
    for tie_pt, tile_arr in raster.get_next_tile():

        tile_rows, tile_cols = tile_arr.shape

        tile_coords = [tie_pt,

                       [tie_pt[0]+raster.metadict['xpixel']*tile_cols, tie_pt[1]],

                       [tie_pt[0]+raster.metadict['xpixel']*tile_cols, tie_pt[1]-raster.metadict['ypixel']*tile_rows],

                       [tie_pt[0], tie_pt[1]-raster.metadict['ypixel']*tile_rows],

                       tie_pt]

        tile_wkt = Vector.wkt_from_coords(tile_coords,
                                          geom_type='polygon')

        tile_geom = Vector.get_osgeo_geom(tile_wkt)

        if tile_geom.Intersects(bound_geom):

            Opt.cprint('Reading tile: {} of {}'.format(str(tile_count),
                                                       str(raster.ntiles)))

            yield (tile_count,
                   levels,
                   tie_pt,
                   tile_arr,
                   pixel_size,
                   nsamp)

        else:
            Opt.cprint('Omitting tile: {} of {}'.format(str(tile_count),
                                                        str(raster.ntiles)))

        tile_count += 1


if __name__ == '__main__':

    # script, infile, outfile, nsamp, nprocs = argv

    # infile = "C:/temp/LC08_L1TP_128051_20180105_20180118_01_T1_sr_band4.tif"
    # outfile = "C:/temp/LC08_L1TP_128051_20180105_20180118_01_T1_sr_band4_v4.shp"

    infile = "C:/temp/LC081440532017062701T2-SC20180910215823/" \
             "LC08_L1GT_144053_20170627_20170714_01_T2_sr_band4.tif"
    outfile = "C:/temp/LC081440532017062701T2-SC20180910215823/" \
              "LC08_L1GT_144053_20170627_20170714_01_T2_sr_band4_v4.shp"

    temp_file = "C:/temp/LC081440532017062701T2-SC20180910215823/" \
              "LC08_L1GT_144053_20170627_20170714_01_T2_sr_band4_v4.txt"

    with open(temp_file, 'w') as tf:
        tf.write('dictionaries\n')

    nsamp = 2
    nprocs = 4
    chunksize = 50

    levels = range(5000, 9000, 1)

    nprocs = int(nprocs)
    nsamp = int(nsamp)

    pool = mp.Pool(nprocs)

    out_attr_name = 'tc_value'

    # boundary of the region
    # above_coords = [[603145.0, 1771195.0],
    #                 [998128.0, 1771195.0],
    #                 [998128.0, 1171195.0],
    #                 [603145.0, 1171195.0],
    #                 [603145.0, 1771195.0]]

    above_coords = [[563129, 1263106],
                    [863129, 1263106],
                    [863129, 976106],
                    [563129, 976106],
                    [563129, 1263106]]

    # above_coords = [[-168.83884, 66.60503], [-168.66305, 64.72256], [-166.11423, 63.29787], [-168.83884, 60.31062],
    #                  [-166.02634, 56.92698], [-166.64157, 54.70557], [-164.84625, 54.05535], [-157.94684, 54.69525],
    #                  [-153.64020, 56.21509], [-151.17926, 57.48851], [-149.64118, 58.87838], [-147.67361, 61.37118],
    #                  [-142.04861, 59.70736], [-135.67654, 58.69490], [-130.48731, 55.73262], [-124.82205, 50.42354],
    #                  [-113.70389, 51.06312], [-112.07791, 53.29901], [-109.00174, 53.03557], [-105.16527, 52.53873],
    #                  [-101.13553, 50.36751], [-98.007415, 49.77869], [-96.880859, 48.80976], [-94.983189, 48.94521],
    #                  [-94.851353, 52.79709], [-88.238500, 56.92737], [-91.862463, 57.81702], [-93.775610, 59.60700],
    #                  [-92.984594, 61.25472], [-87.315649, 64.30688], [-80.504125, 66.77919], [-79.976781, 68.59675],
    #                  [-81.426977, 69.84364], [-84.547094, 70.00956], [-87.447485, 69.93430], [-91.094946, 70.77629],
    #                  [-91.798071, 72.17192], [-89.688696, 73.86475], [-89.600805, 74.33426], [-92.940649, 74.61654],
    #                  [-93.380102, 75.58784], [-94.874242, 75.69681], [-95.137914, 75.86949], [-96.719946, 76.56045],
    #                  [-97.598852, 76.81343], [-97.618407, 77.32284], [-99.552001, 78.91297], [-103.94653, 79.75829],
    #                  [-113.79028, 78.81110], [-124.33715, 76.52777], [-128.02856, 71.03224], [-136.99340, 69.67342],
    #                  [-149.64965, 71.03224], [-158.08715, 71.65080], [-167.93090, 69.24910], [-168.83884, 66.60503]]

    above_wkt = Vector.wkt_from_coords(above_coords,
                                       geom_type='polygon')

    # -------------------------------------------------------------------------------------------------------

    raster = Raster(infile)
    raster.initialize(sensor=None)
    Opt.cprint(raster)

    results = list()
    for result in pool.imap_unordered(tile_process,
                                      get_tile_data(raster, above_wkt, levels),
                                      chunksize=chunksize):
        results.append(result)
        with open(temp_file, 'a') as tf:
            tf.write(str(result) + '\n')

    result_dicts = list()
    for result in results:
        if result is not None:
            result_dicts.append(result)

    print('All tiles completed - Recording levels')

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
                out_loc = Sublist(loc).random_selection(nsamp)

                out_coord_list += out_loc
                out_attr_list += list({out_attr_name: level} for _ in range(0, len(out_loc)))

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

    Opt.cprint(vec)

    vec.write_vector(outfile)

    Opt.cprint('Written : {}'.format(outfile))

