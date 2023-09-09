from geosoup import Vector, Handler


"""
Script to convert csv format deciduous fraction locations and values to shapefile with attributes
"""


if __name__ == '__main__':

    infilename = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1.csv"

    outfilename = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1.shp"

    attr = {'site': 'str',
            'Latitude': 'float',
            'Longitude': 'float',
            'decid_frac': 'float',
            'year': 'int'}

    samp_data = Handler(infilename).read_from_csv(return_dicts=True)

    wkt_list = list()
    attr_list = list()

    spref_str = '+proj=longlat +datum=WGS84'

    count = 0
    for row in samp_data:
        print('Reading elem: {}'.format(str(count + 1)))

        if (-155.0 <= row['Longitude'] <= -50.0) and (40.0 <= row['Latitude'] <= 70.0):

            wkt_list.append(Vector.wkt_from_coords([row['Longitude'], row['Latitude']], geom_type='point'))
            attr_list.append(row)

            count += 1

    vector = Vector.vector_from_string(wkt_list,
                                       spref_string=spref_str,
                                       spref_string_type='proj4',
                                       vector_type='point',
                                       attributes=attr_list,
                                       attribute_types=attr,
                                       verbose=False)

    print(vector)

    vector.write_vector(outfilename)
