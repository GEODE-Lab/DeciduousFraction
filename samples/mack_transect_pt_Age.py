from geosoup import *
import pandas as pd
import math
import numpy as np
from osgeo import ogr
import geopy.distance as dist


def convert_usable(elem):
    if not math.isnan(elem):
        try:
            return int(elem)
        except ValueError:
            try:
                return float(elem)
            except ValueError:
                try:
                    return str(elem)
                except:
                    return ''
    else:
        return ''


if __name__ == '__main__':

    age_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/raw/" +\
               "All_Stands_Transect_age.csv"

    samp_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects.shp"

    out_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects_pts_with_age.shp"
    log_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects_pts_with_age.log"

    age_dicts = Handler(age_file).read_from_csv(return_dicts=True)

    age_dict = dict()
    for temp_dict in age_dicts:

        site = temp_dict['Site'].strip()

        if site not in ('MATDEC', 'UBHW') and 'TKN' not in site:

            out_site = site[:2] + str(temp_dict['Tran'])

        elif 'TKN' in site:
            out_site = site

        else:
            out_site = site + str(temp_dict['Tran'])

        age_dict[out_site] = temp_dict['Age']

    mack_vec = Vector(samp_file)

    year_attr = ogr.FieldDefn('age', ogr.OFTInteger)
    year_attr.SetWidth(8)

    mack_vec.fields.append(year_attr)

    for attr in mack_vec.attributes:
        site = attr['site']
        if site in age_dict:
            age = age_dict[site]
        else:
            age = 0
        attr['age'] = age

    mack_vec.write_vector(out_file)
