from geosoup import Raster, Sublist, Opt, Vector
import numpy as np
import multiprocessing as mp
from sys import argv


def tile_process(args):
    """
    Method to provide coordinates of all the levels (max limit: nsamp)
    :return: dictionary
    """
    tile_id, levels, tie_pt, tile_arr, pixel_size, nsamp = args

    level_dict = dict()

    print('Processing {}'.format(tile_id))

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
        q_out.put(level_dict)


if __name__ == '__main__':

    # script, infile, outfile, nsamp, nprocs = argv

    # infile = "C:/temp/LC08_L1TP_128051_20180105_20180118_01_T1_sr_band4.tif"
    # outfile = "C:/temp/LC08_L1TP_128051_20180105_20180118_01_T1_sr_band4_v5.shp"

    infile = "C:/temp/LC081440532017062701T2-SC20180910215823/" \
             "LC08_L1GT_144053_20170627_20170714_01_T2_sr_band4.tif"
    outfile = "C:/temp/LC081440532017062701T2-SC20180910215823/" \
              "LC08_L1GT_144053_20170627_20170714_01_T2_sr_band4_v1.shp"

    nsamp = 100
    nprocs = 4

    levels = range(0, 100, 1)

    nprocs = int(nprocs)
    nsamp = int(nsamp)

    q_in = mp.Queue(maxsize=nprocs)
    q_out = mp.Manager().Queue()

    pool = mp.Pool(nprocs-1, initializer=tile_process, initargs=(q_in,))

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

    above_wkt = Vector.wkt_from_coords(above_coords,
                                       geom_type='polygon')
    above_geom = Vector.get_osgeo_geom(above_wkt)

    # -------------------------------------------------------------------------------------------------------

    raster = Raster(infile)
    raster.initialize(sensor=None)
    Opt.cprint(raster)

    pixel_size = (raster.transform[1], raster.transform[5])

    tile_count = 1
    tile_list = list()

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

        if tile_geom.Intersects(above_geom):

            Opt.cprint('Reading tile: {} of {}'.format(str(tile_count),
                                                       str(raster.ntiles)))

            # tile_list.append((tile_count, levels, tie_pt, tile_arr, pixel_size, nsamp))
            q_in.put((tile_count, levels, tie_pt, tile_arr, pixel_size, nsamp))


        else:
            Opt.cprint('Omitting tile: {} of {}'.format(str(tile_count),
                                                        str(raster.ntiles)))

        tile_count += 1

    # results = pool.map(tile_process, tile_list)


    pool.close()

    results = q_out.get()



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

