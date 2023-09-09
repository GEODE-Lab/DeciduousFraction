"""
Code to extract point samples from Landsat image collections on Google Earth Engine
This script returns large csv files. It also uses looped getInfo calls to GEE
"""

import ee
import sys
import datetime
import pandas as pd


ee.Initialize()


# constant variables
BUFFER_DIST = 30
CRS = 'EPSG:4326'
SCALE = 30
KEYS = ee.List(['site',
                'Decid_AVG',
                'Decid_SD'])

PROPERTY_LIST = ee.List(['CLOUD_COVER',
                         'GEOMETRIC_RMSE_MODEL',
                         'LANDSAT_ID',
                         'SOLAR_ZENITH_ANGLE'])

outfile = '/scratch/rm885/csv/landsat_extracted_ak_2010.csv'

# Landsat Surface Reflectance collections
ls5_1 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR")
ls5_2 = ee.ImageCollection("LANDSAT/LT05/C01/T2_SR")
ls7_1 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
ls7_2 = ee.ImageCollection("LANDSAT/LE07/C01/T2_SR")

# Get squares around each point with side (2 x BUFFER_DIST)
sites = ee.FeatureCollection('ft:1qB1-aZ55PkKGW9tK07nwEICudlyKf-02f1BwLu9D').merge(
    ee.FeatureCollection('ft:1NbYQupmfy_hTYHT9Cr9Sww7kGSamiGXa1OKI51RR')) \
                .map(lambda feat: feat.buffer(BUFFER_DIST).bounds())


# define boundary for area of interest
boundary = ee.Geometry.Polygon([[[-166.904296875, 68.91100484562017],
                                 [-169.365234375, 64.88626540914477],
                                 [-167.607421875, 62.431074232920906],
                                 [-168.3984375, 57.75107598132104],
                                 [-164.794921875, 53.852526600449515],
                                 [-154.16015625, 55.07836723201514],
                                 [-146.162109375, 59.84481485969105],
                                 [-132.71484375, 54.059387886623576],
                                 [-128.408203125, 54.97761367069628],
                                 [-131.220703125, 58.44773280389084],
                                 [-139.833984375, 61.14323525084058],
                                 [-139.658203125, 69.90011762668541],
                                 [-158.02734375, 71.60828252210266]]])

# merge all collections in one
LS_COLL = ee.ImageCollection(ls5_1
                             .merge(ls7_1
                                    .merge(ls5_2
                                           .merge(ls7_2)))) \
                .filterBounds(boundary) \
                .select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
                         'pixel_qa', 'radsat_qa']) \
                .map(lambda image: image.float())


# print and flush function
def cprint(text):
    sys.stdout.write(str(text) + '\n')
    sys.stdout.flush()


# function to extract properties from collection as list of dictionaries
def get_coll_dict(image_collection):

    n_images = ee.ImageCollection(image_collection).size()
    coll_list = ee.ImageCollection(image_collection).toList(n_images)

    # extract properties in PROPERTY_LIST from one image
    def get_prop(image):
        image_dict = ee.Image(image).toDictionary()
        val_list = PROPERTY_LIST.map(lambda prop: image_dict.get(prop)).add(ee.Image(image).id())
        return ee.Dictionary.fromLists(PROPERTY_LIST.add('id'), val_list)

    return coll_list.map(get_prop)


# function to concatenate two GEE lists
def add_lists(list1, list2):
    first = ee.List(list1).add(list2.get(0))
    n = list2.size()

    def _combine(this, prev):
        return ee.List(prev).add(this)

    return ee.List(list2).slice(1, n).iterate(_combine, first)


# function to extract regions from Image Collection and add scene metadata as dictionaries
def get_regions(feature):

    # get images that intersect with the feature as collection and make a list from it
    coll = LS_COLL.filterBounds(ee.Feature(feature).geometry())
    coll_dicts = get_coll_dict(coll)
    coll_index_list = coll_dicts.map(lambda image_dict: ee.Dictionary(image_dict).get('id'))

    # extract pixel values as list
    temp_list = coll.getRegion(ee.Feature(feature).geometry(), SCALE)
    n = temp_list.length()

    # This appends the fusion table values to the properties exported
    # But this will throw an error if there are 'Null' values in the fusion table
    feature_indices = KEYS.map(lambda x: ee.Feature(feature).get(x))
    keys = add_lists(ee.List(temp_list.get(0)), KEYS)

    # list of keys and values
    val_list = temp_list.slice(1, n).map(lambda x: add_lists(x, feature_indices))
    key_list = ee.List.repeat(keys, n.subtract(1))

    # prepare dictionary from key, value pairs
    feat_dict = ee.List.sequence(0, n.subtract(2)).map(lambda x: ee.Dictionary.fromLists(key_list.get(x),
                                                                                         val_list.get(x)))
    return feat_dict.map(lambda x: ee.Dictionary(x).combine(ee.List(coll_dicts)
                         .get(coll_index_list.indexOf(ee.Dictionary(x).get('id')))))


time0 = datetime.datetime.now()

# convert sites collection to list
n_sites = sites.size().getInfo()
sites_list = sites.toList(n_sites)

# iterate thru site list
for i in range(0, n_sites):
    time1 = datetime.datetime.now()

    try:
        temp_dicts = get_regions(sites_list.get(i)).getInfo()

    # if any error occurs, print it and break the loop
    except Exception as e:
        print(e)
        break

    # convert to pandas data frame
    df = pd.DataFrame(temp_dicts)

    # all extracted values to file
    if i == 0:
        with open(outfile, 'w') as f:
            df.to_csv(f, index=False, header=True)
    else:
        with open(outfile, 'a') as f:
            df.to_csv(f, index=False, header=False)

    time2 = datetime.datetime.now()

    cprint('Time taken for sample {s}: {t} seconds'.format(s=str(i+1),
                                                           t=str(round((time2-time1).total_seconds(), 1))))

time0_ = datetime.datetime.now()
cprint('Total Time taken: {t} seconds'.format(t=str(round((time0_-time0).total_seconds(), 1))))
