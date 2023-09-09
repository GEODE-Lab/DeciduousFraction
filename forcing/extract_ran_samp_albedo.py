from geosoup import *
from eehelper import *
import numpy as np
import multiprocessing as mp
from sys import argv


CUTOFF = 0
OUT_BNAMES = ['treecover', 'decid', 'decidw', 'albedo_1', 'albedo_2', 'albedo_3', 'albedo_4']


def tile_process(args):

    if args is not None:
        tile_id, levels_, tie_pt, tile_arr, pixel_size_, bnames_, nsamp_ = args

        level_list_ = list()

        for level_ in levels_:
            xlocs, ylocs = np.where((tile_arr[1, :, :] >= CUTOFF) &
                                    (tile_arr[0, :, :] == level_))

            if len(xlocs) > 0 and len(ylocs) > 0:
                locs = np.array(zip(xlocs.tolist(), ylocs.tolist()))

                if locs.shape[0] > nsamp_:
                    locs = locs[np.random.choice(np.arange(0, locs.shape[0], 1), size=nsamp_, replace=False)]

                coords = Raster.get_coords(locs.tolist(),
                                           pixel_size=pixel_size_,
                                           tie_point=tie_pt,
                                           pixel_center=True)

                arr_ = np.apply_along_axis(lambda xx: tile_arr[:, xx[0], xx[1]], 1, locs)

                for ii, elem in enumerate(arr_.tolist()):

                    dict_ = dict()
                    for jj, bname in enumerate(OUT_BNAMES):
                        dict_[bname] = elem[jj]
                    dict_['x'] = coords[ii][0]
                    dict_['y'] = coords[ii][1]
                    dict_['year'] = int(bnames_[0].split('treecover')[1])

                    level_list_.append(dict_)

        if len(level_list_) > 0:
            return level_list_
        else:
            return []
    else:
        return []


def get_tile_data(raster_,
                  bound_wkt_=None,
                  levels_=None,
                  nsamp_=None,
                  bands_=(1,)):
    """
    Generator to yield a tuple of raster tile parameters for tile_process() function.
    To be used with imap or imap_nordered in multiprocessing
    :param raster_: Raster object
    :param bound_wkt_: Boundary WKT string
    :param levels_: Strata/pixel values used in sampling
    :param nsamp_: Number of samples
    :param bands_: Bands to extract
    :return: Tuple
    """

    bound_geom = Vector.get_osgeo_geom(bound_wkt_)

    pixel_size_ = (raster_.transform[1], raster_.transform[5])

    bnames_ = list(raster_.bnames[ii-1] for ii in bands_)

    tile_count = 1
    for tie_pt, tile_arr in raster_.get_next_tile(bands=bands_):

        if len(tile_arr.shape) > 2:

            tile_bands, tile_rows, tile_cols = tile_arr.shape

        else:
            tile_rows, tile_cols = tile_arr.shape

        tile_coords = [tie_pt,

                       [tie_pt[0] + raster_.metadict['xpixel'] * tile_cols, tie_pt[1]],

                       [tie_pt[0] + raster_.metadict['xpixel'] * tile_cols,
                        tie_pt[1] - raster_.metadict['ypixel'] * tile_rows],

                       [tie_pt[0], tie_pt[1] - raster_.metadict['ypixel'] * tile_rows],

                       tie_pt]

        tile_wkt = Vector.wkt_from_coords(tile_coords,
                                          geom_type='polygon')

        tile_geom = Vector.get_osgeo_geom(tile_wkt)

        if tile_geom.Intersects(bound_geom):

            Opt.cprint('Reading tile: {} of {}'.format(str(tile_count),
                                                       str(raster_.ntiles)))

            yield (tile_count,
                   levels_,
                   tie_pt,
                   tile_arr,
                   pixel_size_,
                   bnames_,
                   nsamp_)

        else:
            Opt.cprint('Omitting tile: {} of {}'.format(str(tile_count),
                                                        str(raster_.ntiles)))

        tile_count += 1


if __name__ == '__main__':

    # script, infile, outfile, nsamp, start_level, end_level, step_level = argv

    # -------------------------------------------------------------------------------------------------------

    infolder = "/scratch/rm885/gdrive/sync/decid/albedo_data_mean/"
    outfile = "/scratch/rm885/gdrive/sync/decid/albedo_data_mean/albedo_data_2000_2010_full_by_tc.csv"

    filelist = Handler(dirname=infolder).find_files(pattern='albedo_data_2000_2010')

    filelist = list(infolder + filename for filename in filelist if filename[-4:] == '.tif')

    for filename in filelist:
        Opt.cprint(filename)

    nsamp = 10  # samples per level per tile
    start_level = 0
    end_level = 100
    step_level = 1

    bands_list = [(13, 16, 19, 1, 2, 3, 4),  # TC, decid, decidw, albedo 1-4 for 2000, 2005, 2010
                  (14, 17, 20, 5, 6, 7, 8),
                  (15, 18, 21, 9, 10, 11, 12)]

    levels = range(start_level, end_level, step_level)

    nsamp = int(nsamp)

    results = list()

    for infile in filelist:

        raster = Raster(infile)
        raster.initialize(sensor=None)
        Opt.cprint(raster)

        for ib in range(len(raster.bnames)):
            Opt.cprint('{} : {}'.format(str(ib+1), raster.bnames[ib]))
        Opt.cprint('')

        bound_wkt = Vector.wkt_from_coords(raster.get_bounds(),
                                           geom_type='polygon')

        for bands in bands_list:
            Opt.cprint('Processing : {}'.format(' '.join(list(raster.bnames[ib_-1] for ib_ in bands))))
            for x in get_tile_data(raster, bound_wkt, levels, nsamp, bands):
                results += tile_process(x)

            print(len(results))

    for result in results[0:10]:
        print(result)

    Handler.write_to_csv(results, outfile)
    Opt.cprint('Written : {}'.format(outfile))




