from geosoup import Vector, Handler
import pandas as pd
import json
from osgeo import ogr
import numpy as np


if __name__ == '__main__':

    infilename = "C:/shared/projects/NAU/landsat_deciduous/data/samples/CAN_PSP\PSP_data\All_sites_101218.csv"
    outfilename = infilename.replace('.csv', '.shp')

    attrs = {'site': 'string',
             'Longitude': 'float',
             'Latitude': 'float'}

    samp_data = Handler(infilename).read_from_csv(return_dicts=True)

    spref_str = '+proj=longlat +datum=WGS84'

    vector = Vector(filename=outfilename,
                    name='psp_all_sites_101218',
                    spref_str=spref_str,
                    spref_str_type='proj4',
                    geom_type='point',
                    in_memory=True,
                    attr_def=attrs)

    for samp in samp_data:
        if samp['Longitude'] != 'NA' or samp['Latitude'] != 'NA':
            vector.add_feat(Vector.get_osgeo_geom(Vector.wkt_from_coords([float(samp['Longitude']),
                                                                          float(samp['Latitude'])])),
                            attr={attr: samp[attr] for attr in list(attrs)})

    print(vector)
    vector.write_vector(outfilename)


    infilename = "C:/shared/projects/NAU/mack/Site_locations_MD_chrono_JFSP_corrected.csv"

    outfilename = infilename.replace('.csv', '.shp')

    attrs = {'project': 'string',
             'site': 'string',
             'tran': 'string',
             'lat': 'float',
             'lon': 'float'}

    samp_data = Handler(infilename).read_from_csv(return_dicts=True)

    spref_str = '+proj=longlat +datum=WGS84'

    vector = Vector(filename=outfilename,
                    name='Site_locations_MD_chrono_JFSP',
                    spref_str=spref_str,
                    spref_str_type='proj4',
                    geom_type='point',
                    in_memory=True,
                    attr_def=attrs)

    for samp in samp_data:
        if samp['lon'] != 'NA' or samp['lat'] != 'NA':
            vector.add_feat(Vector.get_osgeo_geom(Vector.wkt_from_coords([float(samp['lon']),
                                                                          float(samp['lat'])])),
                            attr={attr: samp[attr] for attr in list(attrs)})

    print(vector)
    vector.write_vector(outfilename)




