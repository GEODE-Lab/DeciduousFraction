/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3_blended"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3_blended"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3_blended"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    alb_samp_tc_elev = ee.FeatureCollection("users/masseyr44/albedo_samples/albedo_samp_loc_based_on_tc"),
    albedo_2015_spr = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2013_2018_60_150_ran_samp"),
    albedo_2015_fal = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2013_2018_240_300_ran_samp"),
    albedo_2015_sum = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2013_2018_150_240_ran_samp"),
    albedo_2010_spr = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2008_2012_60_150_ran_samp"),
    albedo_2010_fal = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2008_2012_240_300_ran_samp"),
    albedo_2010_sum = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2008_2012_150_240_ran_samp"),
    albedo_2005_spr = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2003_2007_60_150_ran_samp"),
    albedo_2005_fal = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2003_2007_240_300_ran_samp"),
    albedo_2005_sum = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2003_2007_150_240_ran_samp"),
    albedo_2000_spr = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2000_2002_60_150_ran_samp"),
    albedo_2000_fal = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2000_2002_240_300_ran_samp"),
    albedo_2000_sum = ee.FeatureCollection("users/masseyr44/albedo_samples_by_tc/albedo_composite_mean_2000_2002_150_240_ran_samp"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3_blended"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
print(albedo_2000_spr.first())

// 2000
var img2000 = decid2000.addBands(tc2000).select([0,1],['decid2000','tc2000'])
var samp2000_sum = img2000.reduceRegions(albedo_2000_sum, ee.Reducer.first(), 30);
var samp2000_spr = img2000.reduceRegions(albedo_2000_spr, ee.Reducer.first(), 30);
var samp2000_fal = img2000.reduceRegions(albedo_2000_fal, ee.Reducer.first(), 30);

Export.table.toDrive({
  collection:samp2000_sum,
  description:'samp2000_sum',
  fileNamePrefix:'samp2000_sum',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2000_spr,
  description:'samp2000_spr',
  fileNamePrefix:'samp2000_spr',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2000_fal,
  description:'samp2000_fal',
  fileNamePrefix:'samp2000_fal',
  folder:'albedo_samp_v2'
})


// 2005
var img2005 = decid2005.addBands(tc2005).select([0,1],['decid2005','tc2005'])
var samp2005_sum = img2005.reduceRegions(albedo_2005_sum, ee.Reducer.first(), 30);
var samp2005_spr = img2005.reduceRegions(albedo_2005_spr, ee.Reducer.first(), 30);
var samp2005_fal = img2005.reduceRegions(albedo_2005_fal, ee.Reducer.first(), 30);

Export.table.toDrive({
  collection:samp2005_sum,
  description:'samp2005_sum',
  fileNamePrefix:'samp2005_sum',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2005_spr,
  description:'samp2005_spr',
  fileNamePrefix:'samp2005_spr',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2005_fal,
  description:'samp2005_fal',
  fileNamePrefix:'samp2005_fal',
  folder:'albedo_samp_v2'
})


// 2010
var img2010 = decid2010.addBands(tc2010).select([0,1],['decid2010','tc2010'])
var samp2010_sum = img2010.reduceRegions(albedo_2010_sum, ee.Reducer.first(), 30);
var samp2010_spr = img2010.reduceRegions(albedo_2010_spr, ee.Reducer.first(), 30);
var samp2010_fal = img2010.reduceRegions(albedo_2010_fal, ee.Reducer.first(), 30);

Export.table.toDrive({
  collection:samp2010_sum,
  description:'samp2010_sum',
  fileNamePrefix:'samp2010_sum',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2010_spr,
  description:'samp2010_spr',
  fileNamePrefix:'samp2010_spr',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2010_fal,
  description:'samp2010_fal',
  fileNamePrefix:'samp2010_fal',
  folder:'albedo_samp_v2'
})



// 2015
var img2015 = decid2015.addBands(tc2015).select([0,1],['decid2015','tc2015'])
var samp2015_sum = img2015.reduceRegions(albedo_2015_sum, ee.Reducer.first(), 30);
var samp2015_spr = img2015.reduceRegions(albedo_2015_spr, ee.Reducer.first(), 30);
var samp2015_fal = img2015.reduceRegions(albedo_2015_fal, ee.Reducer.first(), 30);

Export.table.toDrive({
  collection:samp2015_sum,
  description:'samp2015_sum',
  fileNamePrefix:'samp2015_sum',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2015_spr,
  description:'samp2015_spr',
  fileNamePrefix:'samp2015_spr',
  folder:'albedo_samp_v2'
})
Export.table.toDrive({
  collection:samp2010_fal,
  description:'samp2015_fal',
  fileNamePrefix:'samp2015_fal',
  folder:'albedo_samp_v2'
})
