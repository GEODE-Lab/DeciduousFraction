/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var zone1 = 
    /* color: #253bd6 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-151.54717639808922, 66.57062738111507],
          [-151.54717639808922, 63.923454144024895],
          [-145.65850452308922, 63.923454144024895],
          [-145.65850452308922, 66.57062738111507]]], null, false),
    zone5 = 
    /* color: #98ff00 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-66.20537952308922, 54.90893888955114],
          [-66.20537952308922, 51.10433052345691],
          [-60.05303577308922, 51.10433052345691],
          [-60.05303577308922, 54.90893888955114]]], null, false),
    zone2 = 
    /* color: #0b4a8b */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-133.88116077308922, 61.000374179496234],
          [-133.88116077308922, 57.734172295040956],
          [-127.81670764808922, 57.734172295040956],
          [-127.81670764808922, 61.000374179496234]]], null, false),
    zone4 = 
    /* color: #ffc82d */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-91.34209827308922, 52.94279378969202],
          [-91.34209827308922, 48.90168440580128],
          [-85.36553577308922, 48.90168440580128],
          [-85.36553577308922, 52.94279378969202]]], null, false),
    zone3 = 
    /* color: #d63000 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-116.03936389808922, 58.477138765420975],
          [-116.03936389808922, 55.31112376592724],
          [-110.41436389808922, 55.31112376592724],
          [-110.41436389808922, 58.477138765420975]]], null, false),
    image = ee.Image("users/masseyr44/ak_decid_1995_pred"),
    image2 = ee.Image("users/masseyr44/ak_decid_2000_pred"),
    image3 = ee.Image("users/masseyr44/ak_decid_2005_pred"),
    image4 = ee.Image("users/masseyr44/ak_decid_2010_pred"),
    image5 = ee.Image("users/masseyr44/ak_decid_2015_pred"),
    table = ee.FeatureCollection("users/masseyr44/decid/ABoVE_Study_Domain"),
    tc2010 = ee.Image("users/masseyr44/decid/hansen_tc_2010_mosaic_vis"),
    boreal_b = ee.FeatureCollection("users/masseyr44/decid/NABoreal_boreal_10km_buffer"),
    boreal_h = ee.FeatureCollection("users/masseyr44/decid/NAboreal_10kmbuffer"),
    boreal = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-170.170703125, 50.55860413479424],
          [-158.217578125, 52.68617167041279],
          [-153.30939285434152, 55.911669002771404],
          [-150.04375, 58.80503543579855],
          [-139.233203125, 58.068985987821954],
          [-138.090625, 54.61324407475211],
          [-131.7625, 47.267822642617666],
          [-125.34648437499999, 44.01233232748235],
          [-109.26249999999999, 43.50449628805959],
          [-104.60429687499999, 44.82836904206655],
          [-98.36406249999999, 44.95290210881181],
          [-91.06914062499999, 42.08574735811644],
          [-84.56523437499999, 40.900807176085465],
          [-78.14921874999999, 41.75877252719287],
          [-68.56914062499999, 42.1509412002535],
          [-56.70390624999999, 43.7589530883319],
          [-50.72734374999999, 47.38696854291394],
          [-52.92460937499999, 52.79259685897027],
          [-57.84648437499999, 56.64698491697063],
          [-64.87773437499999, 61.5146781712937],
          [-78.32093919613442, 62.78853877630148],
          [-80.52226562499999, 59.74792657078106],
          [-84.9374198886535, 59.27782159718193],
          [-88.37276592344836, 60.37639431989281],
          [-94.32109374999999, 64.65432185309979],
          [-110.84453124999999, 69.12528180058297],
          [-127.28007812499999, 70.48995985899165],
          [-143.803515625, 70.81028714470123],
          [-158.1296875, 69.8943395440455],
          [-167.358203125, 68.74622173946399],
          [-168.588671875, 67.76966607015038],
          [-168.14921875, 66.18922286480425],
          [-168.061328125, 64.84179146448706],
          [-167.44609375, 63.34458838903397],
          [-167.006640625, 61.64017806521875]]]);
/***** End of imports. If edited, may not auto-convert in the playground. *****/
/*
Map.addLayer(image, {min:0,max:100,palette:'006400,ffff00'},'1995')
Map.addLayer(image2, {min:0,max:100,palette:'006400,ffff00'},'2000')
Map.addLayer(image3, {min:0,max:100,palette:'006400,ffff00'},'2005')
Map.addLayer(image4, {min:0,max:100,palette:'006400,ffff00'},'2010')
Map.addLayer(image5, {min:0,max:100,palette:'006400,ffff00'},'2015')
*/
//Map.addLayer(boreal_h, {color:'ff0000'})


var start_year = 2008
var end_year = 2012
var year = 2010
var bounds = zone5
var zone_name = 'zone5'

var L = 0.5
var index = 'NDVI'
var min_pctl = 50
var max_pctl = 95

var vis_band = 'nir_1'

var startJulian1 = 90;
var endJulian1 = 165;
var startJulian2 = 180;
var endJulian2 = 240;
var startJulian3 = 255;
var endJulian3 = 330;

var internal_bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2','PIXEL_QA', 'RADSAT_QA','NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])
var bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

//************************************************

var startDate = ee.Date.fromYMD(start_year,1,1);
var endDate = ee.Date.fromYMD(end_year,12,31);

//define all image collections to use
var ls5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR"); 
var ls7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR");
var ls8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR");

//merge all collections
var all_images=ls5.merge(ls7).merge(ls8)
print(all_images.first())

//************************************************

//normalized difference vegetation index
var ndvi_calc=function(img){
  return img.normalizedDifference(['NIR', 'RED'])
            .select([0],['NDVI'])
            .multiply(10000)
            .toInt16()
}

// Visible Atmospherically Resistant Index 
var vari_calc=function(img){
  return (img.select(['RED']).subtract(img.select(['GREEN'])))
          .divide(img.select(['RED']).add(img.select(['GREEN'])).subtract(img.select(['BLUE'])))
            .select([0],['VARI'])
            .multiply(10000)
            .toInt16()
}

//normalized difference water index
var ndwi_calc=function(img){
  return img.normalizedDifference(['NIR', 'SWIR2'])
            .select([0],['NDWI'])
            .multiply(10000)
            .toInt16()
}

//normalized burn ratio
var nbr_calc=function(img){
  return img.normalizedDifference(['NIR', 'SWIR1'])
            .select([0],['NBR'])
            .multiply(10000)
            .toInt16()
}

//soil adjusted vegetation index
var savi_calc=function(img){
  return (img.select(['NIR']).subtract(img.select(['RED'])).multiply(1+L))
      .divide(img.select(['NIR']).add(img.select(['RED'])).add(L))
            .select([0],['SAVI'])
            .multiply(10000)
            .toInt16()
}

//function to add indices to an image
//NDVI, NDWI, VARI, NBR, SAVI
var addIndices=function(in_image){
  var temp_image = in_image.float().divide(10000.0)
  return in_image.addBands(ndvi_calc(in_image))
                 .addBands(ndwi_calc(in_image))
                 .addBands(vari_calc(in_image))
                 .addBands(nbr_calc(in_image))
                 .addBands(savi_calc(in_image))

}


// add suffix to all band names
var add_suffix = function(in_image, suffix_str){
  var bandnames = in_image.bandNames().map(function(elem){return ee.String(elem).toLowerCase().cat('_').cat(suffix_str)})
  var nb = bandnames.length()
  return in_image.select(ee.List.sequence(0, ee.Number(nb).subtract(1)), bandnames)
}

//method to correct Landsat 8 based on Landsat 7 reflectance. 
//This method scales the SR reflectance values to match LS7 reflectance
//The returned values are generally lower than input image
var LS8_SR_corr = function(img){
  return img.select(['B2'],['BLUE']).float().multiply(0.8850).add(183).int16()
            .addBands(img.select(['B3'],['GREEN']).float().multiply(0.9317).add(123).int16())
            .addBands(img.select(['B4'],['RED']).float().multiply(0.9372).add(123).int16())
            .addBands(img.select(['B5'],['NIR']).float().multiply(0.8339).add(448).int16())
            .addBands(img.select(['B6'],['SWIR1']).float().multiply(0.8639).add(306).int16())
            .addBands(img.select(['B7'],['SWIR2']).float().multiply(0.9165).add(116).int16())
            .addBands(img.select(['pixel_qa'],['PIXEL_QA']).int16())
            .addBands(img.select(['radsat_qa'],['RADSAT_QA']).int16())
            .copyProperties(img)
            .copyProperties(img, ['system:time_start','system:time_end', 'system:index', 'system:footprint'])
}


//this method renames LS5 and LS7 bands and corrects LS8 bands using LS8_corr()
//this method should be used with SR only
var LS_SR_band_correction = function(img){
    return ee.Algorithms.If( 
      
      ee.String(img.get('SATELLITE')).compareTo('LANDSAT_8'),
      
        ee.Image(img.select(['B1','B2','B3','B4','B5','B7', 'pixel_qa', 'radsat_qa'],
                            ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA', 'RADSAT_QA'])
                    .int16()
                    .copyProperties(img)
                    .copyProperties(img, ['system:time_start', 'system:time_end', 'system:index', 'system:footprint'])), 
      
        ee.Image(LS8_SR_corr(img))
                    
      )}

//method to calcluate clear mask based on pixel_qa and radsat_qa bands
var LS_SR_only_clear = function(image) {
    var clearBit = 1;
    var clearMask = Math.pow(2, clearBit);
    var qa = image.select('PIXEL_QA');
    var qa_mask = qa.bitwiseAnd(clearMask);
    
    var ra = image.select('RADSAT_QA')
    var ra_mask = ra.eq(0)
    
    return ee.Image(image.updateMask(qa_mask).updateMask(ra_mask));
};



//make collections based on given parameters
function getLandsatImages(collection, bounds, startDate,endDate,startJulian,endJulian){  
  return ee.ImageCollection(collection)
          .filterDate(startDate,endDate)
          .filter(ee.Filter.calendarRange(startJulian,endJulian))
          .filterBounds(bounds)
          .map(LS_SR_band_correction)
          .map(LS_SR_only_clear)
          .map(addIndices)
          //.map(function(img){return img.addBands(img.normalizedDifference(['B4','B3']).select([0],['NDVI']))})
}

//function to make pctl th value composite
var maxvalcompNDVI = function(collection,bounds) {
  var index_band = collection.select(index)
  .reduce(ee.Reducer.percentile([min_pctl]))
  var withDist = collection.map(function(image) {
    return image.addBands(image.select(index).subtract(index_band)
    .abs().multiply(-1).rename('quality'))
  })
  return withDist.qualityMosaic('quality')
}

var interval_mean = function(collection, bounds){
  var temp_img = ee.ImageCollection(collection).reduce(ee.Reducer.intervalMean(min_pctl, max_pctl))
  return temp_img.select(ee.List.sequence(0, internal_bands.length().subtract(1)), internal_bands)
}

var elevation = ee.Image('USGS/GMTED2010')
var slope = ee.Terrain.slope(elevation).multiply(10000)
var aspect = ee.Terrain.aspect(elevation)

var topo_image = elevation.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                               ['elevation', 'slope', 'aspect']).int16()
                                                               

function makeLS(bounds){
  var allImages1 = getLandsatImages(all_images, bounds, startDate,endDate,startJulian1,endJulian1)
  var allImages2 = getLandsatImages(all_images, bounds, startDate,endDate,startJulian2,endJulian2)
  var allImages3 = getLandsatImages(all_images, bounds, startDate,endDate,startJulian3,endJulian3)

  var imgSeason1 = ee.Image(add_suffix(maxvalcompNDVI(allImages1,bounds).select(bands), '1')).unmask(-9999);
  var imgSeason2 = ee.Image(add_suffix(maxvalcompNDVI(allImages2,bounds).select(bands), '2')).unmask(-9999);
  var imgSeason3 = ee.Image(add_suffix(maxvalcompNDVI(allImages3,bounds).select(bands), '3')).unmask(-9999);
  
  //var imgSeason1= maxvalcompNDVI(allImages1,bounds).select(['NDVI']);
  //var imgSeason2= maxvalcompNDVI(allImages2,bounds).select(['NDVI']);
  //var imgSeason3= maxvalcompNDVI(allImages3,bounds).select(['NDVI']);
  
  return imgSeason1.addBands(imgSeason2).addBands(imgSeason3)
}


var output_img = ee.Image(makeLS(bounds)).addBands(tc2010.int16()).clip(bounds)
print(output_img)

//var tree_thresh = 20

//Map.addLayer(table, {color:'ff0000'})

//var tc = tc2010.updateMask(tc2010.gt(tree_thresh)).multiply(0).add(1)
//var data_disp = output_img.select([vis_band]).multiply(0).add(1)
//var data_diff = tc.unmask().subtract(data_disp.unmask())
//Map.addLayer(tc, {palette:'ff0000'})
//Map.addLayer(data_disp,{},'output')


// green - where data is available but landcover is non tree cover
// red - where land cover is tree over and data is not available
//Map.addLayer(data_diff.updateMask(data_diff.neq(0)),{palette:'00ff00,ff0000'},'data_diff')

//Map.addLayer(output_img,{},'output')
Map.addLayer(output_img.select([vis_band]),{min:0, max:10000, palette:"2e8b57,fff44f"},'output')

var out_name = 'ABoVE_median_SR_NDVI_check_' + zone_name + '_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_check',
  fileNamePrefix:  out_name,
  region: bounds,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});
/*
Export.image.toCloudStorage({
  image: output_img,
  description: out_name,
  bucket:'masseyr44_store1',
  fileNamePrefix:  'gee_output/' + out_name,
  region: bounds,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});


*/
