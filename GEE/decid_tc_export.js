/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
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
    tc2010u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_uncertainty_vis_nd"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd"),
    tc2015u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_uncertainty_vis_nd"),
    land = ee.Image("users/masseyr44/decid/land_extent_NA"),
    geometry = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-167.58646916240514, 69.26102141879815],
          [-169.16850041240514, 61.73804050615485],
          [-174.96928166240514, 55.73485657800552],
          [-178.48490666240514, 51.952744505542185],
          [-176.55131291240514, 48.93153813252652],
          [-153.34818791240514, 49.39132812974774],
          [-143.32865666240514, 42.56321385293061],
          [-123.46537541240512, 39.78534211544716],
          [-94.81303166240512, 40.45741570367504],
          [-72.13725041240514, 38.69624780388922],
          [-62.82084416240513, 40.45741570367504],
          [-47.87943791240513, 46.56831917462663],
          [-47.87943791240513, 52.704697787504166],
          [-57.89896916240513, 61.10743666455614],
          [-77.41068791240514, 66.7973302677825],
          [-110.98490666240512, 71.36146386172412],
          [-151.06303166240514, 71.64032669069202],
          [-161.78568791240514, 71.41756137944405]]]),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    decid2015u = ee.Image("users/masseyr44/decid/decid_mosaic_2015_uncertainty_vis_nd_3"),
    canada_extent = ee.Image("users/masseyr44/decid/canada_extent"),
    tc1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_prediction_vis_nd"),
    tc1992u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_uncertainty_vis_nd"),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3"),
    decid1992u = ee.Image("users/masseyr44/decid/decid_mosaic_1992_uncertainty_vis_nd_3");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var tc_mask = tc2000.gt(25).add(tc2015.gt(25)).gt(0)
tc_mask = tc_mask.updateMask(tc_mask).multiply(land)

Map.addLayer(tc_mask, {min:0, max:1},'tc_mask')


Export.image.toDrive({
  image:tc_mask,
  description:'tc_mask_2000_2015_thresh25',
  folder: 'final_exports',
  fileNamePrefix: 'tc_mask_2000_2015_tcthresh25',
  region: geometry,
  scale:30,
  maxPixels:1e13
})


var decid_diff = (decid2015.int16()).subtract(decid2000.int16()).multiply(tc_mask.int16())
Map.addLayer(decid_diff, {min:-100, max:100},'decid_diff')

Export.image.toDrive({
  image:decid_diff,
  description:'decid_diff_2000_2015_tcthresh25',
  folder: 'final_exports',
  fileNamePrefix: 'decid_diff_2000_2015_tcthresh25',
  region: geometry,
  scale:30,
  maxPixels:1e13
})

var tc_diff = (tc2015.int16()).subtract(tc2000.int16()).multiply(tc_mask.int16())
Map.addLayer(tc_diff, {min:-100, max:100},'tc_diff')

Export.image.toDrive({
  image:tc_diff,
  description:'tc_diff_2000_2015_tcthresh25',
  folder: 'final_exports',
  fileNamePrefix: 'tc_diff_2000_2015_tcthresh25',
  region: geometry,
  scale:30,
  maxPixels:1e13
})


// Canada 1995 - 2015
var tc_mask2 = tc1992.gt(25).add(tc2015.gt(25)).add(tc2000.gt(25)).gt(0).multiply(canada_extent)
tc_mask2 = tc_mask2.updateMask(tc_mask2).multiply(land)

Map.addLayer(tc_mask2, {min:0, max:1},'tc_mask2')


Export.image.toDrive({
  image:tc_mask2,
  description:'tc_mask_1992_2015_thresh25',
  folder: 'final_exports',
  fileNamePrefix: 'tc_mask_1992_2015_tcthresh25',
  region: geometry,
  scale:30,
  maxPixels:1e13
})


var decid_diff = (decid2015.int16()).subtract(decid1992.int16()).multiply(tc_mask2.int16())
Map.addLayer(decid_diff, {min:-100, max:100},'decid_diff2')

Export.image.toDrive({
  image:decid_diff,
  description:'decid_diff_1992_2015_tcthresh25',
  folder: 'final_exports',
  fileNamePrefix: 'decid_diff_1992_2015_tcthresh25',
  region: geometry,
  scale:30,
  maxPixels:1e13
})

var tc_diff = (tc2015.int16()).subtract(tc1992.int16()).multiply(tc_mask2.int16())
Map.addLayer(tc_diff, {min:-100, max:100},'tc_diff2')

Export.image.toDrive({
  image:tc_diff,
  description:'tc_diff_1992_2015_tcthresh25',
  folder: 'final_exports',
  fileNamePrefix: 'tc_diff_1992_2015_tcthresh25',
  region: geometry,
  scale:30,
  maxPixels:1e13
})



