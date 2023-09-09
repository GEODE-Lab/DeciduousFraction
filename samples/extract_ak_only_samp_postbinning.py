import ee
import math
from eehelper import EEHelper


# normalized difference vegetation index
def ndvi_calc(img, scale_factor=10000):
    return img.normalizedDifference(['NIR', 'RED']).select([0], ['NDVI']).multiply(scale_factor).toInt16()


# Visible Atmospherically Resistant Index
def vari_calc(img, scale_factor=10000):
    return (img.select(['RED']).subtract(img.select(['GREEN'])))\
        .divide(img.select(['RED']).add(img.select(['GREEN'])).subtract(img.select(['BLUE'])))\
        .select([0], ['VARI']).multiply(scale_factor).toInt16()


# normalized difference water index
def ndwi_calc(img, scale_factor=10000):
    return img.normalizedDifference(['NIR', 'SWIR2']).select([0], ['NDWI']).multiply(scale_factor).toInt16()


# normalized burn ratio
def nbr_calc(img, scale_factor=10000):
    return img.normalizedDifference(['NIR', 'SWIR1']).select([0], ['NBR']).multiply(scale_factor).toInt16()


# soil adjusted vegetation index
def savi_calc(img, const=0.5, scale_factor=10000):
    return (img.select(['NIR']).subtract(img.select(['RED'])).multiply(1 + const))\
        .divide(img.select(['NIR']).add(img.select(['RED'])).add(const))\
        .select([0], ['SAVI']).multiply(scale_factor).toInt16()


# function to add indices to an image
# NDVI, NDWI, VARI, NBR, SAVI
def add_indices(in_image, const=0.5, scale_factor=10000):

    temp_image = in_image.float().divide(scale_factor)
    return in_image.addBands(ndvi_calc(temp_image, scale_factor))\
        .addBands(ndwi_calc(temp_image, scale_factor))\
        .addBands(vari_calc(temp_image, scale_factor))\
        .addBands(nbr_calc(temp_image, scale_factor))\
        .addBands(savi_calc(temp_image, const, scale_factor))


# add suffix to all band names
def add_suffix(in_image, suffix_str):
    bandnames = in_image.bandNames().map(lambda elem: ee.String(elem).toLowerCase().cat('_').cat(suffix_str))
    nb = bandnames.length()
    return in_image.select(ee.List.sequence(0, ee.Number(nb).subtract(1)), bandnames)


# method to correct Landsat 8 based on Landsat 7 reflectance.
# This method scales the SR reflectance values to match LS7 reflectance
# The returned values are generally lower than input image
# based on roy et al 2016
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


# method to correct Landsat 5 based on Landsat 7 reflectance.
# This method scales the SR reflectance values to match LS7 reflectance
# The returned values are generally lower than input image
# based on sulla-menashe et al 2016
def ls5_sr_corr(img):
    return img.select(['B1'], ['BLUE']).float().multiply(0.91996).add(37).int16()\
        .addBands(img.select(['B2'], ['GREEN']).float().multiply(0.92764).add(84).int16())\
        .addBands(img.select(['B3'], ['RED']).float().multiply(0.8881).add(98).int16())\
        .addBands(img.select(['B4'], ['NIR']).float().multiply(0.95057).add(38).int16())\
        .addBands(img.select(['B5'], ['SWIR1']).float().multiply(0.96525).add(29).int16())\
        .addBands(img.select(['B7'], ['SWIR2']).float().multiply(0.99601).add(20).int16())\
        .addBands(img.select(['pixel_qa'], ['PIXEL_QA']).int16())\
        .addBands(img.select(['radsat_qa'], ['RADSAT_QA']).int16())\
        .copyProperties(img)\
        .copyProperties(img, ['system:time_start', 'system:time_end', 'system:index', 'system:footprint'])


# this method renames LS5, LS7, and LS8 bands and corrects LS5 and LS8 bands
# this method should be used with SR only
def ls_sr_band_correction(img):
    return \
        ee.Algorithms.If(
            ee.String(img.get('SATELLITE')).compareTo('LANDSAT_8'),
            ee.Algorithms.If(
                ee.String(img.get('SATELLITE')).compareTo('LANDSAT_5'),
                ee.Image(img.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'pixel_qa', 'radsat_qa'],
                                    ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA', 'RADSAT_QA'])
                         .int16()
                         .copyProperties(img)
                         .copyProperties(img,
                                         ['system:time_start',
                                          'system:time_end',
                                          'system:index',
                                          'system:footprint'])),
                ee.Image(ls5_sr_corr(img))
            ),
            ee.Image(ls8_sr_corr(img))
        )


# method to calcluate clear mask based on pixel_qa and radsat_qa bands
def ls_sr_only_clear(image):

    clearbit = 1
    clearmask = math.pow(2, clearbit)
    qa = image.select('PIXEL_QA')
    qa_mask = qa.bitwiseAnd(clearmask)

    ra = image.select('RADSAT_QA')
    ra_mask = ra.eq(0)

    return ee.Image(image.updateMask(qa_mask).updateMask(ra_mask))


# make collections based on given parameters
def get_landsat_images(collection, bounds, start_date, end_date, start_julian, end_julian):

    return ee.ImageCollection(collection)\
        .filterDate(start_date, end_date)\
        .filter(ee.Filter.calendarRange(start_julian, end_julian))\
        .filterBounds(bounds)\
        .map(ls_sr_band_correction)\
        .map(ls_sr_only_clear)\
        .map(add_indices)


# function to make pctl th value composite
def maxval_comp_ndvi(collection, pctl=50, index='NDVI'):
    index_band = collection.select(index).reduce(ee.Reducer.percentile([pctl]))
    with_dist = collection.map(lambda image : image.addBands(image.select(index)
                                                             .subtract(index_band).abs().multiply(-1)
                                                             .rename('quality')))
    return with_dist.qualityMosaic('quality')


# function to make interval mean composite
def interval_mean(collection, min_pctl, max_pctl, internal_bands):
    temp_img = collection.reduce(ee.Reducer.intervalMean(min_pctl, max_pctl))
    return temp_img.select(ee.List.sequence(0, internal_bands.length().subtract(1)), internal_bands)


# function to make image collection
def make_ls(args):
    collection, elevation_image, elev_scale_factor, bounds, bands, \
        start_date, end_date, start_julian, end_julian, \
        pctl, index, unmask_val = args

    all_images1 = ee.ImageCollection(get_landsat_images(collection, bounds, start_date, end_date,
                                                        start_julian[0], end_julian[0]))

    all_images2 = ee.ImageCollection(get_landsat_images(collection, bounds, start_date, end_date,
                                                        start_julian[1], end_julian[1]))

    all_images3 = ee.ImageCollection(get_landsat_images(collection, bounds, start_date, end_date,
                                                        start_julian[2], end_julian[2]))

    img_season1 = ee.Image(add_suffix(maxval_comp_ndvi(all_images1, pctl, index).select(bands), '1'))\
        .unmask(unmask_val)

    img_season2 = ee.Image(add_suffix(maxval_comp_ndvi(all_images2, pctl, index).select(bands), '2'))\
        .unmask(unmask_val)

    img_season3 = ee.Image(add_suffix(maxval_comp_ndvi(all_images3, pctl, index).select(bands), '3'))\
        .unmask(unmask_val)

    slope = ee.Terrain.slope(elevation_image).multiply(elev_scale_factor)
    aspect = ee.Terrain.aspect(elevation_image)

    topo_image = elevation_image.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                                         ['elevation', 'slope', 'aspect']).int16()

    return img_season1.addBands(img_season2).addBands(img_season3).addBands(topo_image).clip(bounds)


if __name__ == '__main__':

    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_postbin_v8_ak.shp"

    ee.Initialize()

    alaska = ee.Geometry.Polygon(
        [[[-167.783203125, 68.07330474079025],
          [-164.970703125, 66.96447630005638],
          [-168.486328125, 66.26685631430843],
          [-168.22265625, 64.54844014422517],
          [-163.740234375, 63.89873081524393],
          [-166.728515625, 63.11463763252092],
          [-168.3984375, 59.355596110016315],
          [-159.78515625, 57.326521225217064],
          [-165.498046875, 55.727110085045986],
          [-164.70703125, 53.225768435790194],
          [-158.818359375, 54.87660665410869],
          [-153.193359375, 55.7765730186677],
          [-152.490234375, 57.27904276497778],
          [-149.4140625, 58.99531118795094],
          [-145.810546875, 59.977005492196],
          [-140.7568359375, 59.153403092050375],
          [-140.90746584324359, 65.67611691802753],
          [-140.888671875, 70.1851027549897],
          [-146.162109375, 70.55417853776078],
          [-154.248046875, 71.49703690095419],
          [-160.3125, 71.24435551310674],
          [-167.255859375, 68.97416358340674]]])

    # geometries end -------------------------------------------------------------------------------------------------

    all_samp = ee.FeatureCollection("users/masseyr44/shapefiles/all_samp_postbin_v8")

    ls5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR")
    ls7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
    ls8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")

    elevation = ee.Image('USGS/GMTED2010')

    # collections end ----------------------------------------------------------------------------------------

    elev_scale_factor = 10000
    pctl = 50
    index = 'NDVI'
    unmask_val = -9999

    startJulian1 = 90
    endJulian1 = 165
    startJulian2 = 180
    endJulian2 = 240
    startJulian3 = 255
    endJulian3 = 330

    # start year , end year , year
    years = {
        '2000': (1998, 2002),
        '2005': (2003, 2007),
        '2010': (2008, 2012),
        '2015': (2013, 2018)
    }

    # zone name, bounds
    zones = {
        'alaska': alaska,
    }

    internal_bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA',
                              'RADSAT_QA', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

    bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2',
                     'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

    startJulian = [startJulian1, startJulian2, startJulian3]
    endJulian = [endJulian1, endJulian2, endJulian3]

    # static definitions end ----------------------------------------------------------------------------------------

    all_images = ls5.merge(ls7).merge(ls8)

    # print(EEFunc.expand_image_meta(all_images.first()))
    # print(EEFunc.expand_feature_meta(ee.Feature(all_samp.first())))

    for year, dates in years.items():

        startDate = ee.Date.fromYMD(dates[0], 1, 1)
        endDate = ee.Date.fromYMD(dates[1], 12, 31)

        vec_coll = all_samp.filterMetadata('year', 'not_greater_than', dates[1]) \
            .filterMetadata('year', 'not_less_than', dates[0])\
            .filterBounds(alaska)

        print(EEHelper.expand_feature_coll_meta(ee.FeatureCollection(vec_coll)))

        for zone, bounds in zones.items():

            args = (all_images, elevation, elev_scale_factor, bounds, bands,
                    startDate, endDate, startJulian, endJulian,
                    pctl, index, unmask_val)

            output_img = ee.Image(make_ls(args))

            samp = output_img.sample(vec_coll, 30)

            out_name = 'Alaska_samp_median_SR_NDVI_corr_' + zone + '_' + year

            task_config = {
                'driveFileNamePrefix': out_name,
                'driveFolder': 'Boreal_NA_median_SR_NDVI',
                'fileFormat': 'CSV'
            }

            task1 = ee.batch.Export.table(samp,
                                          out_name,
                                          task_config)

            task1.start()
            print(task1)



