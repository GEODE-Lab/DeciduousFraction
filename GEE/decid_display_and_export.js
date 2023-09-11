/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    output = ee.Image("users/masseyr44/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808_median_output_west_v2"),
    uncert = ee.Image("users/masseyr44/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808_uncert_west_v2"),
    data = ee.Image("users/masseyr44/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808"),
    output2 = ee.Image("users/masseyr44/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808_median_output_west_output4"),
    reduced = ee.Image("users/masseyr44/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808_median_output_west_reduced"),
    reduced_uncert = ee.Image("users/masseyr44/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808_uncert_west_reduced"),
    decid1992_east = ee.Image("users/masseyr44/decid1992_median_output_east_lzw_v5"),
    decid1992_west = ee.Image("users/masseyr44/decid1992_median_output_west_lzw_v5"),
    geometry = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-176.30663755528616, 50.61689951239838],
          [-169.75878599278616, 50.82556043645113],
          [-158.26708677403616, 52.82153644856624],
          [-153.49902036778616, 55.91736702990162],
          [-150.15917661778616, 58.897991486738064],
          [-139.01903989903616, 58.163907494421046],
          [-136.18456724278616, 55.20914002682911],
          [-134.66845396153616, 52.55516294290881],
          [-132.11962583653616, 47.21081741456321],
          [-127.72509458653616, 41.597594731493494],
          [-124.43840497272336, 41.37102049000263],
          [-123.87260907428586, 41.32359653816888],
          [-116.22337811725461, 41.465764749279565],
          [-108.54942792194211, 41.366898039379485],
          [-102.90794842975461, 41.40399069083456],
          [-96.21727460162961, 41.26994526416991],
          [-90.49065106647336, 41.23897253362297],
          [-84.25316327350461, 41.23897253362297],
          [-77.03514569537961, 41.300903308049456],
          [-68.13555547405333, 41.297028347037],
          [-68.02019902874083, 41.38775925906904],
          [-63.933284966240834, 42.53145544430825],
          [-57.209652153740834, 44.03491487800861],
          [-54.660824028740834, 45.501176028070006],
          [-51.057308403740834, 47.408227442796786],
          [-53.078792778740834, 52.38450813892567],
          [-54.528988091240834, 53.83521015193632],
          [-59.231136528740834, 57.57082285172514],
          [-63.757503716240834, 60.42105745932923],
          [-66.21844121624083, 61.52965311533393],
          [-70.87664434124083, 62.11071021516713],
          [-73.29363652874083, 62.60005809328801],
          [-77.42449590374083, 62.74128617837794],
          [-78.21551152874083, 62.62027479264088],
          [-80.19305059124083, 59.65291488696769],
          [-80.98406621624083, 58.775766755355235],
          [-85.20281621624083, 58.7073572247346],
          [-87.53191777874083, 59.586240334917626],
          [-91.48699590374083, 62.498767891827704],
          [-95.13445684124083, 64.79906286486573],
          [-99.08953496624083, 66.16640873196738],
          [-103.44012090374083, 67.49733780007695],
          [-107.35125371624083, 68.30729981507875],
          [-109.10906621624083, 68.74167576235111],
          [-111.74578496624083, 69.19898333351952],
          [-114.47039434124083, 69.57032092878605],
          [-117.41473027874083, 69.87491380656965],
          [-120.62273809124083, 70.14532177529644],
          [-123.30340215374083, 70.35322521473053],
          [-125.72039434124083, 70.52976250454438],
          [-129.32390996624082, 70.777248762719],
          [-131.38933965374082, 70.97878566837679],
          [-136.22332402874082, 71.23491606805898],
          [-138.72820684124082, 71.31955178556281],
          [-143.34246465374082, 71.4038193360784],
          [-145.53973027874082, 71.48772013965171],
          [-149.62664434124082, 71.64059045673494],
          [-153.40594121624082, 71.66825381566173],
          [-158.02019902874082, 71.36173149287065],
          [-159.99773809124082, 71.16410403823458],
          [-163.51336309124082, 70.32365322775318],
          [-165.93035527874082, 69.29241826234916],
          [-168.43523809124082, 67.71498068540176],
          [-168.56707402874082, 66.0774653843356],
          [-168.30340215374082, 65.39122548640397],
          [-169.27019902874082, 64.64895348974386],
          [-172.30242559124082, 63.613703648303456],
          [-175.90594121624082, 60.85202000118463]]]),
    decid1992u = ee.Image("users/masseyr44/decid/decid_mosaic_1992_uncertainty_vis_nd_3"),
    decid2000u = ee.Image("users/masseyr44/decid/decid_mosaic_2000_uncertainty_vis_nd_3"),
    decid2005u = ee.Image("users/masseyr44/decid/decid_mosaic_2005_uncertainty_vis_nd_3"),
    decid2010u = ee.Image("users/masseyr44/decid/decid_mosaic_2010_uncertainty_vis_nd_3"),
    decid2015u = ee.Image("users/masseyr44/decid/decid_mosaic_2015_uncertainty_vis_nd_3"),
    tc1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_prediction_vis_nd"),
    tc1992u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_uncertainty_vis_nd"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    tc2000u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_uncertainty_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2005u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_uncertainty_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    tc2010u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_uncertainty_vis_nd"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd"),
    tc2015u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_uncertainty_vis_nd"),
    tc1992__ = ee.Image("users/masseyr44/tc_1992_median_output_lzw"),
    tc2000__ = ee.Image("users/masseyr44/tc_2000_median_output_lzw"),
    tc2005__ = ee.Image("users/masseyr44/tc_2005_median_output_lzw"),
    tc2010__ = ee.Image("users/masseyr44/tc_2010_median_output_lzw"),
    tc2015__ = ee.Image("users/masseyr44/tc_2015_median_output_lzw"),
    land = ee.Image("users/masseyr44/decid/land_extent_NA");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var bandnames = ee.List(['blue_1','green_1','red_1','nir_1','swir1_1','swir2_1','ndvi_1','ndwi_1','nbr_1','vari_1','savi_1',
                         'blue_2','green_2','red_2','nir_2','swir1_2','swir2_2','ndvi_2','ndwi_2','nbr_2','vari_2','savi_2',
                         'blue_3','green_3','red_3','nir_3','swir1_3','swir2_3','ndvi_3','ndwi_3','nbr_3','vari_3','savi_3',
                         'elevation','slope','aspect'])

data = data.rename(bandnames)

print(data)

var vis1 = {min:0, max:100, palette:['065D18','FFD905']};
var vis2 = {min:0, max:100, palette:['1546B8','E86E0E']};

decid1992 = decid1992.clip(geometry)
decid2000 = decid2000.clip(geometry)
decid2005 = decid2005.clip(geometry)
decid2010 = decid2010.clip(geometry)
decid2015 = decid2015.clip(geometry)

decid1992u = decid1992u.clip(geometry)
decid2000u = decid2000u.clip(geometry)
decid2005u = decid2005u.clip(geometry)
decid2010u = decid2010u.clip(geometry)
decid2015u = decid2015u.clip(geometry)

tc1992 = tc1992.clip(geometry)
tc2000 = tc2000.clip(geometry)
tc2005 = tc2005.clip(geometry)
tc2010 = tc2010.clip(geometry)
tc2015 = tc2015.clip(geometry)

tc1992u = tc1992u.clip(geometry)
tc2000u = tc2000u.clip(geometry)
tc2005u = tc2005u.clip(geometry)
tc2010u = tc2010u.clip(geometry)
tc2015u = tc2015u.clip(geometry)


//Map.addLayer(decid2015, vis1, 'decid2015',false)
//Map.addLayer(decid2015u, vis2, 'decid2015u',false)
//
Map.addLayer(decid2010, vis1, 'decid2010',false)
Map.addLayer(decid2010u, vis2, 'decid2010u',false)
//
//Map.addLayer(decid2005, vis1, 'decid2005',false)
//Map.addLayer(decid2005u, vis2, 'decid2005u',false)
//
//Map.addLayer(decid2000, vis1, 'decid2000',false)
//Map.addLayer(decid2000u, vis2, 'decid2000u',false)

Map.addLayer(decid1992, vis1, 'decid1992',false)
Map.addLayer(decid1992u, vis2, 'decid1992u',false)

/*

Map.addLayer(tc2015, vis1, 'tc2015',false)
Map.addLayer(tc2015u, vis2, 'tc2015u',false)

Map.addLayer(tc2010, vis1, 'tc2010',false)
Map.addLayer(tc2010u, vis2, 'tc2010u',false)

Map.addLayer(tc2005, vis1, 'tc2005',false)
Map.addLayer(tc2005u, vis2, 'tc2005u',false)

Map.addLayer(tc2000, vis1, 'tc2000',false)
Map.addLayer(tc2000u, vis2, 'tc2000u',false)

Map.addLayer(tc1992, vis1, 'tc1992')
Map.addLayer(tc1992u, vis2, 'tc1992u')
*/

Map.addLayer(tc2015.multiply(land), vis2, 'tc2015',false)

Map.addLayer(tc2010.multiply(land), vis2, 'tc2010',false)

Map.addLayer(tc2005.multiply(land), vis2, 'tc2005',false)

Map.addLayer(tc2000.multiply(land), vis2, 'tc2000',false)

Map.addLayer(tc1992.multiply(land), vis2, 'tc1992', false)


Map.addLayer(tc2015__.multiply(land), vis2, 'tc2015__new',false)

Map.addLayer(tc2010__.multiply(land), vis2, 'tc2010__new',false)

Map.addLayer(tc2005__.multiply(land), vis2, 'tc2005__new',false)

Map.addLayer(tc2000__.multiply(land), vis2, 'tc2000__new',false)

Map.addLayer(tc1992__.multiply(land), vis2, 'tc1992__new', false)


var new_decid1992 = ee.ImageCollection([decid1992_east.updateMask(decid1992_east.neq(0)), 
                                    decid1992_west.updateMask(decid1992_west.neq(0))]).mosaic()
var new_decid1992 = new_decid1992.unmask(0)

var mask1992 = decid1992.multiply(0).add(1)




Map.addLayer(new_decid1992.multiply(mask1992), vis1, 'decid1992_new', false)



Export.image.toDrive({
  image:decid1992,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid1992_prediction',
  description:'decid1992_prediction',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2000,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2000_prediction',
  description:'decid2000_prediction',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2005,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2005_prediction',
  description:'decid2005_prediction',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2010,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2010_prediction',
  description:'decid2010_prediction',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2015,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2015_prediction',
  description:'decid2015_prediction',
  folder:'decid_outputs_v4',
  scale:30
})


Export.image.toDrive({
  image:decid1992u,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid1992_uncertainty',
  description:'decid1992_uncertainty',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2000u,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2000_uncertainty',
  description:'decid2000_uncertainty',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2005u,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2005_uncertainty',
  description:'decid2005_uncertainty',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2010u,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2010_uncertainty',
  description:'decid2010_uncertainty',
  folder:'decid_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:decid2015u,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'decid2015_uncertainty',
  description:'decid2015_uncertainty',
  folder:'decid_outputs_v4',
  scale:30
})




Export.image.toDrive({
  image:tc1992,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'tc1992_prediction',
  description:'tc1992_prediction',
  folder:'tc_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:tc2000,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'tc2000_prediction',
  description:'tc2000_prediction',
  folder:'tc_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:tc2005,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'tc2005_prediction',
  description:'tc2005_prediction',
  folder:'tc_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:tc2010,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'tc2010_prediction',
  description:'tc2010_prediction',
  folder:'tc_outputs_v4',
  scale:30
})

Export.image.toDrive({
  image:tc2015,
  region:geometry,
  maxPixels:1e13,
  fileNamePrefix:'tc2015_prediction',
  description:'tc2015_prediction',
  folder:'tc_outputs_v4',
  scale:30
})



/*

Map.addLayer(decid2000, vis1, 'decid2000')

var vis2 = {min:0, max:1, palette:['065D18','FFD905']};
var vis3 = {min:0, max:0.5, palette:['E86E0E','1546B8']};
var vis4 = {min:0, max:9000, palette:['E1741E','E6E50D','29E70F','11D9AC','1E36AA']};
var vis5 = {min:0, max:1000, palette:['E1741E','E6E50D','29E70F','11D9AC','1E36AA']};

Map.addLayer(output, vis2, 'output')

Map.addLayer(output2, vis2, 'output2')

Map.addLayer(reduced, vis2, 'reduced')

Map.addLayer(reduced_uncert, vis2, 'reduced_uncert')

Map.addLayer(uncert, vis3, 'uncert',false)

Map.addLayer(data.select(['red_1']), vis5, 'red_1')
Map.addLayer(data.select(['red_2']), vis5, 'red_2')
Map.addLayer(data.select(['red_3']), vis5, 'red_3')
Map.addLayer(data.select(['nir_1']), vis4, 'nir_1')
Map.addLayer(data.select(['nir_2']), vis4, 'nir_2')
Map.addLayer(data.select(['nir_3']), vis4, 'nir_3')

Map.addLayer(data, {}, 'data',false)

*/
