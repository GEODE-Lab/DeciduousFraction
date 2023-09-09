import ee
import sys
import os
import time
import datetime
from geosoup import Vector, Handler, Timer, Logger, Opt

if __name__ == '__main__':

    script, elem_per_chunk, chunk_number = sys.argv

    # elem_per_chunk = 3000
    # chunk_number = 6

    ee.Initialize()

    infile = "/home/richard/data/all_samp_pre_v1_uniq.shp"

    '''
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1_uniq.shp"    
    OUTFILE = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1_uniq_test_extract.csv"    
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/all_samp_pre_v1_uniq.shp"
    OUTFILE = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/' \
              'gee_samp_extract_prebin_v1_chunk6_last60_{}_{}.csv'.format(str(chunk_number),
                                                                                          Opt.hostname(),
                                                                                  datetime.datetime.now().isoformat()
    '''
    OUTFILE = '/home/richard/scratch/gee_samp_extract_prebin_v1_chunk{}_{}_{}.csv'.format(str(chunk_number),
                                                                                          Opt.hostname(),
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
    endJulian = 366  # end
    startYear = 1984
    endYear = 2020

    # parts to divide into if 'too many values' error
    n = 5

    # wait time
    wait = 30  # seconds

    max_elem = int(elem_per_chunk)

    # boundary of the region
    bound_coords = [[-166.552734375, 56.218923189166624],
                      [-165.146484375, 52.268157373768176],
                      [-155.126953125, 54.622978132690335],
                      [-150.908203125, 57.98480801923985],
                      [-145.810546875, 59.17592824927136],
                      [-138.076171875, 58.12431960569374],
                      [-131.044921875, 51.508742458803326],
                      [-126.123046875, 47.57652571374621],
                      [-111.005859375, 48.28319289548349],
                      [-96.416015625, 48.2246726495652],
                      [-90.703125, 47.45780853075031],
                      [-83.14453125, 44.653024159812006],
                      [-86.220703125, 40.58058466412762],
                      [-82.705078125, 40.44694705960048],
                      [-76.025390625, 43.70759350405294],
                      [-73.125, 44.08758502824516],
                      [-68.37890625, 45.9511496866914],
                      [-67.763671875, 42.16340342422401],
                      [-59.326171875, 43.834526782236814],
                      [-50.537109375, 46.255846818480315],
                      [-51.50390625, 51.12421275782688],
                      [-51.064453125, 57.61010702068388],
                      [-65.654296875, 62.062733258846514],
                      [-85.341796875, 66.44310650816469],
                      [-95.185546875, 67.57571741708057],
                      [-113.466796875, 68.13885164925574],
                      [-125.947265625, 70.4073476760681],
                      [-140.09765625, 70.31873847853124],
                      [-156.708984375, 71.63599288330609],
                      [-167.431640625, 69.3493386397765],
                      [-165.146484375, 66.72254132270653],
                      [-168.662109375, 65.47650756256367],
                      [-165.673828125, 63.31268278043484],
                      [-168.837890625, 60.326947742998414],
                      [-166.552734375, 56.218923189166624]]

    # boundary = ee.Geometry.Polygon(bound_coords)
    # boundary = ee.FeatureCollection('users/masseyr44/shapefiles/NAboreal_10kmbuffer').first().geometry()

    boundary_geom = Vector.get_osgeo_geom(Vector.wkt_from_coords(bound_coords, 'polygon'),
                                          geom_type='wkt')

    # values to copy from fusion table/feature collection
    feat_properties = ['site', 'latitude', 'longitude']
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

    intersect_count = 0

    for i, wkt in enumerate(samp_vec.wktlist):

        if boundary_geom.Intersects(Vector.get_osgeo_geom(wkt)):

            intersect_count += 1

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

            elif 'LINESTRING' in wkt:
                coords = list(list(float(coord) for coord in coord_str.split(' '))
                              for coord_str in wkt.split('LINESTRING')[1].replace(')', '').replace('(', '').strip().split(','))
                feat = ee.Feature(ee.Geometry.LineString(coords),
                                  feat_dict)

            else:
                raise ValueError('Unsupported geometry type')

            if feat is not None:
                feat_list.append(feat)

        log.lprint('{} intersecting features'.format(str(intersect_count)))

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
                end_year=None,
                geometry=None):

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

        collection = ls_coll(start_year=startYear,
                             end_year=endYear,
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


    site_count = 0
    time0 = datetime.datetime.now()

    chunk = feat_list_chunks[int(chunk_number)]

    # for j, chunk in enumerate(feat_list_chunks[2:3]):
    log.lprint('\n ----------Working on chunk {} --------------\n'.format(str(int(chunk_number) + 1)))

    n_sites = len(chunk)
    sites_list = ee.List(chunk)

    log.lprint('Number of sites: {}'.format(str(n_sites)))

    i = 0
    while i < n_sites:

        time1 = datetime.datetime.now()
        site = sites_list.get(i)

        temp_dicts = []
        try:
            temp_dicts = get_region(site)

        # if any error occurs, print it and break the loop
        except Exception as e:
            log.lprint(e.args[0])

            if type(e.args[0]) == str:

                if 'Earth Engine memory capacity exceeded' in e.args[0]:
                    log.lprint('Waiting 30 secs...'.format(str(wait)))
                    time.sleep(wait)
                    continue

                elif 'ServerNotFoundError' in e.args[0] or \
                        'Unable to find the server' in e.args[0] or \
                        'getaddrinfo failed' in e.args[0] or \
                        'connection attempt failed' in e.args[0]:

                    log.lprint('Waiting 30 secs...'.format(str(wait)))
                    time.sleep(wait)
                    continue

            else:
                continue
        if temp_dicts:
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
                                                                                    t=str(round((time2 - time1)
                                                                                                .total_seconds(), 1))))

        i += 1
        site_count += 1

    log.lprint('\n ----------completed chunk {} --------------\n'.format(str(int(chunk_number) + 1)))

    time0_ = datetime.datetime.now()
    log.lprint('Total Time taken: {t} seconds'.format(t=Timer.display_time((time0_ - time0).total_seconds(),
                                                                           precision=1)))
