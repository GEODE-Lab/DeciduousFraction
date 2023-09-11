/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var land_extent = ee.Image("users/masseyr44/decid/land_extent_NA"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    region1 = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-179.61481791588096, 56.937146201416084],
          [-179.43903666588096, 50.9493869687966],
          [-172.84723979088096, 50.78297498171658],
          [-169.59528666588096, 50.83851165133647],
          [-158.52106791588096, 53.00614925731423],
          [-153.86286479088096, 55.81791186989735],
          [-150.25934916588096, 58.98791856019706],
          [-138.92145854088096, 58.25573787671123],
          [-132.94489604088096, 52.151650609697626],
          [-127.23200541588096, 41.76060837318981],
          [-121.60700541588096, 41.497830269003],
          [-118.09138041588096, 41.497830269003],
          [-115.54255229088096, 41.366039694567455],
          [-110.88434916588096, 41.4319684263165],
          [-107.63239604088096, 41.366039694567455],
          [-103.76520854088096, 41.366039694567455],
          [-98.93122416588096, 41.366039694567455],
          [-93.21833354088096, 41.366039694567455],
          [-88.73591166588096, 41.30004409320506],
          [-83.98981791588096, 41.233981642052996],
          [-78.62848979088096, 41.366039694567455],
          [-67.90583354088096, 41.366039694567455],
          [-56.74372416588096, 44.07727681047281],
          [-51.03083354088096, 47.38863478927866],
          [-52.96442729088096, 52.52754361947182],
          [-58.36631121633798, 56.92234529307904],
          [-64.56598979088096, 61.051340332982754],
          [-73.88239604088096, 62.70788293917659],
          [-77.92536479088096, 62.62717248940481],
          [-80.03473979088096, 59.437779256468055],
          [-83.63825541588096, 58.942605881974316],
          [-86.89020854088096, 59.52704141645111],
          [-89.52692729088096, 60.9234591582422],
          [-95.09436534817581, 64.71417843917348],
          [-103.23786479088096, 67.30043871002778],
          [-127.93513041588096, 70.66613072465374],
          [-129.16559916588096, 70.63701150988258],
          [-140.59138041588096, 71.1831259338569],
          [-150.52302104088096, 71.4924823151993],
          [-155.35700541588096, 71.4924823151993],
          [-158.69684916588096, 71.32435568549903],
          [-162.30036479088096, 70.57864651008072],
          [-166.16755229088096, 69.15745273879102],
          [-168.10114604088096, 67.903221714997],
          [-168.36481791588096, 66.47248040800079],
          [-168.10114604088096, 65.79689393528601],
          [-169.15583354088096, 64.73051638866495],
          [-172.14411479088096, 63.85371304371537],
          [-179.26325541588096, 58.5786460305011]]]),
    decid2000w = ee.Image("users/masseyr44/decid/decid_2000_prediction_vis_nd_2_250m_tc_wtd"),
    decid2005w = ee.Image("users/masseyr44/decid/decid_2005_prediction_vis_nd_2_250m_tc_wtd"),
    decid2010w = ee.Image("users/masseyr44/decid/decid_2010_prediction_vis_nd_2_250m_tc_wtd"),
    albedo2000 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_mean_2000"),
    albedo2005 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_mean_2005"),
    albedo2010 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_mean_2010"),
    table = ee.FeatureCollection("users/masseyr44/shapefiles/hansen_tc_2010_part_1"),
    table2 = ee.FeatureCollection("users/masseyr44/shapefiles/hansen_tc_2010_part_2"),
    table3 = ee.FeatureCollection("users/masseyr44/shapefiles/hansen_tc_2010_part_3"),
    table4 = ee.FeatureCollection("users/masseyr44/shapefiles/hansen_tc_2010_part_4"),
    table5 = ee.FeatureCollection("users/masseyr44/shapefiles/hansen_tc_2010_part_5"),
    boreal = ee.FeatureCollection("users/masseyr44/shapefiles/NAboreal_10kmbuffer"),
    udecid2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_uncertainty_vis_nd"),
    udecid2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_uncertainty_vis_nd"),
    udecid2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_uncertainty_vis_nd"),
    ak_fire = ee.FeatureCollection("users/masseyr44/shapefiles/AK_fire_database"),
    geometry = 
    /* color: #d63000 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[177.56420167528643, 83.53302733608693],
          [177.56420167528643, 34.97948091439697],
          [321.3532641752864, 34.97948091439697],
          [321.3532641752864, 83.53302733608693]]], null, false),
    boreal2 = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_simple"),
    boreal3 = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3"),
    tc1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_prediction_vis_nd"),
    ak_decid1992 = ee.Image("users/masseyr44/ak_decid_1995_pred"),
    ak_decid2000 = ee.Image("users/masseyr44/ak_decid_2000_pred"),
    ak_decid2005 = ee.Image("users/masseyr44/ak_decid_2005_pred"),
    ak_decid2010 = ee.Image("users/masseyr44/ak_decid_2010_pred"),
    ak_decid2015 = ee.Image("users/masseyr44/ak_decid_2015_pred"),
    all_sites = ee.FeatureCollection("users/masseyr44/shapefiles/DiVA_ALL_coordinates"),
    decid2015e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_prediction_east_vis_nd_2"),
    decid2010e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_east_vis_nd_2"),
    decid2005e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_prediction_east_vis_nd_2"),
    decid2000e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_prediction_east_vis_nd_2"),
    decid1992e = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_prediction_east_vis_nd_2"),
    forcing_tc25 = ee.Image("users/masseyr44/albedo_products/forcing_boreal_all_2000_2015_500m_tc25"),
    can_fire = ee.FeatureCollection("users/masseyr44/shapefiles/Can_fire"),
    fire_1978_1998 = ee.FeatureCollection("users/masseyr44/shapefiles/fire_filtered_1978_1998"),
    fire_1998_2018 = ee.FeatureCollection("users/masseyr44/shapefiles/fire_filtered_1998_2018"),
    tc_max = ee.Image("users/masseyr44/decid/tree_cover_all_max"),
    fire_1950_1978 = ee.FeatureCollection("users/masseyr44/shapefiles/fire_filtered_1950_1978"),
    can_fire3 = ee.FeatureCollection("users/masseyr44/shapefiles/NFDB_poly_20190607"),
    ak_fire3 = ee.FeatureCollection("users/masseyr44/shapefiles/AlaskaFireAreaHistory_1940_2018"),
    fire_1998_2018_ = ee.FeatureCollection("users/masseyr44/shapefiles/fire_filtered_1998_2018_"),
    cropland = ee.Image("users/masseyr44/rhseg_v9/final_RHseg_v9"),
    alb_kernel_aug = ee.Image("users/masseyr44/kernels/CAM5_alb_kernel_FSNSC_jul_250m"),
    alb_kernel_jul = ee.Image("users/masseyr44/kernels/CAM5_alb_kernel_FSNSC_aug_250m"),
    alb_kernel_jan = ee.Image("users/masseyr44/kernels/CAM5_alb_kernel_FSNSC_jan_250m"),
    alb_kernel_sep = ee.Image("users/masseyr44/kernels/CAM5_alb_kernel_FSNSC_sep_250m");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var tcmax = ee.ImageCollection([tc2015,tc2000]).map(function(img){return img.int16()}).reduce(ee.Reducer.max())
var tcmin = ee.ImageCollection([tc2015,tc2000]).map(function(img){return img.int16()}).reduce(ee.Reducer.min())

print(tcmin)
print(tcmax)
var tcdiff = tcmax.subtract(tcmin).multiply(land_extent)

var tcdiff_total = tc2015.subtract(tc2000).multiply(land_extent)

//tcdiff = tcdiff.updateMask(tcdiff.gt(10))
//Map.addLayer(boreal3)
Map.addLayer(tcmax, {min:0, max:100,palette:'FF3600,0051FF'},'tcmax',false)
Map.addLayer(tcdiff_total, {min:-40, max:40,palette:'FF3600,FFFFFF,0051FF'},'tcdiff_total',false)

tcmax = ee.ImageCollection([tc2015,tc2000]).map(function(img){return img.int16()}).reduce(ee.Reducer.max())


Map.addLayer(tcmax.updateMask(tcmax.gt(25).multiply(land_extent)), {min:0, max:100, palette:'FF3600,0051FF'},'tc_max',false) //.updateMask(tcmax.gt(25).multiply(land_extent))

Map.addLayer(tcdiff.multiply(land_extent), {min:-100, max:100, palette:'FF0000,00ff00'},'tc_diff',false)

//throw('stop')

Export.image.toAsset({
  image: tcmax,
  description: 'tree_cover_all_max',
  assetId:  'users/masseyr44/decid/tree_cover_all_max',
  region: region1,
  scale: 30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

//ak_decid2000 = ak_decid2000.rename('band_1').addBands(ee.Image(0).rename('quality').byte())
//ak_decid2015 = ak_decid2015.rename('band_1').addBands(ee.Image(0).rename('quality').byte())

decid2015e = decid2015e.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()
decid2010e = decid2010e.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()
decid2000e = decid2000e.rename('band_1').addBands(ee.Image(1).rename('quality')).int16()


print(decid2000e)
Map.addLayer(decid2000.multiply(land_extent),{min:0, max:100, palette:'0F5008,F9DC4D'},'decid2000',false)
Map.addLayer(decid2000e.select(['band_1']).multiply(land_extent),{min:0, max:100, palette:'0F5008,F9DC4D'},'decid2000e',false)
Map.addLayer(decid2015.multiply(land_extent),{min:0, max:100, palette:'0F5008,F9DC4D'},'decid2015',false)

decid2015 = decid2015.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()
decid2010 = decid2010.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()
decid2000 = decid2000.rename('band_1').addBands(ee.Image(0).rename('quality')).int16()


Map.addLayer(decid2015e.select(['band_1']).multiply(land_extent),{min:0, max:100, palette:'0F5008,F9DC4D'},'decid2015e',false)

var initial = ee.ImageCollection([ decid2000e, decid2000]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)

var expr = '(-0.034)*(x**2) + 0.105*x + 0.09'
var expr_tc25 = '(-0.009)*(x**2) + 0.076*x + 0.09'

var ini_alb = initial.expression(expr_tc25, {'x': initial})

var final = ee.ImageCollection([ decid2015e, decid2015]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)
var final0 = ee.ImageCollection([ decid2010e, decid2010]).qualityMosaic('quality').select([0],['band_1']).divide(100.0)

print(final)
Map.addLayer(initial.multiply(land_extent),{min:0, max:1, palette:'0F5008,F9DC4D'},'final_decid',false)
Map.addLayer(final.multiply(land_extent),{min:0, max:1, palette:'0F5008,F9DC4D'},'initial_decid',false)

var fin_alb = final.expression(expr_tc25, {'x': final})
var fin_alb0 = final0.expression(expr_tc25, {'x': final0})

var change_decid = final.subtract(initial).multiply(land_extent).updateMask(tcmax.gt(25)).clip(boreal3)
var change_decid10 = change_decid.updateMask(change_decid.abs().gt(0.1))

var change_decid0 = final0.subtract(initial).multiply(land_extent).updateMask(tcmax.gt(25)).clip(boreal3)
var change_decid10_0 = change_decid0.updateMask(change_decid0.abs().gt(0.1))

Map.addLayer(change_decid, {min:-0.25, max:0.25, palette:'FF3600,FFFFFF,0051FF'},'change_decid',false)

Map.addLayer(change_decid10, {min:-0.25, max:0.25, palette:'FF3600,0051FF'},'change_decid15',false)

//Map.addLayer(change_decid10_0, {min:-0.25, max:0.25, palette:'FF3600,0051FF'},'change_decid10_0',true)

Export.image.toAsset({
  image: change_decid,
  description: 'change_decid_all_2000_2015',
  assetId:  'users/masseyr44/decid/change_decid_all_2000_2015',
  region: region1,
  scale: 30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toDrive({
  image: change_decid,
  description: 'change_decid_all_2000_2015_drive',
  folder:'decid_change',
  fileNamePrefix:  'change_decid_all_2000_2015',
  region: region1,
  scale: 250,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toDrive({
  image: change_decid10,
  description: 'change_decid_10_all_2000_2015_drive',
  folder:'decid_change',
  fileNamePrefix:  'change_decid_10_all_2000_2015',
  region: region1,
  scale: 250,
  crs:'EPSG:4326',
  maxPixels:1e13,
});
Export.image.toDrive({
  image: tcdiff_total.clip(boreal3),
  description: 'tc_change_all_2000_2015_drive3',
  folder:'decid_change',
  fileNamePrefix:  'tc_change_all_2000_2015_drive3',
  region: geometry,
  scale: 250,
  crs:'EPSG:4326',
  maxPixels:1e13,
});


Map.addLayer(alb_kernel_sep, {min:-3 ,max:-1, palette:'FF3600,FF5733,FFE333,42FD33,33FDDB,3339FD'},'alb_kernel_sep',false)
Map.addLayer(alb_kernel_aug, {min:-4 ,max:-2, palette:'FF3600,FF5733,FFE333,42FD33,33FDDB,3339FD'},'alb_kernel_aug',false)
Map.addLayer(alb_kernel_jul, {min:-4 ,max:-2, palette:'FF3600,FF5733,FFE333,42FD33,33FDDB,3339FD'},'alb_kernel_jul',false)

Map.addLayer(alb_kernel_jan, {min:-1.5 ,max:0, palette:'FF3600,FF5733,FFE333,42FD33,33FDDB,3339FD'},'alb_kernel_jan',false)


var forcing_aug = fin_alb.subtract(ini_alb).updateMask(tcmax.gt(25)).multiply(land_extent).multiply(alb_kernel_aug).rename('forcing_aug')
var forcing_sep = fin_alb.subtract(ini_alb).updateMask(tcmax.gt(25)).multiply(land_extent).multiply(alb_kernel_sep).rename('forcing_sep')
var forcing_jul = fin_alb.subtract(ini_alb).updateMask(tcmax.gt(25)).multiply(land_extent).multiply(alb_kernel_jul).rename('forcing_sep')

var forcing_aug0 = fin_alb0.subtract(ini_alb).updateMask(tcmax.gt(25)).multiply(land_extent).multiply(alb_kernel_aug).rename('forcing_aug')

Export.image.toAsset({
  image: forcing_aug,
  description: 'forcing_aug_2000_2015_500m',
  assetId:  'users/masseyr44/decid/forcing_aug_2000_2015_500m_tc25_boreal',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toAsset({
  image: forcing_sep,
  description: 'forcing_sep_2000_2015_500m',
  assetId:  'users/masseyr44/decid/forcing_sep_2000_2015_500m_tc25_boreal',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toDrive({
  image: forcing_sep.clip(boreal3),
  description: 'forcing_boreal_sep_2000_2015_500m_out',
  folder:'decid_forcing',
  fileNamePrefix:  'forcing_boreal_sep_2000_2015_500m',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toDrive({
  image: forcing_aug.clip(boreal3),
  description: 'forcing_boreal_aug_2000_2015_500m_out',
  folder:'decid_forcing',
  fileNamePrefix:  'forcing_boreal_aug_2000_2015_500m',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});


Export.image.toDrive({
  image: forcing_aug0.clip(boreal3),
  description: 'forcing_boreal_aug0_2000_2015_500m_out',
  folder:'decid_forcing',
  fileNamePrefix:  'forcing_boreal_aug0_2000_2015_500m',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toDrive({
  image: forcing_jul.clip(boreal3),
  description: 'forcing_boreal_jul_2000_2015_500m_out',
  folder:'decid_forcing',
  fileNamePrefix:  'forcing_boreal_jul_2000_2015_500m',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

//var forcing10 = fin_alb.subtract(ini_alb).updateMask(tcmax.gt(25)).multiply(land_extent).multiply(albedo_kernel).rename('forcing10').updateMask(change_decid.abs().gt(0.05))

//Map.addLayer(forcing.clip(boreal2), {min:-0.001 ,max:0.001, palette:'0051FF,FF3600'},'forcing_extended',false)
//Map.addLayer(forcing10.clip(boreal2), {min:-0.001 ,max:0.001, palette:'0051FF,FF3600'},'forcing_extended10')

//Map.addLayer(forcing_tc25, {min:-0.001 ,max:0.001, palette:'0051FF,FF3600'},'forcing_tc25')
/*
Export.image.toAsset({
  image: forcing,
  description: 'forcing_all_2000_2015_500m',
  assetId:  'users/masseyr44/decid/forcing_all_2000_2015_500m_tc25_boreal',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toAsset({
  image: forcing.clip(boreal2),
  description: 'forcing_boreal_extended_all_2000_2015_500m',
  assetId:  'users/masseyr44/decid/forcing_boreal_extended_all_2000_2015_500m',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});

Export.image.toDrive({
  image: forcing.clip(boreal2),
  description: 'forcing_boreal_extended_all_2000_2015_500m_out',
  folder:'decid_forcing',
  fileNamePrefix:  'forcing_boreal_extended_all_2000_2015_500m_out',
  region: region1,
  scale: 500,
  crs:'EPSG:4326',
  maxPixels:1e13,
});
*/
print(ak_fire3.first())
print(can_fire3.first())

var can_fire_ = can_fire3.map(function(elem){ return elem.set({'FID': ee.String('CAN_').cat(ee.String(elem.get('FIRE_ID')))})})
var can_fire2 = can_fire_.map(function(elem){
  var feat = ee.Feature(elem.geometry(),{})
  return feat.copyProperties(elem,['YEAR', 'FID', 'SIZE_HA'])
})

var ak_fire_ = ak_fire3.map(function(elem){ return elem.set({'YEAR': ee.Number.parse(elem.get('FIREYEAR')),
                                                            'SIZE_HA': ee.Number(elem.get('ACRES')).multiply(0.40467),
                                                            'FID': ee.String('AK_').cat(ee.String(elem.get('FIREID')))}) })
var ak_fire2 = ak_fire_.map(function(elem){
  var feat = ee.Feature(elem.geometry(),{})
  return feat.copyProperties(elem,['YEAR', 'FID', 'SIZE_HA'])
})

print(ak_fire2.first())
print(can_fire2.first())


var fire_filtered = can_fire2.merge(ak_fire2).filterMetadata('SIZE_HA','greater_than', 500).filterMetadata('YEAR','not_less_than',1998).filterMetadata('YEAR','less_than',2018).filterMetadata('SIZE_HA','greater_than', 500)  // > 500 hectares
                        
print(fire_filtered.size())

print(fire_filtered.first())

Export.table.toAsset({
  collection:fire_filtered,
  description:'fire_filtered_1998_2018',
  assetId:'users/masseyr44/shapefiles/fire_filtered_1998_2018_'
})

print(fire_1950_1978.size())
Map.addLayer(fire_1950_1978,{color:'red'},'fire_1950_1978')

print(fire_1978_1998.size())
Map.addLayer(fire_1978_1998,{color: 'blue'}, 'fire_1978_1998')

print(fire_1998_2018_.size())
Map.addLayer(fire_1998_2018_, {color: 'green'}, 'fire_1998_2018')

/*
var image_stack = ee.Image(forcing_tc25.addBands(change_decid).addBands(tc_max).addBands(tcdiff_total))
                          .multiply(ee.Image.pixelArea()).addBands(ee.Image.pixelArea())
                          .select([0,1,2,3,4],['forc_tc25','decid_ch_00_15','tc_max','tc_diff','area'])
*/
var image_stack2 = ee.Image(forcing_aug.addBands(forcing_sep).addBands(forcing_jul).addBands(forcing_aug0).addBands(change_decid).addBands(tcmax).addBands(tcdiff_total))
                          .multiply(ee.Image.pixelArea()).addBands(ee.Image.pixelArea())
                          .select([0,1,2,3,4,5,6,7],['forc_aug', 'forc_aug0', 'forc_sep','forc_jul','decid_ch_00_15','tc_max','tc_diff','area'])                          


var fire_1998_2018_extract = image_stack2.reduceRegions(fire_1998_2018_, ee.Reducer.sum(), 30).map(function(feat){ return feat.setGeometry(feat.geometry().centroid())})
var fire_1978_1998_extract = image_stack2.reduceRegions(fire_1978_1998, ee.Reducer.sum(), 30).map(function(feat){ return feat.setGeometry(feat.geometry().centroid())})
var fire_1950_1978_extract = image_stack2.reduceRegions(fire_1950_1978, ee.Reducer.sum(), 30).map(function(feat){ return feat.setGeometry(feat.geometry().centroid())})

var all_fire_extract_NA = image_stack2.reduceRegions(fire_filtered, ee.Reducer.sum(), 30).map(function(feat){ return feat.setGeometry(feat.geometry().centroid())}) 

Export.table.toDrive({
  collection: fire_1998_2018_extract,
  description: 'fire_1998_2018_extract_wtc_v3',
  folder: 'forcing_extract_gee',
  fileNamePrefix: 'fire_1998_2018_extract_wtc_v3'
})


Export.table.toDrive({
  collection: fire_1978_1998_extract,
  description: 'fire_1978_1998_extract_wtc_v3',
  folder: 'forcing_extract_gee',
  fileNamePrefix: 'fire_1978_1998_extract_wtc_v3'
})

Export.table.toDrive({
  collection: fire_1950_1978_extract,
  description: 'fire_1950_1978_extract_wtc_v3',
  folder: 'forcing_extract_gee',
  fileNamePrefix: 'fire_1950_1978_extract_wtc_v3'
})

Export.table.toDrive({
  collection: all_fire_extract_NA,
  description: 'all_fire_extract_NA_v2',
  folder: 'forcing_extract_gee',
  fileNamePrefix: 'all_fire_extract_NA_v2',


})