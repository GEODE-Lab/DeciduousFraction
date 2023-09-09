import ee
import datetime
from geosoup import *
from eehelper import *


if __name__ == '__main__':

    ee.Initialize()

    folder = "c:/temp/decid_1/"

    scale = 250
    cutoff = 4000
    fire_year_limit = 1970

    Handler(dirname=folder).dir_create()

    OUTFILE = folder + \
        'gee_fire_data_extract_{}_v{}.csv'.format(str(scale),datetime.datetime.now().isoformat()
                                               .split('.')[0].replace('-', '_').replace(':', '_'))

    logfile = OUTFILE.split('.csv')[0] + '.log'

    log = Logger('SAMP',
                 filename=logfile,
                 stream=True)

    log.lprint('Outfile: {}'.format(OUTFILE))
    log.lprint('Logfile: {}'.format(logfile))

    decid_layer1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3")
    decid_layer2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3")
    decid_layer2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3")
    decid_layer2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3")
    decid_layer2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3")

    layer_stack = 0


    ak_fire = ee.FeatureCollection("users/masseyr44/decid/AK_fire_database")
    ak_interior = ee.FeatureCollection("users/masseyr44/decid/alaska_interior_zones")

    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_MM").rename('tree_cover')
    epa_l3 = ee.FeatureCollection("users/masseyr44/decid/alaska_EPA_L3")
    elevation = ee.Image('USGS/GMTED2010').rename('elevation')
    slope = ee.Terrain.slope(elevation)
    aspect = ee.Terrain.aspect(elevation)

    all_bands = ['id', 'EPA_DESIG', 'FIREID', 'FireYear',
                 'decid_frac', 'latitude', 'longitude', 'elevation', 'slope', 'aspect', 'tree_cover']

    epa_reg_list = ['3.1.1', '3.1.2', '3.1.3', '6.1.1', '6.1.3']

    log.lprint('EPA ecozone classes: {}'.format(str(epa_reg_list)))

    remap_epa_list = list(int(elem.replace('.', '')) for elem in epa_reg_list)

    epa_idx = list(range(len(epa_reg_list)))

    def reg_iterator(elem, coll):
        temp_coll = ee.FeatureCollection(epa_l3).filterMetadata('NA_L3CODE', 'equals', ee.List(epa_reg_list).get(elem))
        return ee.FeatureCollection(coll).merge(temp_coll.map(lambda x:
                                                              ee.Feature(x).set('NA_L3CODE',
                                                                                ee.List(remap_epa_list).get(elem))))

    epa_l3 = ee.FeatureCollection(ee.List(epa_idx).iterate(reg_iterator,
                                                           ee.FeatureCollection([])))

    epa_ras = epa_l3.reduceToImage(['NA_L3CODE'], ee.Reducer.first()).rename('EPA_DESIG')
    epa_bounds = epa_l3.union()

    bounds = ee.Feature(ak_interior.first()).geometry().intersection(epa_bounds)

    mask_classes = ee.List([11, 12, 21, 22, 23, 24, 31, 82])

    remap_nlcd = mask_classes.map(lambda x:
                                  ee.Number(x).multiply(0))

    nlcd_mask = nlcd.remap(mask_classes, remap_nlcd)

    nlcd_mask = nlcd_mask.updateMask(nlcd_mask.eq(0)).unmask(1)
    nlcd_mask = nlcd_mask.updateMask(nlcd_mask.eq(1))

    decid_layer = decid_layer.multiply(nlcd_mask).rename('decid_frac').clip(bounds)

    ak_fire = ak_fire.map(lambda x: ee.Feature(x).set('FireYear', ee.Number.parse(ee.Feature(x).get('FireYear'))))
    ak_fire = ak_fire.filterMetadata('FireYear', 'not_less_than', fire_year_limit).filterBounds(bounds)

    topo_image = elevation.addBands(slope.rename('slope')).addBands(aspect.rename('aspect'))

    data_cube = decid_layer.addBands(ee.Image.pixelLonLat()).addBands(epa_ras).addBands(topo_image).addBands(tc2000)
    data_cube = data_cube.clip(bounds)

    data_cube_meta = data_cube.getInfo()

    bnames = list(str(meta['id']) for meta in data_cube_meta['bands'])

    log.lprint('Band_names: {}'.format(str(bnames)))

    ak_fire = ak_fire.toList(ak_fire.size())
    n_fires = ak_fire.size().getInfo()

    for i in range(n_fires):
        time1 = datetime.datetime.now()

        temp_data = data_cube.sampleRegions(ee.FeatureCollection([ak_fire.get(i)]), None, scale)
        temp_data = temp_data.toList(temp_data.size())
        try:
            temp_list = temp_data.getInfo()
        except Exception as e:
            temp_list = list()
            if 'Collection query aborted after accumulating over 5000 elements' in e.args[0]:

                n_temp_feat = temp_data.size().getInfo()
                if n_temp_feat > cutoff:

                    feat_slice_list = list((i*cutoff, (i+1)*cutoff) for i in range(n_temp_feat // cutoff))

                    if n_temp_feat % cutoff > 0:
                        feat_slice_list += [(feat_slice_list[-1][1], feat_slice_list[-1][1] + (n_temp_feat % cutoff))]

                    for feat_slice in feat_slice_list:
                        temp_list += temp_data.slice(feat_slice[0], feat_slice[1]).getInfo()

        time2 = datetime.datetime.now()

        log.lprint('Time taken for {} pixels, '.format(str(len(temp_list))) +
                   ' ({ii} of {nn} fires): {t} seconds'.format(ii=str(i + 1),
                                                               nn=str(n_fires),
                                                               t=str(round(
                                                                     (time2 - time1).total_seconds(), 1))))

        out_list = list()
        for feat in temp_list:
            out_dict = dict()
            for key in all_bands:
                if key == 'EPA_DESIG':
                    out_dict[key] = str(int(feat['properties'][key]))
                elif key == 'id':
                    out_dict[key] = feat[key]
                elif key == 'tree_cover':
                    out_dict[key] = int(round(feat['properties'][key]))
                else:
                    out_dict[key] = feat['properties'][key]

            out_list.append(out_dict)

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

