from geosoup import Vector, Handler
import numpy as np

if __name__ == '__main__':

    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1.shp"
    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1_uniq.shp"

    vec = Vector(infile)

    print(vec)
    print(vec.wktlist[0])

    lonlat = np.array(list([float(num) for
                           num in elem.replace('POINT (', '').replace(')', '').split(' ')] for
                           elem in vec.wktlist))

    uniq, indices, = np.unique(ar=lonlat,
                               axis=0,
                               return_index=True)

    print(uniq.shape)
    print(indices.shape)

    attributes = list({'site': vec.attributes[i]['site'],
                       'latitude': vec.attributes[i]['Latitude'],
                       'longitude': vec.attributes[i]['Longitude']} for i in indices)

    uniq_coord_list = uniq.tolist()
    uniq_coord_float_list = []
    for elem in uniq_coord_list:
        try:
            uniq_coord_float_list.append((float(elem[0]), float(elem[1])))
        except Exception as e:
            print(e)

    wkt_strings = list(Vector.wkt_from_coords(elem, 'point') for elem in uniq_coord_float_list)

    vec = Vector.vector_from_string(wkt_strings,
                                    out_epsg=4326,
                                    primary_key=None,
                                    attributes=attributes,
                                    attribute_types={'site': 'str', 'latitude': 'float', 'longitude': 'float'})

    vec.write_vector(outfile)
