/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var bounds = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal"),
    samp1 = ee.FeatureCollection("users/masseyr44/shapefiles/albedo_data_2000_2010_full_by_tc_loc_boreal"),
    image1 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2000_2002_1_90_v3"),
    image2 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2000_2002_90_150_v3"),
    image3 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2000_2002_150_240_v3"),
    image4 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2003_2007_1_90_v3"),
    image5 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2003_2007_90_150_v3"),
    image6 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2003_2007_150_240_v3"),
    image7 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2008_2012_1_90_v3"),
    image8 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2008_2012_90_150_v3"),
    image9 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_50_2008_2012_150_240_v3"),
    image10 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2000_2002_120_180_v2"),
    image11 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2000_2002_180_240_v2"),
    image12 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2000_2002_240_300_v2"),
    image13 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2003_2007_120_180_v2"),
    image14 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2003_2007_180_240_v2"),
    image15 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2003_2007_240_300_v2"),
    image16 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2008_2012_120_180_v2"),
    image17 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2008_2012_180_240_v2"),
    image18 = ee.Image("users/masseyr44/albedo_products/albedo_composite_pctl_90_2008_2012_240_300_v2"),
    decid2000e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_prediction_east_vis_nd_2"),
    decid2005e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_prediction_east_vis_nd_2"),
    decid2010e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_east_vis_nd_2"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2000u = ee.Image("users/masseyr44/decid/decid_mosaic_2000_uncertainty_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2005u = ee.Image("users/masseyr44/decid/decid_mosaic_2005_uncertainty_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    decid2010u = ee.Image("users/masseyr44/decid/decid_mosaic_2010_uncertainty_vis_nd_3"),
    land_extent = ee.Image("users/masseyr44/decid/land_extent_NA"),
    decid2000eu = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_uncertainty_east_vis_nd_2"),
    decid2005eu = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_uncertainty_east_vis_nd_2"),
    decid2010eu = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_uncertainty_east_vis_nd_2");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
//Map.addLayer(bounds,{color:'00ff00'})
//Map.addLayer(samp1,{color:'FF5733'})

decid2005e = decid2005e.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()
decid2010e = decid2010e.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()
decid2000e = decid2000e.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()

decid2005 = decid2005.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()
decid2010 = decid2010.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()
decid2000 = decid2000.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()

var decid2005 = ee.ImageCollection([ decid2005e, decid2005]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)
var decid2010 = ee.ImageCollection([ decid2010e, decid2010]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)
var decid2000 = ee.ImageCollection([ decid2000e, decid2000]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)


decid2005eu = decid2005eu.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()
decid2010eu = decid2010eu.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()
decid2000eu = decid2000eu.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()

decid2005u = decid2005u.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()
decid2010u = decid2010u.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()
decid2000u = decid2000u.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()

var decid2005u = ee.ImageCollection([ decid2005eu, decid2005u]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)
var decid2010u = ee.ImageCollection([ decid2010eu, decid2010u]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)
var decid2000u = ee.ImageCollection([ decid2000eu, decid2000u]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)

var tc_slope = ee.Terrain.slope(tc2010)
var connected_mask = tc_slope.updateMask(tc_slope.lt(18)).multiply(0).add(1).toInt16().connectedPixelCount(255)
connected_mask = connected_mask.multiply(land_extent).updateMask(connected_mask.gt(100)).multiply(0).add(1).toInt16().unmask(0)

var coll = ee.ImageCollection([image1, image2, image3,
                               image4, image5, image6,
                               image7, image8, image9,
                               image10, image11, image12,
                               image13, image14, image15,
                               image16, image17, image18,
                               decid2000, decid2005, decid2010,
                               decid2000u, decid2005u, decid2010u,
                               tc2000, tc2005, tc2010, 
                               land_extent.unmask(0),
                               connected_mask])


//function to output a layerstack given a homogeneous collection
var layer_stack=function(collection){
  var collection_list=collection.toList({count: collection.size()});
  var first=ee.Image(collection.first())
  var nb = collection.size()
  function combine(img, prev){return ee.Image(prev).addBands(img)}
  return collection_list.slice(1,nb).iterate(combine,first);
}

var ls = ee.Image(layer_stack(coll)).rename(["pctl_50_2000_001_090",
                                             "pctl_50_2000_090_150",
                                             "pctl_50_2000_150_240",
                                             "pctl_50_2005_001_090",
                                             "pctl_50_2005_090_150",
                                             "pctl_50_2005_150_240",
                                             "pctl_50_2010_001_090",
                                             "pctl_50_2010_090_150",
                                             "pctl_50_2010_150_240",
                                             "pctl_90_2000_120_180",
                                             "pctl_90_2000_180_240",
                                             "pctl_90_2000_240_300",
                                             "pctl_90_2005_120_180",
                                             "pctl_90_2005_180_240",
                                             "pctl_90_2005_240_300",
                                             "pctl_90_2010_120_180",
                                             "pctl_90_2010_180_240",
                                             "pctl_90_2010_240_300",
                                             "decid2000", "decid2005", "decid2010",
                                             "decid2000u", "decid2005u", "decid2010u",
                                             "tc2000", "tc2005", "tc2010",
                                             "land_extent",
                                             "connected_mask_val18"])

print(ls)

print(samp1.size())

//var out_samp = ls.sampleRegions(samp1, null, 30)

var out_samp = ls.sample(samp1,30)

print(out_samp.first())


Export.table.toDrive({collection: out_samp,
                      description: 'albedo_data_2000_2010_full_by_tc_loc_boreal',
                      fileNamePrefix: 'albedo_data_2000_2010_full_by_tc_loc_boreal_conn_val18_v2',
                      folder: 'albedo_data_2000_2010_full_by_tc'
})

Map.addLayer(tc2010.multiply(land_extent),{min:0, max:100, palette: 'AF0606,F3A916,000FFF'})

Map.addLayer(land_extent.unmask(0),{min:0, max:1})
Map.addLayer(connected_mask,{min:0, max:1})

