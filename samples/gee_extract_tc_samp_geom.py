import ee
import os
import sys
import time
import math
import datetime
import traceback
from geosoup import *


if __name__ == '__main__':

    ee.Initialize()

    samp_per_level = 100


    tc_val_list = list(range(0, 100, 1))
    total_samp = len(tc_val_list) * samp_per_level

    # boundary of the region
    above_coords = [[[-168.83884, 66.60503], [-168.66305, 64.72256], [-166.11423, 63.29787], [-168.83884, 60.31062],
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
                     [-149.64965, 71.03224], [-158.08715, 71.65080],
                     [-167.93090, 69.24910]]]

    boundary = ee.Geometry.Polygon(above_coords)

    tc_2010 = ee.Image('users/masseyr44/decid/hansen_tc_2010_mosaic_vis').select([0], ['tree_cover'])

    print(tc_2010.getInfo())

    for tc_perc in tc_val_list:

        tc_perc = 50


        print(tc_perc)

        temp_img = ee.Image(tc_2010).updateMask(ee.Image(tc_2010).eq(tc_perc))

        tc_samp_geom = temp_img.stratifiedSample(numPoints=samp_per_level,
                                                 classBand='tree_cover',
                                                 region=boundary,
                                                 scale=30,
                                                 seed=tc_perc,
                                                 tileScale=2,
                                                 geometries=True).map(lambda x: ee.Feature(x).centroid())

        print(tc_samp_geom.getInfo())

        exit()











