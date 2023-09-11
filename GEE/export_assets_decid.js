/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var geom = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-103.725390625, 65.41473629898074],
          [-103.725390625, 40.601189653480844],
          [-50.11210937500001, 40.601189653480844],
          [-50.11210937500001, 65.41473629898074]]], null, false),
    geom2 = 
    /* color: #98ff00 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-173.69024127947134, 74.66998154063057],
          [-173.69024127947134, 40.67588720157382],
          [-51.69805377947135, 40.67588720157382],
          [-51.69805377947135, 74.66998154063057]]], null, false);
/***** End of imports. If edited, may not auto-convert in the playground. *****/

var e1992 =  ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_prediction_east_vis_nd_2')
var e1992u = ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_uncertainty_east_vis_nd_2')
var e2000 =  ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_prediction_east_vis_nd_2')
var e2000u = ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_uncertainty_east_vis_nd_2')
var e2005 =  ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_prediction_east_vis_nd_2')
var e2005u = ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_uncertainty_east_vis_nd_2')
var e2010 =  ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_east_vis_nd_2')
var e2010u = ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_uncertainty_east_vis_nd_2')
var e2015 =  ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_prediction_east_vis_nd_2')
var e2015u = ee.Image('users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_uncertainty_east_vis_nd_2')

Export.image.toDrive({image:e1992,description:'e1992',folder:'gee_download',fileNamePrefix:'decid_boreal_1992_prediction_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e1992u',folder:'gee_download',fileNamePrefix:'decid_boreal_1992_uncertainty_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2000',folder:'gee_download',fileNamePrefix:'decid_boreal_2000_prediction_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2000u',folder:'gee_download',fileNamePrefix:'decid_boreal_2000_uncertainty_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2005',folder:'gee_download',fileNamePrefix:'decid_boreal_2005_prediction_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2005u',folder:'gee_download',fileNamePrefix:'decid_boreal_2005_uncertainty_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2010',folder:'gee_download',fileNamePrefix:'decid_boreal_2010_prediction_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2010u',folder:'gee_download',fileNamePrefix:'decid_boreal_2010_uncertainty_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2015',folder:'gee_download',fileNamePrefix:'decid_boreal_2015_prediction_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})
Export.image.toDrive({image:e1992,description:'e2015u',folder:'gee_download',fileNamePrefix:'decid_boreal_2015_uncertainty_east_vis_nd_2',maxPixels:1e13,scale:30,region:geom})

var w1992 =  ee.Image('users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3')
var w1992u = ee.Image('users/masseyr44/decid/decid_mosaic_1992_uncertainty_vis_nd_3')
var w2000 =  ee.Image('users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3')
var w2000u = ee.Image('users/masseyr44/decid/decid_mosaic_2000_uncertainty_vis_nd_3')
var w2005 =  ee.Image('users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3')
var w2005u = ee.Image('users/masseyr44/decid/decid_mosaic_2005_uncertainty_vis_nd_3')
var w2010 =  ee.Image('users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3')
var w2010u = ee.Image('users/masseyr44/decid/decid_mosaic_2010_uncertainty_vis_nd_3')
var w2015 =  ee.Image('users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3')
var w2015u = ee.Image('users/masseyr44/decid/decid_mosaic_2015_uncertainty_vis_nd_3')

Export.image.toDrive({image:w1992,description:'w1992',folder:'gee_download',fileNamePrefix:'decid_mosaic_1992_prediction_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w1992u,description:'w1992u',folder:'gee_download',fileNamePrefix:'decid_mosaic_1992_uncertainty_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2000,description:'w2000',folder:'gee_download',fileNamePrefix:'decid_mosaic_2000_prediction_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2000u,description:'w2000u',folder:'gee_download',fileNamePrefix:'decid_mosaic_2000_uncertainty_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2005,description:'w2005',folder:'gee_download',fileNamePrefix:'decid_mosaic_2005_prediction_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2005u,description:'w2005u',folder:'gee_download',fileNamePrefix:'decid_mosaic_2005_uncertainty_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2010,description:'w2010',folder:'gee_download',fileNamePrefix:'decid_mosaic_2010_prediction_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2010u,description:'w2010u',folder:'gee_download',fileNamePrefix:'decid_mosaic_2010_uncertainty_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2015,description:'w2015',folder:'gee_download',fileNamePrefix:'decid_mosaic_2015_prediction_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
Export.image.toDrive({image:w2015u,description:'w2015u',folder:'gee_download',fileNamePrefix:'decid_mosaic_2015_uncertainty_vis_nd_3_west',maxPixels:1e13,scale:30,region:geom2})
