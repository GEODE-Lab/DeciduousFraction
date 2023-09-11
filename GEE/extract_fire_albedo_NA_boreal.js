/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var land = ee.Image("users/masseyr44/decid/land_extent_NA"),
    tiles = ee.FeatureCollection("users/masseyr44/shapefiles/decid_tc_layerstack_tiles"),
    ak_fire = ee.FeatureCollection("users/masseyr44/shapefiles/ak_fire_multi"),
    alb_sum2015_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_sum_albedo_vis_v2"),
    alb_sum2000_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_sum_albedo_vis_v2"),
    alb_fall2000_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_fall_albedo_vis_v2"),
    boreal_bounds = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal"),
    ak_fire_all = ee.FeatureCollection("users/masseyr44/shapefiles/AK_fire_database"),
    ak_fire_new = ee.FeatureCollection("users/masseyr44/shapefiles/AlaskaFireAreaHistory_1940_2018"),
    can_fire = ee.FeatureCollection("users/masseyr44/shapefiles/Can_fire"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    alb_fall2015_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_fall_albedo_vis_v2"),
    alb_spr2015_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_spr_albedo_vis_v2"),
    alb_spr2000_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_spr_albedo_vis_v2"),
    cam5_apr = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_apr_250m"),
    cam5_aug = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_aug_250m"),
    cam5_jul = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_jul_250m"),
    cam5_jun = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_jun_250m"),
    cam5_may = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_may_250m"),
    cam5_nov = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_nov_250m"),
    cam5_oct = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_oct_250m"),
    cam5_sep = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_sep_250m"),
    fire_ak = ee.Image("users/masseyr44/decid/FireAreaHistory_1940_2018_v2_30m"),
    fire_can = ee.Image("users/masseyr44/decid/NFDB_poly_20171106_gt500ha_geo_v2_30m"),
    geometry = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-178.87095379237064, 72.45163111786071],
          [179.01967120762936, 49.95727882073875],
          [-156.37095379237064, 43.45975470768747],
          [-114.88657879237064, 41.25185262811164],
          [-72.5229153112474, 26.713481333704397],
          [-39.30064129237064, 39.103271032573964],
          [-49.14439129237064, 64.40100690048561],
          [-64.78892254237064, 70.32190977142183]]]),
    top_fire_layer = ee.Image("users/masseyr44/decid/NA_fire_top_layer_30m_lzw"),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3_blended"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3_blended"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3_blended"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3_blended"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3_blended"),
    alb_fall2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_fall_albedo_vis_uncert"),
    alb_spr2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_spr_albedo_vis_uncert"),
    alb_sum2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_sum_albedo_vis_uncert"),
    alb_fall2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_fall_albedo_vis_uncert"),
    alb_spr2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_spr_albedo_vis_uncert"),
    alb_sum2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_sum_albedo_vis_uncert"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
Map.setOptions('SATELLITE')

var uncert_calc = function(img_old, img_new, uncert_old, uncert_new){
  return ee.Image(0.02)
           .multiply((ee.Image(img_old).toFloat()).multiply(ee.Image(uncert_new).toFloat())
                        .add((ee.Image(img_new)).toFloat().multiply(ee.Image(uncert_old).toFloat())))
           //.divide((ee.Image(img_old).toFloat()).multiply(ee.Image(img_old).toFloat())).abs()
}

var change_calc = function(img_old, img_new){
  return ((ee.Image(img_new)).subtract(ee.Image(img_old)))//.divide(ee.Image(img_old).toFloat())
}

var vis_decid = {min:0, max:100, palette:'286F09,ECC519'};
var vis_decid_diff = {min:-0.25, max:0.25, palette:'286F09,ECC519'};
var vis_tc = {min:0, max:100, palette:'B62809,FFC560,1178C8'};
var vis_tc_diff = {min:-0.25, max:0.25, palette:'B62809,FFC560,1178C8'};

var boreal_geom = boreal_bounds.geometry();

var top_fire_layer = top_fire_layer.updateMask(top_fire_layer.neq(0)).rename('top_fire_layer').toFloat();
//Map.addLayer(top_fire_layer,{min:1900, max: 2018, palette:'A8FB9E,F4DD36,0B3D05'},'top_fire_layer')

var tc_max = ee.ImageCollection([tc2000, tc2005, tc2010, tc2015]).reduce(ee.Reducer.max()); //
var tc_mask = ee.Image(1).updateMask(tc_max.gt(25));


var fall_diff = change_calc(alb_fall2000_v2, alb_fall2015_v2).updateMask(tc_mask).multiply(land).clip(boreal_bounds);
var fall_udiff = uncert_calc(alb_fall2000_v2, alb_fall2015_v2, alb_fall2000_uncert, alb_fall2015_uncert).updateMask(tc_mask).clip(boreal_bounds);
//Map.addLayer(fall_diff, {min:-.5, max:.5, palette: 'B62809,FFC560,1178C8'}, 'fall_alb_diff', true);
//Map.addLayer(fall_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'fall_alb_udiff', true);

var sum_diff = change_calc(alb_sum2000_v2, alb_sum2015_v2).updateMask(tc_mask).multiply(land).clip(boreal_bounds);
var sum_udiff = uncert_calc(alb_sum2000_v2, alb_sum2015_v2, alb_fall2000_uncert, alb_fall2015_uncert).updateMask(tc_mask).clip(boreal_bounds);
//Map.addLayer(sum_diff, {min:-.25, max:.25, palette: 'B62809,FFC560,1178C8'}, 'summer_alb_diff', true);
//Map.addLayer(sum_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'summer_alb_udiff', true);

var spr_diff = change_calc(alb_spr2000_v2, alb_spr2015_v2).updateMask(tc_mask).multiply(land).clip(boreal_bounds);
var spr_udiff = uncert_calc(alb_spr2000_v2, alb_spr2015_v2, alb_spr2015_uncert, alb_spr2015_uncert).updateMask(tc_mask).clip(boreal_bounds);
//Map.addLayer(spr_diff, {min:-.5, max:.5, palette: 'B62809,FFC560,1178C8'}, 'spring_alb_diff', true);
//Map.addLayer(spr_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'spring_alb_udiff', true);

var tc_diff = tc2015.subtract(tc2000).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);
//var tc_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5) * 0.5',{'a': tc2000u.toFloat().divide(2.0), 'b': tc2015u.toFloat().divide(2.0)}).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);
//Map.addLayer(tc_diff,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'tc_diff');

var decid_diff = ee.Image(decid2015).subtract(ee.Image(decid2000)).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);
//var decid_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5) * 0.5',{'a': decid2000u.toFloat().divide(2.0), 'b': decid2015u.toFloat().divide(2.0)}).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);
//Map.addLayer(decid_diff,vis_decid_diff,'decid_diff');


//Map.addLayer(decid2000.updateMask(tc_mask).multiply(land),vis_decid,'decid2000', false);
//Map.addLayer(decid2015.updateMask(tc_mask).multiply(land),vis_decid,'decid2015', false);

//Map.addLayer(tc2000,vis_tc,'tc2000', false);
//Map.addLayer(tc2015,vis_tc,'tc2015', false);

var spr_kernel = ee.ImageCollection([cam5_apr, cam5_may]).reduce(ee.Reducer.mean()).toFloat();
var sum_kernel = ee.ImageCollection([cam5_jun, cam5_jul, cam5_aug]).reduce(ee.Reducer.mean()).toFloat();
var fall_kernel = ee.ImageCollection([cam5_sep, cam5_oct]).reduce(ee.Reducer.mean()).toFloat();


var sum_forc = sum_kernel.multiply(sum_diff);
var spr_forc = spr_kernel.multiply(spr_diff);
var fall_forc = fall_kernel.multiply(fall_diff);

//Map.addLayer(sum_forc,{min:-.25, max:.25, palette:'B62809,FFC560,1178C8'},'sum');
//Map.addLayer(spr_forc,{min:-5, max:5, palette:'B62809,FFC560,1178C8'},'spr');
//Map.addLayer(fall_forc,{min:-2.5, max:2.5, palette:'B62809,FFC560,1178C8'},'fall');

var sum_uforc = sum_kernel.multiply(sum_udiff).abs();
var spr_uforc = spr_kernel.multiply(spr_udiff).abs();
var fall_uforc = fall_kernel.multiply(fall_udiff).abs();



//Map.addLayer(sum_uforc,{min:-.1, max:.1, palette:'B62809,FFC560,1178C8'},'sum_u');
//Map.addLayer(spr_uforc,{min:-.5, max:.5, palette:'B62809,FFC560,1178C8'},'spr_u');
//Map.addLayer(fall_uforc,{min:-.25, max:.25, palette:'B62809,FFC560,1178C8'},'fall_u');
/*
var forcing_seasonal = spr_forc.addBands(spr_uforc)
                               .addBands(sum_forc)
                               .addBands(sum_uforc)
                               .addBands(fall_forc)
                               .addBands(fall_uforc)
                               .addBands(tc_diff)
                               .addBands(decid_diff)
                               .rename([
                                 'spr_forc',
                                 'spr_uforc',
                                 'sum_forc',
                                 'sum_uforc',
                                 'fall_forc',
                                 'fall_uforc',
                                 'tc_diff',
                                 'decid_diff',
                               ]).toFloat();
                               
*/

var forcing_seasonal = spr_diff
                        .addBands(sum_diff)
                        .addBands(fall_diff)
                        .rename([
                         'spr_diff',
                         'sum_diff',
                         'fall_diff',
                        ])
                        
                        //.toFloat();
                       //.addBands(spr_udiff)
                       //.addBands(sum_udiff)
                       //.addBands(fall_udiff)
                       //.addBands(tc_diff)
                       //.addBands(decid_diff)
                       //  'spr_udiff',
                       //  'sum_udiff',
                       //  'fall_udiff',
                       //  'tc_diff',
                       //  'decid_diff',
                       
                               

//Map.addLayer(forcing_seasonal)
print(forcing_seasonal);




Export.image.toDrive({
  image:forcing_seasonal,
  region:geometry,
  scale:30,
  maxPixels:1e13,
  folder:'alb_diff_raster_30m_2000_2015',
  fileNamePrefix:'alb_diff_raster_30m_2000_2015',
  description:'alb_diff_raster_30m_2000_2015'
});




Export.image.toDrive({
  image:spr_forc,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'spr_forc_2000_2015',
  description:'spr_forc_2000_2015'
});
Export.image.toDrive({
  image:spr_uforc,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'spr_uforc_2000_2015',
  description:'spr_uforc_2000_2015'
});


Export.image.toDrive({
  image:sum_forc,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'sum_forc_2000_2015',
  description:'sum_forc_2000_2015'
});
Export.image.toDrive({
  image:sum_uforc,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'sum_uforc_2000_2015',
  description:'sum_uforc_2000_2015'
});


Export.image.toDrive({
  image:fall_forc,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'fall_forc_2000_2015',
  description:'fall_forc_2000_2015'
});
Export.image.toDrive({
  image:fall_uforc,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'fall_uforc_2000_2015',
  description:'fall_uforc_2000_2015'
});


Export.image.toDrive({
  image:decid_diff,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'decid_diff_2000_2015',
  description:'decid_diff_2000_2015'
});

Export.image.toDrive({
  image:tc_diff,
  region:geometry,
  scale:250,
  maxPixels:1e13,
  folder:'forcing_raster_250m_v2',
  fileNamePrefix:'tc_diff_2000_2015',
  description:'tc_diff_2000_2015'
});


//print(ak_fire_new.first())
//print(can_fire.first())

//Map.addLayer(ak_fire_new)
//Map.addLayer(can_fire)

var ak_fire_sample = ak_fire_new.map(function(feat){return ee.Feature(feat.geometry(), {'year': feat.get('FIREYEAR'), 
                                                                                        'area': ee.Number(feat.get('ACRES')).multiply(0.4047),
                                                                                        'featid': feat.get('FIREID')})});
                                                                                        
print(ak_fire_sample.first());

var can_fire_sample = can_fire.map(function(feat){return ee.Feature(feat.geometry(), {'year': feat.get('YEAR'), 
                                                                                        'area': ee.Number(feat.get('SIZE_HA')),
                                                                                        'featid': feat.get('FIRE_ID')})});
                                                                                        
var fire_samp = can_fire_sample.merge(ak_fire_sample)

print(ak_fire_sample);

print(fire_samp.first());

//var geom = fire_samp.first().geometry()
//var fire_area_first = ee.Image.pixelArea().reduceRegion(ee.Reducer.sum(), geom, 30)
//print(fire_area_first)
//throw('stop')

var grab_top_layer = function(feat){
  
  var _year = feat.get('year')
  var _masked_img = forcing_seasonal.updateMask(top_fire_layer.eq(ee.Number(_year))).multiply(ee.Image.pixelArea())
  var fire_area = ee.Image.pixelArea().reduceRegion(ee.Reducer.sum(), feat.geometry(), 30, null, null, false, 1e13)

  return ee.Feature(null, _masked_img.divide(ee.Number(fire_area.get('area'))).reduceRegion(ee.Reducer.sum(), feat.geometry(), 30, null, null, false, 1e13).combine(
                                                                                                {'year': feat.get('year'), 
                                                                                                 'area_rep': feat.get('area'),
                                                                                                 'area_calc': ee.Number(fire_area.get('area')).divide(10000.0),
                                                                                                 'featid': feat.get('featid')}
                                                                                              ))
  
};

var grab_top_layer2 = function(feat){
  
  var _year = feat.get('year')
  var _masked_img = forcing_seasonal.updateMask(top_fire_layer.eq(ee.Number.parse(_year))).multiply(ee.Image.pixelArea())
  var fire_area = ee.Image.pixelArea().reduceRegion(ee.Reducer.sum(), feat.geometry(), 30, null, null, false, 1e13)

  return ee.Feature(null, _masked_img.divide(ee.Number(fire_area.get('area'))).reduceRegion(ee.Reducer.sum(), feat.geometry(), 30, null, null, false, 1e13).combine(
                                                                                                {'year': feat.get('year'), 
                                                                                                 'area_rep': feat.get('area'),
                                                                                                 'area_calc': ee.Number(fire_area.get('area')).divide(10000.0),
                                                                                                 'featid': feat.get('featid')}
                                                                                              ))
  
};


print(fire_samp.size());

var can_fire_list = can_fire_sample.toList(60000);

var fire_list1 = can_fire_list.slice(0, 10000);
var fire_list2 = can_fire_list.slice(10001, 20000);
var fire_list3 = can_fire_list.slice(20001, 30000);
var fire_list4 = can_fire_list.slice(30001, 40000);
var fire_list5 = can_fire_list.slice(40001, 50000);
var fire_list6 = can_fire_list.slice(50001, 60000);


var forc_samp1 = ee.FeatureCollection(fire_list1).map(grab_top_layer);
var forc_samp2 = ee.FeatureCollection(fire_list2).map(grab_top_layer);
var forc_samp3 = ee.FeatureCollection(fire_list3).map(grab_top_layer);
var forc_samp4 = ee.FeatureCollection(fire_list4).map(grab_top_layer);
var forc_samp5 = ee.FeatureCollection(fire_list5).map(grab_top_layer);
var forc_samp6 = ee.FeatureCollection(fire_list6).map(grab_top_layer);

var ak_fire_list = ak_fire_sample.toList(5000);
var ak_forc_samp = ee.FeatureCollection(ak_fire_list).map(grab_top_layer2);

print(ak_forc_samp.first());

Export.table.toDrive({
  collection: forc_samp1,
  description: 'alb_samples1',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples1'
});

Export.table.toDrive({
  collection: forc_samp2,
  description: 'alb_samples2',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples2'
});

Export.table.toDrive({
  collection: forc_samp3,
  description: 'alb_samples3',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples3'
});

Export.table.toDrive({
  collection: forc_samp4,
  description: 'alb_samples4',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples4'
});

Export.table.toDrive({
  collection: forc_samp5,
  description: 'alb_samples5',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples5'
});

Export.table.toDrive({
  collection: forc_samp6,
  description: 'alb_samples6',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples6'
});


Export.table.toDrive({
  collection: ak_forc_samp,
  description: 'alb_samples7',
  folder: 'alb_samples_v3',
  fileNamePrefix: 'alb_samples7'
});

Export.image.toDrive({
  image:forcing_seasonal,
  region:geometry,
  scale:30,
  maxPixels:1e13,
  folder:'forcing_layerstack_2000_2015',
  fileNamePrefix:'forcing_layerstack_2000_2015_sum_spr_fall',
  description:'forcing_layerstack_2000_2015_sum_spr_fall'
});