import ee
from eehelper import EEHelper
from geosoup import Sublist

"""
Script to preprocess Landsat 5, 7, and 8 datasets into Mosaicked layerstacks
for deciduous fraction and tree cover regression
"""


def bounds2coords(bounds_list,
                  close_rings=False):
    """
    Method to return point coords of vertices from bounds
    :param bounds_list: (minx, maxx, miny, maxy)
    :param close_rings: bool, should last vertex be the same as the first one
    :return: list of list oof x, y coords
    """
    minx, maxx, miny, maxy = bounds_list
    vertex_coords = [[minx, maxy],
                     [maxx, maxy],
                     [maxx, miny],
                     [minx, miny]]
    if close_rings:

        return vertex_coords + [vertex_coords[0]]
    else:
        return vertex_coords


def get_landsat_images(collection, bound_geom, start_date, end_date, start_julian, end_julian):
    """ Make collections based on given parameters"""
    return ee.ImageCollection(collection) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.calendarRange(start_julian, end_julian)) \
        .filterBounds(bound_geom) \
        .map(EEHelper.ls_sr_band_correction) \
        .map(EEHelper.ls_sr_only_clear) \
        .map(EEHelper(scale_factor=10000).add_indices)


def make_ls(composite_args):
    """ function to make image collection"""
    collection, elevation_image, slope_scale_fac, bound_geom, band_list, \
        start_date, end_date, start_julian, end_julian, \
        percentile, veg_index, nodata_val = composite_args

    seasonal_composite = EEHelper(composite_index=veg_index,
                                  composite_function='percentile_{}'.format(str(percentile))).composite_image

    all_images = ee.ImageCollection(get_landsat_images(collection, bound_geom,
                                                       start_date, end_date,
                                                       start_julian, end_julian))

    img_season = ee.Image(EEHelper.add_suffix(seasonal_composite(all_images, bound_geom).select(band_list), '1')) \
        .unmask(nodata_val) \
        .clip(bound_geom).toInt16()

    slope = ee.Terrain.slope(elevation_image).multiply(slope_scale_fac)
    aspect = ee.Terrain.aspect(elevation_image)
    topo_image = elevation_image.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                                         ['elevation', 'slope', 'aspect'])\
        .unmask(nodata_val) \
        .clip(bound_geom).toInt16()

    return img_season.addBands(topo_image)


if __name__ == '__main__':

    ee.Initialize()

    # minx maxx miny maxy
    bounds = (-179.5, -50, 40, 80)

    ndiv = 5

    zone_x_edges = Sublist.frange(-179.5, -50, div=ndiv)
    print(zone_x_edges)

    zone_bounds = list((zone_x_edges[i], zone_x_edges[i + 1], 40, 80) for i in range(ndiv))

    zones = {}

    for i, zone_bound in enumerate(zone_bounds):
        coords = bounds2coords(zone_bound)
        zones['zone{}'.format(str(i + 1))] = ee.Geometry.Polygon([coords])

    # geometries end -------------------------------------------------------------------------------------------------

    all_samp = ee.FeatureCollection("users/masseyr44/shapefiles/all_samp_postbin_v8")
    boreal_h = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_simple").first().geometry()
    boreal_b = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal_10km_buffer").first().geometry()

    ls5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR")
    ls7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
    ls8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")

    elevation = ee.Image('USGS/GMTED2010')

    # collections end ----------------------------------------------------------------------------------------

    slope_scale_factor = 1000
    pctl = 95
    index = 'NDVI'
    nodata = -9999

    startJulian = 120
    endJulian = 300

    # start year , end year , year
    years = {
        '1992': (1987, 1997),
        # '2000': (1998, 2002),
        # '2005': (2003, 2007),
        # '2010': (2008, 2012),
        # '2015': (2013, 2018)
    }

    internal_bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA',
                              'RADSAT_QA', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

    bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2',
                     'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

    # static definitions end ----------------------------------------------------------------------------------------

    all_coll = ls5.merge(ls7).merge(ls8)

    print(EEHelper.expand_image_meta(all_coll.first()))

    for year, dates in years.items():

        startDate = ee.Date.fromYMD(dates[0], 1, 1)
        endDate = ee.Date.fromYMD(dates[1], 12, 31)

        for zone, bounds in zones.items():

            args = (all_coll, elevation, slope_scale_factor, bounds, bands,
                    startDate, endDate, startJulian, endJulian,
                    pctl, index, nodata)

            output_img = ee.Image(make_ls(args))

            out_name = 'Boreal_NA_pctl{}_SR_NDVI_LS5C_'.format(str(pctl)) + zone + '_' + year

            task_config = {
                'driveFileNamePrefix': out_name,
                'crs': 'EPSG:4326',
                'scale': 30,
                'maxPixels': 1e13,
                'fileFormat': 'GeoTIFF',
                'region': bounds,
                'driveFolder': 'Boreal_NA_pctl_{}_annual_SR_NDVI_{}'.format(str(pctl), str(year))
            }

            task1 = ee.batch.Export.image(output_img,
                                          out_name,
                                          task_config)

            task1.start()
            print(task1)
