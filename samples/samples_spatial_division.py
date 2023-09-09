from geosoup import Vector, Handler
import multiprocessing as mp
import json

"""
Script to spatially divide the samples into eastern and western boundaries. 
East and West are defined by eastern and western sides of Manitoba-Ontario border 
"""


east_bounds = {"type": "Polygon",
               "coordinates": [[[-88.92868342469129, 43.88140552252109],
                                [-85.58883967469129, 38.323711003230784],
                                [-79.87594904969129, 37.70049188364389],
                                [-69.94430842469129, 42.40656696303263],
                                [-64.93454279969129, 41.88524780859888],
                                [-58.606417799691286, 42.92358958547362],
                                [-48.762667799691286, 46.7241804827487],
                                [-51.750949049691286, 53.05387833767768],
                                [-59.20289538355753, 58.098307375516235],
                                [-63.99293444605753, 60.73509747139949],
                                [-67.90406725855753, 61.066354971727314],
                                [-72.62818835230753, 62.87277411402012],
                                [-78.42896960230753, 62.83267144776967],
                                [-78.82447741480753, 62.029351321519535],
                                [-79.57154772730753, 58.10991723037259],
                                [-77.37428210230753, 56.72571697779769],
                                [-79.08814928980753, 55.58777104723874],
                                [-81.46119616480753, 55.27609923664135],
                                [-84.60328600855753, 56.105857321452554],
                                [-88.84400866480753, 57.037849002209526],
                                [-95.19410632105753, 52.812842882180924],
                                [-95.17213366480753, 48.94788910435037]]]}

west_bounds = {"type": "Polygon",
               "coordinates": [[[-94.99313654969129, 48.15082483501459],
                                [-95.14694514344129, 48.92190507517494],
                                [-95.14694514344129, 52.80221471852629],
                                [-88.77487483094129, 57.06413861846923],
                                [-90.97214045594129, 57.71540213117909],
                                [-92.53219904969129, 58.7449377860594],
                                [-92.64206233094129, 60.35911691116686],
                                [-88.68698420594129, 62.94481935613294],
                                [-85.69870295594129, 65.32062761180954],
                                [-80.24948420594129, 66.29300926684802],
                                [-78.84323420594129, 67.70076657413327],
                                [-80.24948420594129, 70.04278949806441],
                                [-81.47995295594129, 70.22200493041868],
                                [-86.75339045594129, 70.04278949806441],
                                [-93.08151545594129, 69.58791277052849],
                                [-99.23385920594129, 68.51985942867181],
                                [-103.80417170594129, 68.48765277362025],
                                [-106.61667170594129, 68.99747742277796],
                                [-111.36276545594129, 68.22833903025843],
                                [-113.12057795594129, 68.22833903025843],
                                [-113.99948420594129, 68.80765866061395],
                                [-117.51510920594129, 69.55723713361026],
                                [-122.52487483094129, 70.51726868499823],
                                [-127.35885920594129, 70.92352807693337],
                                [-130.6108123309413, 71.09513206443117],
                                [-140.1908904559413, 70.60501872881767],
                                [-145.8158904559413, 71.37783826758219],
                                [-153.9018279559413, 71.37783826758219],
                                [-159.5268279559413, 71.23699843753144],
                                [-163.5697967059413, 70.63418421010688],
                                [-167.2612029559413, 68.51985942867181],
                                [-168.7553435809413, 65.86537240505295],
                                [-167.6127654559413, 61.13219241507228],
                                [-167.6127654559413, 56.64364983065983],
                                [-167.0854217059413, 52.842048376256116],
                                [-157.5932342059413, 53.15940459266299],
                                [-151.4408904559413, 53.15940459266299],
                                [-143.0912810809413, 52.575800398461965],
                                [-136.2358123309413, 51.549188699400815],
                                [-132.4565154559413, 50.21851600874486],
                                [-127.35885920594129, 49.02286847673588],
                                [-122.08542170594129, 48.03341447135981],
                                [-108.72604670594129, 48.03341447135981]]]}


def get_next_samp_east_west(samp_list):
    for samp_elem in samp_list:
        yield json.dumps(east_bounds), json.dumps(west_bounds), samp_elem


def find_region(args):
    east_json, west_json, samp_dict = args

    east_geom = Vector.get_osgeo_geom(east_json, geom_type='json')
    east_geom.CloseRings()

    west_geom = Vector.get_osgeo_geom(west_json, geom_type='json')
    west_geom.CloseRings()

    samp_geom = Vector.get_osgeo_geom(samp_dict['geom'], geom_type='wkt')

    if east_geom.Intersects(samp_geom):
        return 'east', samp_dict
    elif west_geom.Intersects(samp_geom):
        return 'west', samp_dict
    else:
        return


if __name__ == '__main__':

    infile = "C:/shared" \
             "/projects/NAU/landsat_deciduous/data/samples/" \
             "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples.csv"

    # "all_samp_decid_pre_v1_tile_extracted_v7.csv"

    nprocs = 4
    point_dicts = Handler(infile).read_from_csv(return_dicts=True)

    boreal_bounds = "C:/shared/projects/NAU/landsat_deciduous/data/STUDY_AREA/boreal/" \
                    "NABoreal_boreal_geo_single_geom_buffer_0_1_deg.shp"

    bounds_vector = Vector(boreal_bounds)
    bounds_wkt = bounds_vector.wktlist[0]

    for point_dict in point_dicts[:5]:
        print(point_dict)

    pool = mp.Pool(nprocs)

    point_list = []

    for results in pool.imap_unordered(find_region,
                                       get_next_samp_east_west(point_dicts),
                                       chunksize=500):
        point_list.append(results)

    pool.close()

    east_list = []
    west_list = []
    samp_counter = 0
    bounds_geom = Vector.get_osgeo_geom(bounds_wkt)
    for region, samp_point in point_list:
        print('Processing samp {} of {} - {} '.format(str(samp_counter),
                                                          str(len(point_list)),
                                                          region))
        samp_geom = Vector.get_osgeo_geom(samp_point['geom'], geom_type='wkt')
        if bounds_geom.Intersects(samp_geom):
            if region == 'west':
                west_list.append(samp_point)
            else:
                east_list.append(samp_point)
        samp_counter += 1

    print('East - {} | West - {}'.format(len(east_list), len(west_list)))

    print('Total Number of East samples: {}'.format(str(len(east_list))))
    print('Total Number of West samples: {}'.format(str(len(west_list))))

    east_file = Handler(infile).add_to_filename('_east_boreal_samp')
    west_file = Handler(infile).add_to_filename('_west_boreal_samp')

    Handler().write_to_csv(east_list, outfile=east_file)
    Handler().write_to_csv(west_list, outfile=west_file)
