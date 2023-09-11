/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var east1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_prediction_east_vis_nd_2"),
    east2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_prediction_east_vis_nd_2"),
    east2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_prediction_east_vis_nd_2"),
    east2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_east_vis_nd_2"),
    east2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_prediction_east_vis_nd_2"),
    diff2015_2000 = ee.Image("users/masseyr44/decid/decid_diff2_2015_2000_250m"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    all_product = ee.Image("users/masseyr44/all_product_stack_250m"),
    image = ee.Image("users/masseyr44/decid/decid_2010_prediction_vis_nd_2_250m_tc_wtd"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_2000_prediction_vis_nd_2_250m_tc_wtd");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var vis1 = {min:0, max:100, palette:['065D18','FFD905']};
var vis2 = {min:-25, max:25, palette:'FF3600,FFFFFF,0051FF'}

Map.addLayer(decid2015, vis1, 'decid2015')
Map.addLayer(east2015, vis1, 'east2015')

Map.addLayer(decid2010, vis1, 'decid2010')
Map.addLayer(east2010, vis1, 'east2010')






print(all_product)
Map.addLayer(all_product.select(['decid2010']), vis1, 'all_product_Decid')


Map.addLayer(east2015.subtract(east2000),vis2, 'diff2015_2000_')

Map.addLayer(decid2015.subtract(decid2000), vis2, 'diff2015_2000')