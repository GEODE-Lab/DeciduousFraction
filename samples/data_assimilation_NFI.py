from geosoup import *
import multiprocessing as mp
import pandas as pd
import math
import time


if __name__ == '__main__':

    data_folder = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/CAN_NFI/Canada_NFI/From_Jackie_11_17_17/Originial_Canada_data/"

    csv_file = data_folder + 'NFI_plots_sample_site_data_July_26_2013_meta.csv'

    out_shp = data_folder + "NFI_plots_sample_site_data_July_26_2013_meta.shp"

    csv_data = pd.read_csv(csv_file)

    headers = list(csv_data)

    print(headers)

    meta_headers = ['plot', 'date',
                    'Lat_start', 'Long_start']

    site_list = csv_data.transpose().to_dict().values()

    nsites = len(site_list)

    print('\nSubmitting all sites for processing...\n')

    t0 = time.time()


    for i, site_dict in enumerate(site_list):

        # date = int('20' + site_dict['date'].split('-')[2])
        # site_dict['date'] = date
        # site_dict['plot'] = i+1

        print(site_dict)

    wkt_list = list()
    attribute_list = list()
    attribute_types = {'year': 'int',
                       'plot': 'str'}

    for i, data in enumerate(site_list):
        spref_str = '+proj=longlat +datum=WGS84'

        wkt = Vector.wkt_from_coords((data['Longitude'], data['Latitude']),
                                     geom_type='point')

        vector = Vector.vector_from_string(wkt,
                                           spref_string=spref_str,
                                           spref_string_type='proj4',
                                           vector_type=OGR_TYPE_DEF['point'])

        print('{}: {}'.format(str(i+1),
                              vector))

        wkt_list.append(vector.wktlist[0])

        attribute_list.append({'year': data['year'],
                               'plot': data['Plot']})

    print('\n\n')

    vector = Vector.vector_from_string(wkt_list,
                                       out_epsg=4326,
                                       attributes=attribute_list,
                                       attribute_types=attribute_types)

    print(vector)

    vector.write_to_file(outfile=out_shp)
