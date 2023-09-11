/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var samp = ee.FeatureCollection("users/masseyr44/albedo_samples/albedo_samp_loc_based_on_tc"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    decid2000u = ee.Image("users/masseyr44/decid/decid_mosaic_2000_uncertainty_vis_nd_3"),
    decid2005u = ee.Image("users/masseyr44/decid/decid_mosaic_2005_uncertainty_vis_nd_3"),
    decid2010u = ee.Image("users/masseyr44/decid/decid_mosaic_2010_uncertainty_vis_nd_3"),
    tc2000u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_uncertainty_vis_nd"),
    tc2005u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_uncertainty_vis_nd"),
    tc2010u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_uncertainty_vis_nd");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
print(samp.size())


var layerstack = decid2000.addBands(decid2005).addBands(decid2010).addBands(tc2000).addBands(tc2005).addBands(tc2010)
                          .addBands(decid2000u).addBands(decid2005u).addBands(decid2010u).addBands(tc2000u).addBands(tc2005u).addBands(tc2010u)
                          .select([0,1,2,3,4,5,6,7,8,9,10,11],['decid2000','decid2005','decid2010','tc2000','tc2005','tc2010',
                                                               'decid2000u','decid2005u','decid2010u','tc2000u','tc2005u','tc2010u',])
                          
var extract_samp = layerstack.reduceRegions(samp, ee.Reducer.first(), 30 )

Export.table.toDrive({
  collection:extract_samp,
  description:'tc_decid_extract_samp_2000_2005_2010',
  folder:'tc_decid_extract_samp',
  fileNamePrefix:'tc_decid_extract_samp_2000_2005_2010'
})

