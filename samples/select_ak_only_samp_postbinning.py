from geosoup import *
from osgeo import ogr


if __name__ == '__main__':
    bounds_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/STUDY_AREA/alaska_main.shp"

    '''
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_postbin_v8.shp"    
    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_postbin_v8_ak.shp"

    samp_vec = Vector(infile)
    print(samp_vec)

    bounds_vec = Vector(bounds_file)
    print(bounds_vec)

    ak_samp = samp_vec.get_intersecting_vector(bounds_vec)

    print(ak_samp)

    ak_samp.write_vector(outfile)
    '''
    bounds_vec = Vector(bounds_file)

    extracted_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
                     "gee_samp_extract_postbin_v30_all_2019_08_28T23_59_02_formatted_md.csv"

    outfilename = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" \
                     "gee_samp_extract_postbin_v30_all_2019_08_28T23_59_02_formatted_alaska.csv"

    out_list = list()

    for attr_dict in Handler(extracted_file).read_from_csv(return_dicts=True):

        attr_geom = ogr.CreateGeometryFromWkt(attr_dict['geom'])

        bounds_geom = ogr.CreateGeometryFromWkt(bounds_vec.wktlist[0])

        if bounds_geom.Intersects(attr_geom):
            out_list.append(attr_dict)

    print(len(out_list))

    Handler.write_to_csv(out_list, outfilename)
