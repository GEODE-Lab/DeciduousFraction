/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid1992e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_prediction_east_vis_nd_2"),
    decid1992ue = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_uncertainty_east_vis_nd_2"),
    tc1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_prediction_vis_nd"),
    tc1992u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_uncertainty_vis_nd"),
    decid2000e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_prediction_east_vis_nd_2"),
    decid2000ue = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_uncertainty_east_vis_nd_2"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    tc2000u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_uncertainty_vis_nd"),
    decid2005e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_prediction_east_vis_nd_2"),
    decid2005ue = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_uncertainty_east_vis_nd_2"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2005u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_uncertainty_vis_nd"),
    decid2010e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_east_vis_nd_2"),
    decid2010ue = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_uncertainty_east_vis_nd_2"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    tc2010u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_uncertainty_vis_nd"),
    decid2015e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_prediction_east_vis_nd_2"),
    decid2015ue = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_uncertainty_east_vis_nd_2"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd"),
    tc2015u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_uncertainty_vis_nd"),
    land = ee.Image("users/masseyr44/decid/land_extent_NA"),
    aoi = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-177.99296875, 52.14877137510196],
          [-176.850390625, 50.108366999925316],
          [-158.30546875, 51.33244245340349],
          [-153.647265625, 54.45896998912166],
          [-148.9890625, 58.25326897668989],
          [-143.627734375, 58.02128886991836],
          [-138.002734375, 55.86462661831999],
          [-130.88359375, 43.31132324614187],
          [-126.66484374999999, 41.23045273822011],
          [-117.17265624999999, 40.89912063003474],
          [-102.31914062499999, 40.69952053267202],
          [-85.18046874999999, 40.8326539558715],
          [-70.06328124999999, 40.164322656624634],
          [-56.87968749999999, 42.01882877740705],
          [-49.40898437499999, 46.48528231613707],
          [-50.55156249999999, 53.58120112814268],
          [-57.75859374999999, 60.361013236511035],
          [-66.63554687499999, 63.77407219033945],
          [-79.46757812499999, 63.54006870341751],
          [-85.35624999999999, 60.31751940314716],
          [-88.95976562499999, 62.786227819040334],
          [-93.00273437499999, 66.85359819328747],
          [-101.26445312499999, 68.71352862708153],
          [-115.76640624999999, 70.89603696283798],
          [-126.31328124999999, 71.40710625396565],
          [-140.991015625, 71.6299925501241],
          [-151.8015625, 72.04096932486706],
          [-159.799609375, 71.15324093828652],
          [-168.6765625, 68.16447355544426],
          [-169.116015625, 65.21191132858353],
          [-173.42265625, 64.08308592288913],
          [-178.69609375000002, 59.16616942219271]]]),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3"),
    decid1992u = ee.Image("users/masseyr44/decid/decid_mosaic_1992_uncertainty_vis_nd_3"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2000u = ee.Image("users/masseyr44/decid/decid_mosaic_2000_uncertainty_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2005u = ee.Image("users/masseyr44/decid/decid_mosaic_2005_uncertainty_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    decid2010u = ee.Image("users/masseyr44/decid/decid_mosaic_2010_uncertainty_vis_nd_3"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    decid2015u = ee.Image("users/masseyr44/decid/decid_mosaic_2015_uncertainty_vis_nd_3");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
land = land.toInt16()

//Map.addLayer(decid2015e, {min:0, max:100})
decid1992 = decid1992.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid1992u = decid1992u.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2000 = decid2000.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2000u = decid2000u.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2005 = decid2005.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2005u = decid2005u.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2010 = decid2010.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2010u = decid2010u.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16()
decid2015 = decid2015.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16().clip(aoi)
decid2015u = decid2015u.rename('band_1').addBands(ee.Image(0).rename('quality')).toInt16().clip(aoi)

decid1992e = decid1992e.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid1992ue = decid1992ue.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2000e = decid2000e.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2000ue = decid2000ue.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2005e = decid2005e.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2005ue = decid2005ue.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2010e = decid2010e.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2010ue = decid2010ue.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2015e = decid2015e.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()
decid2015ue = decid2015ue.rename('band_1').addBands(ee.Image(1).rename('quality')).toInt16()

decid1992 = ee.ImageCollection([ decid1992e, decid1992]).qualityMosaic('quality').select([0],['band_1'])
decid1992u = ee.ImageCollection([ decid1992ue, decid1992u]).qualityMosaic('quality').select([0],['band_1'])
decid2000 = ee.ImageCollection([ decid2000e, decid2000]).qualityMosaic('quality').select([0],['band_1'])
decid2000u = ee.ImageCollection([ decid2000ue, decid2000u]).qualityMosaic('quality').select([0],['band_1'])
decid2005 = ee.ImageCollection([ decid2005e, decid2005]).qualityMosaic('quality').select([0],['band_1'])
decid2005u = ee.ImageCollection([ decid2005ue, decid2005u]).qualityMosaic('quality').select([0],['band_1'])
decid2010 = ee.ImageCollection([ decid2010e, decid2010]).qualityMosaic('quality').select([0],['band_1'])
decid2010u = ee.ImageCollection([ decid2010ue, decid2010u]).qualityMosaic('quality').select([0],['band_1'])
decid2015 = ee.ImageCollection([ decid2015e, decid2015]).qualityMosaic('quality').select([0],['band_1'])
decid2015u = ee.ImageCollection([ decid2015ue, decid2015u]).qualityMosaic('quality').select([0],['band_1'])

tc1992 = tc1992.toInt16()
tc1992u = tc1992u.toInt16()
tc2000 = tc2000.toInt16()
tc2000u = tc2000u.toInt16()
tc2005 = tc2005.toInt16()
tc2005u = tc2005u.toInt16()
tc2010 = tc2010.toInt16()
tc2010u = tc2010u.toInt16()
tc2015 = tc2015.toInt16().clip(aoi)
tc2015u = tc2015u.toInt16().clip(aoi)

/*
Map.addLayer(tc2015.subtract(tc2015u), {min:0, max:1})

print(decid2015)
var outimg = decid2000.addBands(decid2000u).addBands(tc2000).addBands(tc2000u).rename(['decid2000', 'decid2000u', 'tc2000', 'tc2000u']).multiply(land)
print(outimg)
Map.addLayer(outimg, {},'outimg')

Export.image.toDrive({
  image:decid2000.addBands(decid2000u).addBands(tc2000).addBands(tc2000u).rename(['decid2000', 'decid2000u', 'tc2000', 'tc2000u']).multiply(land),
  region:aoi,
  scale:30,
  maxPixels:1e13,
  folder:'decid_tc_layerstack',
  fileNamePrefix:'decid_tc_layerstack_2000',
  description:'decid_tc_layerstack_2000'
})

Export.image.toDrive({
  image:decid1992.addBands(decid1992u).addBands(tc1992).addBands(tc1992u).rename(['decid1992', 'decid1992u', 'tc1992', 'tc1992u']).multiply(land),
  region:aoi,
  scale:30,
  maxPixels:1e13,
  folder:'decid_tc_layerstack',
  fileNamePrefix:'decid_tc_layerstack_1992',
  description:'decid_tc_layerstack_1992'
})

Export.image.toDrive({
  image:decid2005.addBands(decid2005u).addBands(tc2005).addBands(tc2005u).rename(['decid2005', 'decid2005u', 'tc2005', 'tc2005u']).multiply(land),
  region:aoi,
  scale:30,
  maxPixels:1e13,
  folder:'decid_tc_layerstack',
  fileNamePrefix:'decid_tc_layerstack_2005',
  description:'decid_tc_layerstack_2005'
})

Export.image.toDrive({
  image:decid2010.addBands(decid2010u).addBands(tc2010).addBands(tc2010u).rename(['decid2010', 'decid2010u', 'tc2010', 'tc2010u']).multiply(land),
  region:aoi,
  scale:30,
  maxPixels:1e13,
  folder:'decid_tc_layerstack',
  fileNamePrefix:'decid_tc_layerstack_2010',
  description:'decid_tc_layerstack_2010'
})

var dec = ee.Image(tc2015u)//.addBands(decid2015u).addBands(tc2015).addBands(tc2015u).addBands(land).rename(['decid2015', 'decid2015u', 'tc2015', 'tc2015u', 'land'])).multiply(land.toInt16())
Map.addLayer(dec,{},'dec')
print('dec',dec)
Map.addLayer(tc2015)
Export.image.toDrive({
  image:dec,
  region:aoi,
  scale:1000,
  maxPixels:1e13,
  folder:'decid_tc_layerstack',
  fileNamePrefix:'decid_tc_layerstack_2015_t15u',
  description:'decid_tc_layerstack_2015_t15u'
})


var outimg = ee.Image(decid1992
                      .addBands(decid1992u)
                      .addBands(tc1992)
                      .addBands(tc1992u)
                      .select([0,1,2,3],['decid1992', 'decid1992u', 'tc1992', 'tc1992u'])
                      .toInt16()).multiply(land.toInt16()).unmask(-9999).clip(aoi)
*/                     
var outimg = ee.Image(decid1992.addBands(tc1992)
                      .select([0,1],['decid1992', 'tc1992'])
                      .toInt16()).multiply(land.toInt16()).unmask(-9999).clip(aoi)                      

print(outimg)
Map.addLayer(outimg, {},'outimg')
Export.image.toDrive({
  image:outimg,
  region:aoi,
  scale:30,
  maxPixels:1e13,
  folder:'decid_tc_layerstack_1992',
  fileNamePrefix:'decid_tc_layerstack_1992',
  description:'decid_tc_layerstack_1992'
})

