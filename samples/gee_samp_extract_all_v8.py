import ee
import sys
import os
import time
import datetime
from geosoup import Vector, Handler, Timer, Logger


# function to identify year bins
def get_year_limits(year):
    if year < year_bins[0][0]:
        return 1950, year_bins[0][0]
    elif year > year_bins[-1][1]:
        return year_bins[-1][1], 2020
    else:
        for bins in year_bins:
            if bins[0] <= year <= bins[1]:
                return bins


# merge all collections in one
def ls_coll(start_day=None,
            end_day=None,
            start_year=None,
            end_year=None,
            geometry=None):

    # Landsat Surface Reflectance collections
    ls5_1 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR")
    ls5_2 = ee.ImageCollection("LANDSAT/LT05/C01/T2_SR")
    ls7_1 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
    ls7_2 = ee.ImageCollection("LANDSAT/LE07/C01/T2_SR")
    ls8_1 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
    ls8_2 = ee.ImageCollection("LANDSAT/LC08/C01/T2_SR")

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
        .filterBounds(geometry) \
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

    start_year, end_year = get_year_limits(feat_props['year'])

    collection = ls_coll(start_day=startJulian,
                         end_day=endJulian,
                         start_year=start_year,
                         end_year=end_year,
                         geometry=ee.Feature(feature).geometry())

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


if __name__ == '__main__':

    script, infile, outfolder, version, elem_per_chunk, chunk_number = sys.argv

    '''
    infile = "C:/shared/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1.shp"
    outfolder = 'c:/temp/'
    version = 1
    elem_per_chunk = 1000
    chunk_number = 2
    '''

    ee.Initialize()

    OUTFILE = outfolder + \
        'gee_samp_extract_v{}_{}_{}.csv'.format(str(version),
                                                str(chunk_number),
                                                datetime.datetime.now().isoformat()
                                                .split('.')[0].replace('-', '_').replace(':', '_'))

    logfile = OUTFILE.split('.csv')[0] + '.log'

    log = Logger('SAMP',
                 filename=logfile,
                 stream=True)

    log.lprint('Outfile: {}'.format(OUTFILE))
    log.lprint('Logfile: {}'.format(logfile))

    # SPECIFY SEVERAL VARIABLES
    BUFFER_DIST = 0  # set it to 0 if buffer is not needed, else it will make script timed-out
    CRS = 'EPSG:4326'
    SCALE = 30
    NULL_VALUE = 0
    MASK_VALUE = 0  # used for ADDON image
    startJulian = 1  # start
    endJulian = 365  # end

    year_bins = [(1984, 1997),
                 (1998, 2002),
                 (2003, 2007),
                 (2008, 2012),
                 (2013, 2018)]

    # wait time
    wait = 2  # seconds

    site_count = 0
    n_tries = 10

    max_elem = int(elem_per_chunk)

    # boundary of the region
    bound_coords = [[-167.1254371293343, 51.265857159578474],
                    [-160.0941871293343, 53.255838074180836],
                    [-150.9535621293343, 56.19798604338907],
                    [-142.8676246293343, 56.6838344353184],
                    [-136.1879371293343, 54.49922635010025],
                    [-127.13520275433432, 46.5933986318261],
                    [-106.48090587933432, 47.01452144580692],
                    [-96.90082775433432, 46.10807691948188],
                    [-87.23285900433432, 45.4337200305347],
                    [-84.42035900433432, 41.0841001357377],
                    [-78.53168712933432, 41.546193107354306],
                    [-70.35785900433432, 42.265711759259275],
                    [-59.371530879334316, 41.546193107354306],
                    [-45.309030879334316, 44.626238211456496],
                    [-47.418405879334316, 52.77999675546719],
                    [-54.889109004334316, 60.26474213085188],
                    [-69.30317150433432, 68.96065282391558],
                    [-83.80512462933432, 69.85693191592871],
                    [-109.55707775433432, 70.45361642971407],
                    [-127.83832775433432, 70.86115290711827],
                    [-155.3480933793343, 72.22402444279035],
                    [-168.0043433793343, 70.27641602436853],
                    [-168.1801246293343, 66.46317956940068],
                    [-173.9809058793343, 60.002136210595296],
                    [-178.28754650433427, 50.545366759887806],
                    [-167.1254371293343, 51.265857159578474]]

    boundary_geom = Vector.get_osgeo_geom(Vector.wkt_from_coords(bound_coords, 'polygon'),
                                          geom_type='wkt')

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

    elevation = ee.Image('USGS/GMTED2010')
    slope = ee.Terrain.slope(elevation)
    aspect = ee.Terrain.aspect(elevation)

    topo_image = elevation.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                                   ['elevation', 'slope', 'aspect'])

    topo_bandlist = ['elevation', 'slope', 'aspect']
    bands = bands + topo_bandlist

    samp_vec = Vector(infile)

    log.lprint('{}: {}'.format(os.path.basename(infile), samp_vec))

    # ------------------------------------------------------------------------------------
    # BE CAREFUL MODIFYING THE STUFF BELOW
    # ------------------------------------------------------------------------------------
    # Functions ----------------------------------------

    feat_indx_list = list(range(0, samp_vec.nfeat))

    # using list comprehension to chunk list
    feat_indx_list_chunks = list(feat_indx_list[i * max_elem:(i + 1) * max_elem]
                                 for i in range((len(feat_indx_list) + max_elem - 1) // max_elem))
    len_chunks = list(len(chunk) for chunk in feat_indx_list_chunks)

    log.lprint("Dividing into chunks: {}".format(', '.join(list(str(elem) for elem in len_chunks))))

    time0 = datetime.datetime.now()

    chunk = feat_indx_list_chunks[int(chunk_number)]

    log.lprint('\n ----------Working on chunk {} --------------\n'.format(str(int(chunk_number) + 1)))

    n_sites = len(chunk)
    log.lprint('Number of sites: {}'.format(str(n_sites)))

    # iterate thru site list
    for indx in chunk:

        time1 = datetime.datetime.now()

        samp_wkt = samp_vec.wktlist[indx]
        samp_attr = samp_vec.attributes[indx]

        if boundary_geom.Intersects(Vector.get_osgeo_geom(samp_wkt)):

            samp_dict = dict()
            in_dict = samp_vec.attributes[indx]

            for k, v in in_dict.items():
                if k in feat_properties:
                    samp_dict[k] = v

            if 'POINT' in samp_wkt:
                coords = list(float(coord) for coord in
                              samp_wkt.split('POINT')[1].replace(')', '').replace('(', '').strip().split(' '))
                feat = ee.Feature(ee.Geometry.Point(coords),
                                  samp_dict)
            elif 'LINESTRING' in samp_wkt:
                coords = list(list(float(coord) for coord in coord_str.split(' '))
                              for coord_str in
                              samp_wkt.split('LINESTRING')[1].replace(')', '').replace('(', '').strip().split(','))
                feat = ee.Feature(ee.Geometry.LineString(coords),
                                  samp_dict)
            else:
                raise ValueError('Unsupported geometry type')

            read = False
            n_tries_remain = n_tries

            while not read and n_tries_remain > 0:

                try:
                    temp_dicts = get_region(feat)
                    read = True
                # if any error occurs, print it and break the loop
                except Exception as e:
                    log.lprint(e.args[0])

                    n_tries_remain -= 1

                    if type(e.args[0]) in (str,):

                        if 'Earth Engine memory capacity exceeded' in e.args[0]:
                            log.lprint('Waiting {} secs...'.format(str(wait)))
                            time.sleep(wait)
                            continue

                        elif 'ServerNotFoundError' in e.args[0] or \
                                'Unable to find the server' in e.args[0] or \
                                'getaddrinfo failed' in e.args[0] or \
                                'connection attempt failed' in e.args[0]:

                            log.lprint('Waiting {} secs to read...'.format(str(wait)))
                            time.sleep(wait)
                            continue

                    else:
                        continue

                written = False
                n_tries_remain = n_tries

                while not written and n_tries_remain > 0:

                    try:
                        # all extracted dictionaries to file
                        if not Handler(OUTFILE).file_exists():
                            Handler.write_to_csv(temp_dicts,
                                                 append=False,
                                                 outfile=OUTFILE)
                        else:
                            Handler.write_to_csv(temp_dicts,
                                                 append=True,
                                                 outfile=OUTFILE)
                        written = True

                    except Exception as e:
                        print(e)
                        log.lprint('Waiting {} secs to write...'.format(str(wait)))
                        time.sleep(wait)
                        continue

                time2 = datetime.datetime.now()

                log.lprint('Time taken for site {s} ({ii} of {nn}): {t} seconds'.format(s=str(temp_dicts[0]['site']),
                                                                                        ii=str(site_count + 1),
                                                                                        nn=str(len(chunk)),
                                                                                        t=str(round((time2 - time1)
                                                                                                    .total_seconds(),
                                                                                                    1))))
                site_count += 1

    log.lprint('\n ----------completed chunk {} --------------\n'.format(str(int(chunk_number) + 1)))

    time0_ = datetime.datetime.now()
    log.lprint('Total Time taken: {t} seconds'.format(t=Timer.display_time((time0_ - time0).total_seconds(),
                                                                           precision=1)))
