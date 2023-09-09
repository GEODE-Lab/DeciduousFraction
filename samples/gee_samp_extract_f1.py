import ee
import os
import sys
import time
import math
import datetime
import traceback
from geosoup import *

ee.Initialize()

folder = "C:/users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/"

folder = "D:/shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/tree_cover/"
infile = folder + "hansen_tc_2010_full.shp"
logfile = folder + "hansen_tc_2010_full.log"
OUTFILE = folder + "hansen_tc_2010_full_v{}.csv".format(datetime.datetime.now().isoformat()\
                                      .split('.')[0].replace('-', '_').replace(':', '_'))

logfile = OUTFILE.split('.csv')[0] + '.log'

log = Logger('SAMP',
             filename=logfile,
             stream=True)

# SPECIFY SEVERAL VARIABLES
BUFFER_DIST = 0  # set it to 0 if buffer is not needed, else it will make script timed-out
CRS = 'EPSG:4326'
SCALE = 30
NULL_VALUE = 0
MASK_VALUE = 0  # used for ADDON image
startJulian = 1  # start
endJulian = 365  # end

start_year, end_year = (2008, 2012)

# parts to divide into if 'too many values' error
n = 5

# wait time
wait = 30  # seconds

max_elem = 1000


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

# values to copy from fusion table/feature collection
feat_properties = ['site', 'year', 'decid_frac']
KEYS = ee.List(feat_properties)

# properties to retrieve from scene
scene_properties = ['CLOUD_COVER',
                    'GEOMETRIC_RMSE_MODEL',
                    'LANDSAT_ID',
                    'SOLAR_ZENITH_ANGLE']
PROPERTY_LIST = ee.List(scene_properties)

# Bands to retrieve
bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'pixel_qa', 'radsat_qa']
ALL_BANDS = ee.List(bands)

# Landsat Surface Reflectance collections
ls5_1 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR")
ls5_2 = ee.ImageCollection("LANDSAT/LT05/C01/T2_SR")
ls7_1 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
ls7_2 = ee.ImageCollection("LANDSAT/LE07/C01/T2_SR")
ls8_1 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
ls8_2 = ee.ImageCollection("LANDSAT/LC08/C01/T2_SR")

elevation = ee.Image('USGS/GMTED2010')
slope = ee.Terrain.slope(elevation)
aspect = ee.Terrain.aspect(elevation)

topo_image = elevation.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                               ['elevation', 'slope', 'aspect'])

topo_bandlist = ['elevation', 'slope', 'aspect']
bands = bands + topo_bandlist


feat_list = list()

samp_vec = Vector(infile)
log.lprint('{}: {}'.format(os.path.basename(infile), samp_vec))

for i, wkt in enumerate(samp_vec.wktlist):
    feat_dict = dict()
    in_dict = samp_vec.attributes[i]
    for k, v in in_dict.items():
        if k in feat_properties:
            feat_dict[k] = v

    if 'POINT' in wkt:
        coords = list(float(coord) for coord in
                      wkt.split('POINT')[1].replace(')', '').replace('(', '').strip().split(' '))
        feat = ee.Feature(ee.Geometry.Point(coords),
                          feat_dict)

    else:
        raise ValueError('Unsupported geometry type')

    feat_list.append(feat)

n_samp = len(feat_list)
log.lprint('Number of samples: {}'.format(str(n_samp)))

# ------------------------------------------------------------------------------------
# BE CAREFUL MODIFYING THE STUFF BELOW
# ------------------------------------------------------------------------------------
# Functions ----------------------------------------

# using list comprehension to chunk list
feat_list_chunks = list(feat_list[i * max_elem:(i + 1) * max_elem]
                        for i in range((len(feat_list) + max_elem - 1) // max_elem))
len_chunks = list(len(chunk) for chunk in feat_list_chunks)

log.lprint("Dividing into chunks: {}".format(', '.join(list(str(elem) for elem in len_chunks))))


# merge all collections in one
def ls_coll(start_day=startJulian,
            end_day=endJulian,
            start_year=None,
            end_year=None):

    # start and end dates
    start_date = ee.Date.fromYMD(start_year, 1, 1)
    end_date = ee.Date.fromYMD(end_year, 12, 31)

    return ee.ImageCollection(ls5_1
                              .merge(ls7_1
                                     .merge(ls8_1
                                            .merge(ls5_2
                                                   .merge(ls7_2
                                                          .merge(ls8_2)))))) \
        .filter(ee.Filter.calendarRange(start_day, end_day, "day_of_year")) \
        .filter(ee.Filter.date(start_date, end_date)) \
        .filterBounds(boundary) \
        .map(lambda image: image.addBands(topo_image, topo_bandlist)) \
        .select(bands) \
        .map(lambda image: image.float())


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


# function to extract a feature from a non-null collection
def get_region(feature):
    # feature to be extracted
    feat = ee.Algorithms.If(ee.Number(BUFFER_DIST).gt(0),
                            ee.Feature(feature).buffer(BUFFER_DIST).bounds(),
                            ee.Feature(feature))

    feat_dict = feat.getInfo()
    feat_props = feat_dict['properties']

    collection = ls_coll(start_year=start_year,
                         end_year=end_year)

    coll = collection.filterBounds(ee.Feature(feature).geometry())
    ncoll = coll.size().getInfo()

    pt_list = list()

    if ncoll > 0:

        # list of properties of each image in the collection as dictionary
        coll_dicts = get_coll_dict(coll).getInfo()

        # extract pixel values from the collection
        # the output is a list or lists with the first row as column names
        temp_list = coll.getRegion(ee.Feature(feat).geometry(), SCALE).getInfo()
        n = len(temp_list)

        elem_names = temp_list[0]
        id_column = elem_names.index('id')

        for j in range(1, n):
            pt_dict = dict()
            for k in range(0, len(elem_names)):
                pt_dict[elem_names[k]] = temp_list[j][k]
                id = temp_list[j][id_column]

                scene_prop_list = list(coll_dict for coll_dict in coll_dicts if coll_dict['id'] == id)
                scene_prop = scene_prop_list[0]

                for prop in scene_properties:
                    pt_dict[prop] = scene_prop[prop]

                for prop in feat_properties:
                    pt_dict[prop] = feat_props[prop]

            pt_list.append(pt_dict)

    else:
        pt_dict = dict()
        pt_dict['id'] = NULL_VALUE
        pt_dict['time'] = NULL_VALUE

        for prop in feat_properties:
            pt_dict[prop] = feat_props[prop]

        for prop in scene_properties:
            pt_dict[prop] = NULL_VALUE

        for band in bands:
            pt_dict[band] = NULL_VALUE

        pt_list.append(pt_dict)

    return pt_list


site_count = 0
time0 = datetime.datetime.now()

for j, chunk in enumerate(feat_list_chunks):
    log.lprint('\n ----------Working on chunk {} --------------\n'.format(str(j + 1)))

    n_sites = len(chunk)
    sites_list = ee.List(chunk)

    # iterate thru site list
    i = 0
    while i < n_sites:

        time1 = datetime.datetime.now()
        site = sites_list.get(i)

        try:
            temp_dicts = get_region(site)

        # if any error occurs, print it and break the loop
        except Exception as e:
            print(e)

            if 'Earth Engine memory capacity exceeded' in e.args[0]:
                log.lprint('Waiting 30 secs...'.format(str(wait)))
                time.sleep(wait)
                continue

            elif 'Too many values' in e.args[0]:
                log.lprint('Dividing the julian date range in {} parts and retrying...'.format(str(n)))

                # divide into n parts

                dates = list(range(startJulian, endJulian, int(math.floor((endJulian-startJulian)/n))))
                dates[-1] = endJulian
                date_tuples = [(dates[i], dates[i+1]-1)
                               if i != len(dates)-2
                               else (dates[i], dates[i+1])
                               for i in range(0, len(dates)-1)]

                part_dicts = list()

                for date_tuple in date_tuples:
                    coll = ls_coll(start_day=date_tuple[0],
                                   end_day=date_tuple[1])

                    part_dict = get_region(site,
                                           collection=coll)

                    for part in part_dict:
                        part_dicts.append(part)

                temp_dicts = part_dicts

            elif 'ServerNotFoundError' in e.args[0] or \
                    'Unable to find the server' in e.args[0] or \
                    'getaddrinfo failed' in e.args[0] or \
                    'connection attempt failed' in e.args[0]:

                log.lprint('Waiting 30 secs...'.format(str(wait)))
                time.sleep(wait)
                continue

            else:
                log.lprint('Exiting...')
                break

        # all extracted dictionaries to file
        if not Handler(OUTFILE).file_exists():
            Handler.write_to_csv(temp_dicts,
                                 header=True,
                                 append=False,
                                 outfile=OUTFILE)

        else:
            Handler.write_to_csv(temp_dicts,
                                 header=False,
                                 append=True,
                                 outfile=OUTFILE)

        time2 = datetime.datetime.now()

        log.lprint('Time taken for site {s} ({ii} of {nn}): {t} seconds'.format(s=str(temp_dicts[0]['site']),
                                                                            ii=str(site_count + 1),
                                                                            nn=str(n_samp),
                                                                   t=str(round((time2 - time1).total_seconds(), 1))))

        i += 1
        site_count += 1

    log.lprint('\n ----------completed chunk {} --------------\n'.format(str(j + 1)))

time0_ = datetime.datetime.now()
log.lprint('Total Time taken: {t} seconds'.format(t=Timer.display_time((time0_ - time0).total_seconds(), precision=1)))
