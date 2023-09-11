/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    tc = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    land = ee.Image("users/masseyr44/decid/land_extent_NA"),
    geom = 
    /* color: #d63000 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-147.66537702328174, 64.89786061324045],
          [-147.66537702328174, 62.706842518435145],
          [-142.96322858578174, 62.706842518435145],
          [-142.96322858578174, 64.89786061324045]]], null, false);
/***** End of imports. If edited, may not auto-convert in the playground. *****/

var mask = ((tc.gt(20)).multiply(land))
mask=mask.updateMask(mask.gt(0))
Map.addLayer(tc)
Map.addLayer(mask)

var decid_subset = decid.multiply(mask).clip(geom)

Map.addLayer(decid_subset, {min:0, max:100})

Export.image.toDrive({
  image:decid_subset,
  description:'decid_subset',
  folder:'decid_subset',
  fileNamePrefix:'decid_tc25_subset_2010_delta_jn',
  scale:30,
  maxPixels:1e13,
  region:geom
})
