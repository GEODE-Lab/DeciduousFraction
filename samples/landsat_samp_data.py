from geosoup import *
from osgeo import ogr

if __name__ == '__main__':

    folder = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/gee_extract/"
    samp_file = folder + "gee_samp_extract_short_v2019_01_21T01_49_06.csv"

    samp_data = Handler(filename=samp_file).read_from_csv(return_dicts=True)

    print(len(samp_data))
    print(samp_data[0])
    sites = list(set(list(samp['site']
                          for samp in samp_data)))

    print(len(sites))

    vec = Vector(in_memory=True,
                 name='gee_vec',
                 geom_type='point',
                 primary_key=None,
                 attr_def={'site': 'str',
                           'decid_frac': 'float',
                           'year': 'int'},
                 epsg=4326)

    print(vec)
    for site in sites:
        for samp in samp_data:
            if samp['site'] == site:
                feat_dict = dict()

                lat = samp['latitude']
                lon = samp['longitude']

                wkt = vec.wkt_from_coords((lon, lat),
                                          geom_type='point')

                geom = ogr.CreateGeometryFromWkt(wkt)

                feat_dict['site'] = site
                feat_dict['decid_frac'] = samp['decid_frac']
                feat_dict['year'] = samp['year']

                vec.add_feat(geom,
                             primary_key=None,
                             attr=feat_dict)

                break
    print(vec)
    vec.write_vector(folder + 'gee_ran_samp_vector.shp')





