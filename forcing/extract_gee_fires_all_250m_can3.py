import ee
import os
import sys
import time
import math
import json
import datetime
import warnings
import traceback
from geosoup import *
from eehelper import *
import numpy as np


if __name__ == '__main__':

    ee.Initialize()

    folder = "D:/shared/Dropbox/projects/NAU/landsat_deciduous/data/"

    OUTFILE = folder + 'SAMPLES/fires/can_fire_multi_s1_extract_v{}.csv'.format(datetime.datetime.now().isoformat()
                                          .split('.')[0].replace('-', '_').replace(':', '_'))

    logfile = OUTFILE.split('.csv')[0] + '.log'

    log = Logger('SAMP',
                 filename=logfile,
                 stream=True)

    scale = 250
    cutoff = 4000
    fire_year_limit = 1970

    log.lprint('Outfile: {}'.format(OUTFILE))
    log.lprint('Logfile: {}'.format(logfile))

    # boundary of the region
    above_coords = [[-168.83884, 66.60503], [-168.66305, 64.72256], [-166.11423, 63.29787], [-168.83884, 60.31062],
                     [-166.02634, 56.92698], [-166.64157, 54.70557], [-164.84625, 54.05535], [-157.94684, 54.69525],
                     [-153.64020, 56.21509], [-151.17926, 57.48851], [-149.64118, 58.87838], [-147.67361, 61.37118],
                     [-142.04861, 59.70736], [-135.67654, 58.69490], [-130.48731, 55.73262], [-124.82205, 50.42354],
                     [-113.70389, 51.06312], [-112.07791, 53.29901], [-109.00174, 53.03557], [-105.16527, 52.53873],
                     [-101.13553, 50.36751], [-98.007415, 49.77869], [-96.880859, 48.80976], [-94.983189, 48.94521],
                     [-94.851353, 52.79709], [-88.238500, 56.92737], [-91.862463, 57.81702], [-93.775610, 59.60700],
                     [-92.984594, 61.25472], [-87.315649, 64.30688], [-80.504125, 66.77919], [-79.976781, 68.59675],
                     [-81.426977, 69.84364], [-84.547094, 70.00956], [-87.447485, 69.93430], [-91.094946, 70.77629],
                     [-91.798071, 72.17192], [-89.688696, 73.86475], [-89.600805, 74.33426], [-92.940649, 74.61654],
                     [-93.380102, 75.58784], [-94.874242, 75.69681], [-95.137914, 75.86949], [-96.719946, 76.56045],
                     [-97.598852, 76.81343], [-97.618407, 77.32284], [-99.552001, 78.91297], [-103.94653, 79.75829],
                     [-113.79028, 78.81110], [-124.33715, 76.52777], [-128.02856, 71.03224], [-136.99340, 69.67342],
                     [-149.64965, 71.03224], [-158.08715, 71.65080], [-167.93090, 69.24910]]

    boundary_geom = ee.Geometry.Polygon(above_coords)

    data_cube = ee.Image('users/masseyr44/all_product_stack_250m')
    data_cube = data_cube.addBands(ee.Image.pixelLonLat())

    ak_fire = ee.FeatureCollection('users/masseyr44/shapefiles/ak_fire_multi')

    ak_feat_size = ak_fire.size().getInfo()

    log.lprint('AK FIRE shpfile size: {}'.format(ak_feat_size))

    feat_prop_dict = {'CFS_REF_ID': 'FIREID',
                      'FIREID': 'FIREID',
                      'YEAR': 'YEAR',
                      'SIZE_HA': 'SIZE_HA',
                      'FireYear': 'YEAR'}

    bands = ['tc1992','tc2000','tc2005','tc2010','tc2015','tc1992u','tc2000u','tc2005u','tc2010u','tc2015u',
             'decid1992','decid2000','decid2005','decid2010','decid2015','decid1992u','decid2000u','decid2005u',
             'decid2010u','decid2015u']

    data_cube_meta = data_cube.getInfo()

    bnames = list(str(meta['id']) for meta in data_cube_meta['bands'])

    log.lprint('Band_names: {}'.format(str(bnames)))

    ak_fire = ak_fire.toList(ak_feat_size)

    for i in range(ak_feat_size):
        time1 = datetime.datetime.now()

        temp_data = data_cube.sampleRegions(ee.FeatureCollection([ak_fire.get(i)]), None, 250)
        temp_data = temp_data.toList(temp_data.size())
        try:
            temp_list = temp_data.getInfo()
        except Exception as e:
            temp_list = list()
            if 'Collection query aborted after accumulating over 5000 elements' in e.args[0]:

                n_temp_feat = temp_data.size().getInfo()
                if n_temp_feat > cutoff:

                    feat_slice_list = list((i * cutoff, (i + 1) * cutoff) for i in range(n_temp_feat // cutoff))

                    if n_temp_feat % cutoff > 0:
                        feat_slice_list += [(feat_slice_list[-1][1], feat_slice_list[-1][1] + (n_temp_feat % cutoff))]

                    for feat_slice in feat_slice_list:
                        temp_list += temp_data.slice(feat_slice[0], feat_slice[1]).getInfo()

        time2 = datetime.datetime.now()

        log.lprint('Time taken for {} pixels, '.format(str(len(temp_list))) +
                   ' ({ii} of {nn} fires): {t} seconds'.format(ii=str(i + 1),
                                                               nn=str(ak_feat_size),
                                                               t=str(round(
                                                                   (time2 - time1).total_seconds(), 1))))

        out_list = list()
        for feat in temp_list:
            out_dict = dict()
            for key, val in feat['properties'].items():
                if key in feat_prop_dict:
                    out_dict[feat_prop_dict[key]] = feat['properties'][key]
                elif key in bands:
                    out_dict[key] = feat['properties'][key]
                else:
                    pass

            out_list.append(out_dict)

        if len(out_list) > 0:

            # all extracted dictionaries to file
            if i == 0:
                Handler.write_to_csv(out_list,
                                     header=True,
                                     append=False,
                                     outfile=OUTFILE)

            else:
                Handler.write_to_csv(out_list,
                                     header=False,
                                     append=True,
                                     outfile=OUTFILE)

    can_fire = ee.FeatureCollection('users/masseyr44/shapefiles/can_fire_multi_s1')

    can_feat_size = can_fire.size().getInfo()

    log.lprint('CAN FIRE shpfile size: {}'.format(can_feat_size))

    feat_prop_dict = {'CFS_REF_ID': 'FIREID',
                      'FIREID': 'FIREID',
                      'YEAR': 'YEAR',
                      'SIZE_HA': 'SIZE_HA',
                      'FireYear': 'YEAR'}

    bands = ['tc1992','tc2000','tc2005','tc2010','tc2015','tc1992u','tc2000u','tc2005u','tc2010u','tc2015u',
             'decid1992','decid2000','decid2005','decid2010','decid2015','decid1992u','decid2000u','decid2005u',
             'decid2010u','decid2015u','latitude','longitude']

    data_cube_meta = data_cube.getInfo()

    bnames = list(str(meta['id']) for meta in data_cube_meta['bands'])

    log.lprint('Band_names: {}'.format(str(bnames)))

    can_fire = can_fire.toList(can_feat_size)

    for i in range(can_feat_size):
        time1 = datetime.datetime.now()

        temp_data = data_cube.sampleRegions(ee.FeatureCollection([can_fire.get(i)]), None, 250)
        temp_data = temp_data.toList(temp_data.size())
        try:
            temp_list = temp_data.getInfo()
        except Exception as e:
            temp_list = list()
            if 'Collection query aborted after accumulating over 5000 elements' in e.args[0]:

                n_temp_feat = temp_data.size().getInfo()
                if n_temp_feat > cutoff:

                    feat_slice_list = list((i * cutoff, (i + 1) * cutoff) for i in range(n_temp_feat // cutoff))

                    if n_temp_feat % cutoff > 0:
                        feat_slice_list += [(feat_slice_list[-1][1], feat_slice_list[-1][1] + (n_temp_feat % cutoff))]

                    for feat_slice in feat_slice_list:
                        temp_list += temp_data.slice(feat_slice[0], feat_slice[1]).getInfo()

        time2 = datetime.datetime.now()

        log.lprint('Time taken for {} pixels, '.format(str(len(temp_list))) +
                   ' ({ii} of {nn} fires): {t} seconds'.format(ii=str(i + 1),
                                                               nn=str(can_feat_size),
                                                               t=str(round(
                                                                   (time2 - time1).total_seconds(), 1))))

        out_list = list()
        for feat in temp_list:
            out_dict = dict()
            for key, val in feat['properties'].items():
                if key in feat_prop_dict:
                    out_dict[feat_prop_dict[key]] = feat['properties'][key]
                elif key in bands:
                    out_dict[key] = feat['properties'][key]
                else:
                    pass

            out_list.append(out_dict)

        if len(out_list) > 0:

            # all extracted dictionaries to file
            if i == 0:
                Handler.write_to_csv(out_list,
                                     header=True,
                                     append=False,
                                     outfile=OUTFILE)

            else:
                Handler.write_to_csv(out_list,
                                     header=False,
                                     append=True,
                                     outfile=OUTFILE)

