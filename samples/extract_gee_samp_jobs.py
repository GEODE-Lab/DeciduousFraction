import ee
import os
import sys
import time
import math
import datetime
import traceback
from geosoup import *


# normalized difference vegetation index
def ndvi_calc(img):
    return img.normalizedDifference(['NIR', 'RED'])\
           .select([0],['NDVI'])\
           .multiply(10000)\
           .toInt16()


# Visible Atmospherically Resistant Index
def vari_calc(img):
    return (img.select(['RED']).subtract(img.select(['GREEN'])))\
           .divide(img.select(['RED']).add(img.select(['GREEN'])).subtract(img.select(['BLUE'])))\
           .select([0],['VARI'])\
           .multiply(10000)\
           .toInt16()


# normalized difference water index
def ndwi_calc(img):
    return img.normalizedDifference(['NIR', 'SWIR2'])\
           .select([0],['NDWI'])\
           .multiply(10000)\
           .toInt16()


# normalized burn ratio
def nbr_calc(img):
    return img.normalizedDifference(['NIR', 'SWIR1'])\
           .select([0],['NBR'])\
           .multiply(10000)\
           .toInt16()


# soil adjusted vegetation index
def savi_calc(img):
    return (img.select(['NIR']).subtract(img.select(['RED'])).multiply(1+L))\
            .divide(img.select(['NIR']).add(img.select(['RED'])).add(L))\
            .select([0], ['SAVI'])\
            .multiply(10000)\
            .toInt16()


# function to add indices to an image
# NDVI, NDWI, VARI, NBR, SAVI
def addIndices(in_image):
    in_image = in_image.float().divide(10000.0)
    return in_image.addBands(ndvi_calc(in_image))\
                   .addBands(ndwi_calc(in_image))\
                   .addBands(vari_calc(in_image))\
                   .addBands(nbr_calc(in_image))\
                   .addBands(savi_calc(in_image))\
                   .toInt16()


# method to correct Landsat 8 based on Landsat 7 reflectance.
# This method scales the SR reflectance values to match LS7 reflectance
# The returned values are generally lower than input image
def ls8_sr_corr(img):
    return img.select(['B2'], ['BLUE']).float().multiply(0.8850).add(183).int16()\
            .addBands(img.select(['B3'], ['GREEN']).float().multiply(0.9317).add(123).int16())\
            .addBands(img.select(['B4'], ['RED']).float().multiply(0.9372).add(123).int16())\
            .addBands(img.select(['B5'], ['NIR']).float().multiply(0.8339).add(448).int16())\
            .addBands(img.select(['B6'], ['SWIR1']).float().multiply(0.8639).add(306).int16())\
            .addBands(img.select(['B7'], ['SWIR2']).float().multiply(0.9165).add(116).int16())\
            .addBands(img.select(['pixel_qa'], ['PIXEL_QA']).int16())\
            .addBands(img.select(['radsat_qa'], ['RADSAT_QA']).int16())\
            .copyProperties(img)\
            .copyProperties(img, ['system:time_start', 'system:time_end',
                                  'system:index', 'system:footprint'])


# this method renames LS5 and LS7 bands and corrects LS8 bands using LS8_corr()
# this method should be used with SR only
def ls_sr_band_correction(img):
    return ee.Algorithms.If(
        ee.String(img.get('SATELLITE')).compareTo('LANDSAT_8'),
        ee.Image(img.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'pixel_qa', 'radsat_qa'],
                            ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA', 'RADSAT_QA'])
                 .multiply(10000)
                 .int16()
                 .copyProperties(img)
                 .copyProperties(img, ['system:time_start', 'system:time_end', 'system:index', 'system:footprint'])),
        ee.Image(img.select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'pixel_qa', 'radsat_qa'],
                            ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA', 'RADSAT_QA'])
                 .multiply(10000)
                 .int16()
                 .copyProperties(img)
                 .copyProperties(img, ['system:time_start', 'system:time_end', 'system:index', 'system:footprint'])),)


# method to calcluate clear mask based on pixel_qa and radsat_qa bands
def ls_sr_only_clear(image):
    clear_bit = 1
    clear_mask = int(math.pow(2, clear_bit))
    qa = ee.Image(image).select('PIXEL_QA')
    qa_mask = qa.bitwiseAnd(clear_mask)
    ra = ee.Image(image).select('RADSAT_QA')
    ra_mask = ra.eq(0)

    return ee.Image(image).updateMask(qa_mask).updateMask(ra_mask)


# make collections based on given parameters
def get_landsat_images(collection,
                       bounds,
                       start_date,
                       end_date,
                       start_julian,
                       end_julian):
    return ee.ImageCollection(collection)\
             .filterDate(start_date, end_date)\
             .filter(ee.Filter.calendarRange(start_julian, end_julian))\
             .filterBounds(bounds)\
             .map(ls_sr_band_correction)\
             .map(ls_sr_only_clear)\
             .map(addIndices)


# function to make pctl th value composite
def maxvalcomp_ndvi(collection,
                    bounds,
                    pctl=75,
                    band='NDVI'):
    index_band = collection.select(band).reduce(ee.Reducer.percentile([pctl]))
    with_dist = collection.map(lambda image: image.addBands(image.select(band).subtract(index_band)
                               .abs().multiply(-1).rename('quality')))
    return with_dist.qualityMosaic('quality')


if __name__ == '__main__':

    ee.Initialize()

    folder = "D:/shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/tree_cover/"
    shpfile = folder + "hansen_tc_2010_full.shp"
    logfile = folder + "hansen_tc_2010_full.log"

    version = 2

    out_name = "hansen_tc_2010_v{}_".format(str(version))

    log = Logger('SAMP',
                 filename=logfile,
                 stream=True)

    log.lprint('Shp file: {}'.format(shpfile))

    # max number of samples in a feature collection
    nmax = 1000

    start_year = 2008
    end_year = 2012
    year = 2010
    L = 0.5
    index = 'NDVI'
    pctl = 75

    side_div = 40

    startDate = ee.Date.fromYMD(start_year, 1, 1)
    endDate = ee.Date.fromYMD(end_year, 12, 31)

    startJulian1 = 90
    endJulian1 = 150
    startJulian2 = 180
    endJulian2 = 240
    startJulian3 = 270
    endJulian3 = 330

    # values to copy from fusion table/feature collection
    feat_properties = ['tc_value']
    KEYS = ee.List(feat_properties)

    # Landsat Surface Reflectance collections
    ls5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR")
    ls7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
    ls8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")

    ls_coll = ls5.merge(ls7.merge(ls8))

    elevation = ee.Image('USGS/GMTED2010')
    slope = ee.Terrain.slope(elevation)
    aspect = ee.Terrain.aspect(elevation)

    topo_image = elevation.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                                   ['elevation', 'slope', 'aspect'])

    # boundary of the region
    bound_coords = [[[-168.83884, 66.60503], [-168.66305, 64.72256], [-166.11423, 63.29787], [-168.83884, 60.31062],
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
                     [-149.64965, 71.03224], [-158.08715, 71.65080], [-167.93090, 69.24910]]]

    grid_coords_list = Vector.polygon_bound_grid(bound_coords[0],
                                                 div=side_div,
                                                 intersect_check=True)
    vec = Vector(shpfile)
    grided_samp_list = list()

    for g, grid_coords in enumerate(grid_coords_list):
        grid_wkt = Vector.wkt_from_coords(grid_coords, geom_type='polygon')
        grid_vec = Vector.vector_from_string(grid_wkt, vector_type='polygon')
        grid_samp = grid_vec.get_intersecting_vector(vec, filter_query=True)
        grid_samp.name = out_name + str(g + 1)
        grided_samp_list.append(grid_samp)

        print(grid_samp)

        if grid_samp.nfeat > 0:

            coords_list = list()
            feat_list = list()

            for k, wkt in enumerate(grid_samp.wktlist):
                feat_dict = dict()
                for key, val in grid_samp.attributes[k].items():
                    if key in feat_properties:
                        feat_dict[key] = val

                coords = list(float(coord) for coord in
                              wkt.split('POINT')[1].replace(')', '').replace('(', '').strip().split(' '))
                coords_list.append(coords)

                feat = ee.Feature(ee.Geometry.Point(coords),
                                  feat_dict)

                feat_list.append(feat)

            feat_coll = ee.FeatureCollection(feat_list)

            bound_coords = grid_coords[:-1]
            bounds = ee.Geometry.Polygon(bound_coords)

            allImages1 = get_landsat_images(ls_coll, bounds, startDate, endDate, startJulian1, endJulian1)
            allImages2 = get_landsat_images(ls_coll, bounds, startDate, endDate, startJulian2, endJulian2)
            allImages3 = get_landsat_images(ls_coll, bounds, startDate, endDate, startJulian3, endJulian3)

            imgSeason1 = maxvalcomp_ndvi(allImages1, bounds).select(
                ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

            imgSeason2 = maxvalcomp_ndvi(allImages2, bounds).select(
                ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

            imgSeason3 = maxvalcomp_ndvi(allImages3, bounds).select(
                ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

            layer_stack = imgSeason1.addBands(imgSeason2).addBands(imgSeason3).addBands(topo_image)

            samp_ext = ee.Image(layer_stack).sampleRegions(collection=feat_coll, scale=30)

            image_task_config = {'outputBucket': 'masseyr44_store1',
                                 'outputPrefix': 'tree_cover/{}'.format(out_name + str(g+1)),
                                 'scale': 30}

            post_image_task = ee.batch.Export.table(collection=samp_ext,
                                                    description=out_name + str(g + 1),
                                                    config=image_task_config)
            print('{} : {}'.format(str(g+1), post_image_task))
            post_image_task.start()



