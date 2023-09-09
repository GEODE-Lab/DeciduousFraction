from geosoup import *
import numpy as np


if __name__ == '__main__':

    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/albedo_data/albedo_data_2000_2010_full_by_tc.csv"

    dicts = Handler(infile).read_from_csv(return_dicts=True)

    latlon = np.array(list((round(elem['x'], 5), round(elem['y'], 5)) for elem in dicts))
    print(latlon.shape)

    uniq_latlon = np.unique(ar=latlon,
                            axis=0)

    print(uniq_latlon)
    print(uniq_latlon.shape)

    outfilename = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/albedo_data/" \
                  "albedo_data_2000_2010_full_by_tc_loc.shp"

    attr = {'site_id': 'long',
            'latitude': 'float',
            'longitude': 'float'}

    wkt_list = list()
    attr_list = list()

    spref_str = '+proj=longlat +datum=WGS84'

    for i, row in enumerate(uniq_latlon.tolist()):

        print('Reading elem: {}'.format(str(i + 1)))

        elem = {'latitude': row[1], 'longitude': row[0], 'site_id': i}

        wkt_list.append(Vector.wkt_from_coords([row[0],
                                                row[1]]))

        attr_list.append(elem)

    vector = Vector.vector_from_string(wkt_list,spref_string=spref_str,
                                       spref_string_type='proj4',
                                       vector_type='point',
                                       attributes=attr_list,
                                       attribute_types=attr,
                                       verbose=True)

    print(vector)
    vector.write_vector(outfilename)
