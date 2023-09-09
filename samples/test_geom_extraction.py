from geosoup import MultiRaster
from geosoup import Raster, Opt, Vector, Handler
import multiprocessing as mp
from sys import argv
from copy import deepcopy
'''

ras = Raster("D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m.tif")
ras.initialize()
print(ras)
mras=MultiRaster(filelist=["D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m.tif",
                           "D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m.tif",
                           "D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m.tif"])

#lmras=mras.layerstack(outfile='D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m_3band.tif')
#outlmras=Raster('D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m_3band.tif')
#outlmras.datasource=lmras
#outlmras.initialize()

#outlmras.write_to_file(compress='lzw')

#res=mras.layerstack(outfile='D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m_3band.tif',
#                    return_vrt=False,
#                    compress='lzw')





ras=Raster('D:/temp/tree_cover/hansen_tc_mosaic_2010_byte_lzw_250m_3band.tif')
ras.initialize()
ras.make_tile_grid(10240, 10240)
for tile in ras.tile_grid:
    print(tile)
ras.make_tiles(10240, 10240, "D:/temp/tree_cover/test_tiles", add_overview=True)
'''


'''
This script extracts sample vectors from raster tiles
in a folder. The name of each file is added to the csv as an attribute.
'''


def find_search_string(year):
    """
    Method to return the appropriate string to search for in the tile name
    based on the year of sample
    :param year: Year of sample
    :return: string or None
    """
    str_dict = {
        '_1992-': (1987, 1997),
        '_2000-': (1998, 2002),
        '_2005-': (2003, 2007),
        '_2010-': (2008, 2012),
        '_2015-': (2013, 2018)
    }

    for k, v in str_dict.items():
        if v[0] <= year <= v[1]:
            return k
    return


def find_intersection(name_tuple):
    """
    Method to identify geometries that intersect with the tile
    :param name_tuple: tuple containing - tile filename, vector filename, bounds wkt string
    :return: list or None
    """
    tile_filename, vector_filename, bounds_wkt = name_tuple

    bounds_geom = Vector.get_osgeo_geom(bound_wkt)

    all_samp_vec = Vector(vector_filename)

    temp_ras = Raster(tile_filename)
    temp_bounds = temp_ras.get_bounds()
    temp_wkt = Vector.wkt_from_coords(temp_bounds, geom_type='polygon')
    temp_geom = Vector.get_osgeo_geom(temp_wkt)
    temp_geom.CloseRings()

    if temp_geom.Intersects(bounds_geom):
        intrsct_list = []

        for samp_indx in range(all_samp_vec.nfeat):

            samp_geom = Vector.get_osgeo_geom(all_samp_vec.wktlist[samp_indx])

            samp_year = all_samp_vec.attributes[samp_indx]['year']
            samp_year_search_str = find_search_string(samp_year)

            if (samp_year_search_str is not None) and \
                    (samp_year_search_str in Handler(tile_filename).basename):
                if temp_geom.Intersects(samp_geom):
                    attr = all_samp_vec.attributes[samp_indx]
                    attr.update({'geom': all_samp_vec.wktlist[samp_indx]})
                    intrsct_list.append(attr)

        if len(intrsct_list) > 0:
            return {tile_filename: intrsct_list}


def tile_process(tile_info):
    """
    Method to provide coordinates of all the levels (max limit: nsamp)
    :param tile_info: Dictionary of the form : {tile_raster_path: [list of sample dicts]}
    :return: dictionary
    """

    tile_filename, geom_list = list(tile_info.items())[0]

    tile_ras = Raster(tile_filename)
    tile_ras.initialize()
    tile_bnames = tile_ras.bnames

    geom_wkt_list = [geom_dict['geom'] for geom_dict in geom_list]

    # dict of extracted values where keys are IDs
    extract_list = tile_ras.extract_geom(geom_wkt_list,
                                         pass_pixel_coords=True)

    print('Extract list is {} long from tile {}'.format(str(len(extract_list)), tile_name))

    out_list = []
    for samp_indx, samp_dict in enumerate(extract_list):
        if len(samp_dict['values']) > 0 and len(samp_dict['values'][0]) > 0:

            temp_dict = deepcopy(geom_list[samp_indx])
            samp_dict_with_bands = dict(zip(tile_bnames, samp_dict['values'][0]))
            temp_dict.update(samp_dict_with_bands)
            temp_dict.update({'filename': Handler(tile_filename).basename})
            out_list.append(temp_dict)

    print('Out list is {} long from tile {}'.format(str(len(out_list)), tile_name))

    if len(out_list) > 0:
        return out_list
    else:
        return


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
    """
    raster_filefolder = "D:/temp/tree_cover/test_tiles/"
    samp_shpfile = "D:/temp/tree_cover/all_samp_post_v9.shp"
    extract_file = "D:/temp/tree_cover/all_samp_post_v9_out.csv"
    # nprocs = 2

    # replace bound_coords with the following if no boundary needed:
    # bound_coords = None

    # script, raster_filefolder, samp_shpfile, extract_file, nprocs = argv
    # ------------------------------------------------------------------------------------------------------

    bound_coords = [[-165.90800781250002, 67.14281541784403], [-167.31425781250002, 66.93710574593051],
                    [-169.07207031250002, 64.40470750992607], [-167.66582031250002, 62.35795332711261],
                    [-164.32597656250002, 57.33622778331068], [-165.20488281250002, 53.96666515623615],
                    [-158.34941406250002, 53.550992243482334], [-148.85722656250002, 58.731933742605904],
                    [-142.35332031250002, 58.731933742605904], [-136.48051644679492, 56.74119582563745],
                    [-133.91582031250002, 54.48048639601067], [-129.69707031250002, 52.06354722436047],
                    [-124.7751953125, 48.93431376306091], [-116.36726129245775, 48.724285986503354],
                    [-107.9001953125, 48.47027580249403], [-94.5408203125, 47.17206587233248],
                    [-88.03968465179696, 46.4184607772877], [-83.99394531250002, 43.46597166198637],
                    [-82.93925781250002, 40.192611128052754], [-74.32597656250002, 43.33825798989073],
                    [-67.64628906250002, 42.17673121632382], [-58.32988281250001, 44.603271845712804],
                    [-53.23222656250001, 45.59587375476319], [-49.36503906250001, 49.39407810907766],
                    [-52.35332031250001, 54.27572510460249], [-54.63847656250001, 56.76258052056773],
                    [-61.66972656250001, 57.901054192561524], [-65.00957031250002, 57.901054192561524],
                    [-69.22832031250002, 57.24123463705217], [-80.82988281250002, 55.08866006127723],
                    [-88.74003906250002, 58.087383512987316], [-97.1775390625, 59.89795706904842],
                    [-105.7908203125, 62.194403351036605], [-116.5134765625, 65.5204149882913],
                    [-126.5330078125, 68.59904919862765], [-134.44316406250002, 69.54080414556246],
                    [-140.59550781250002, 69.16895364821778], [-144.81425781250002, 68.40579909921763],
                    [-151.66972656250002, 67.81603533682497], [-158.70097656250002, 67.27898929955994],
                    [-164.32597656250002, 67.00586941496265], [-165.90800781250002, 67.14281541784403]]

    # -------------------------------------------------------------------------------------------------------

    bound_wkt = Vector.wkt_from_coords(bound_coords, geom_type='polygon')

    tile_list = Handler(raster_filefolder).find_all(pattern='*.tif')

    Opt.cprint('Found {} tiles'.format(str(len(tile_list))))
    Opt.cprint('---------------------------')

    tile_preprocess_list = [(tile_name, samp_shpfile, bound_wkt) for tile_name in tile_list]

    # nprocs = int(nprocs)
    # pool = mp.Pool(nprocs)

    tile_samp_list = []
    for tile_name in tile_preprocess_list:
        print(tile_name)

    for tile_tuple in tile_preprocess_list:
        result = find_intersection(tile_tuple)

        if result is not None:
            print(result)
            tile_name, sample_locs = list(result.items())[0]
            print('Number of samples: {}'.format(str(len(sample_locs))))
            tile_samp_list.append(result)

    Opt.cprint('Number of tiles to extract from: {}'.format(str(len(tile_samp_list))))
    Opt.cprint('---------------------------')

    for tile_samp in tile_samp_list:
        Opt.cprint(tile_samp)
    Opt.cprint('---------------------------')


    # pool = mp.Pool(nprocs)

    Handler(extract_file).file_delete()

    result_dicts = []
    for tile_samp in tile_samp_list:

        results = tile_process(tile_samp)

        print('results is {} long from tile {}'.format(str(len(results)), list(tile_samp.items())[0][0]))

        if results is not None:
            result_dicts += results

            if Handler(extract_file).file_exists():
                Handler.write_to_csv(results, outfile=extract_file, append=True, header=False)
            else:
                Handler.write_to_csv(results, outfile=extract_file, append=False, header=True)

            Opt.cprint('Extracted {} samples'.format(str(len(results))))

    Opt.cprint('---------------------------')
    for result in result_dicts:
        Opt.cprint(result)
    Opt.cprint('---------------------------')
    Opt.cprint('All tiles completed - writing csv')

    extract_file2 = Handler(extract_file).add_to_filename('_2')

    Handler.write_to_csv(result_dicts, outfile=extract_file2)

    Opt.cprint('Written : {}'.format(extract_file))

