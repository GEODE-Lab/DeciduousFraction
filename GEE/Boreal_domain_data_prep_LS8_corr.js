/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var image = ee.Image("users/masseyr44/ak_decid_1995_pred"),
    image2 = ee.Image("users/masseyr44/ak_decid_2000_pred"),
    image3 = ee.Image("users/masseyr44/ak_decid_2005_pred"),
    image4 = ee.Image("users/masseyr44/ak_decid_2010_pred"),
    image5 = ee.Image("users/masseyr44/ak_decid_2015_pred"),
    tc2010 = ee.Image("users/masseyr44/decid/hansen_tc_2010_mosaic_vis"),
    all_samp = ee.FeatureCollection("users/masseyr44/shapefiles/all_samp_postbin_v8"),
    boreal_h = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_simple"),
    boreal_b = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal_10km_buffer"),
    geometry1 = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-112.36364941332755, 63.14621313675587],
          [-112.09997753832755, 59.76944682442285],
          [-110.12243847582755, 59.79156511335204],
          [-101.94861035082755, 59.81366874639297],
          [-91.35779003832755, 59.703003958135476],
          [-82.48083691332755, 61.826903188794816],
          [-79.40466503832755, 63.56009479933871],
          [-79.93200878832755, 64.54069185374328],
          [-80.59118847582755, 66.48854982505604],
          [-79.84411816332755, 68.34394258461576],
          [-81.60193066332755, 69.6202332511093],
          [-84.80993847582755, 69.98436555242635],
          [-85.51306347582755, 69.863686501001],
          [-86.47986035082755, 68.96769464162966],
          [-90.17126660082755, 70.07441937827582],
          [-90.96228222582755, 72.04128234076906],
          [-89.38025097582755, 74.18313882843529],
          [-96.14782910082755, 74.32623874489458],
          [-95.88415722582755, 71.98700425681112],
          [-97.37829785082755, 70.25336217457097],
          [-100.63025097582755, 69.43579633800836],
          [-101.50915722582755, 68.32771948621533],
          [-102.56384472582755, 68.36015412245231],
          [-105.11267285082755, 68.84115897684609],
          [-106.43103222582755, 69.03069127303783],
          [-112.93493847582755, 67.96787243457794],
          [-112.80310253832755, 67.34984402575915],
          [-112.62732128832755, 66.7501347463288],
          [-112.62732128832755, 65.90326424423024],
          [-112.58337597582755, 64.82258561884646]]]),
    geometry2 = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[-112.7385690424095, 68.22510275278712],
          [-115.2873971674095, 69.18257172828805],
          [-117.0452096674095, 69.21378490770593],
          [-125.3948190424095, 70.63129092179263],
          [-133.5686471674095, 70.92067639462985],
          [-141.3030221674095, 70.2784554777498],
          [-141.4788034174095, 59.38427497614411],
          [-130.9319284174095, 59.784734543088256],
          [-118.9788034174095, 59.69615526252068],
          [-111.2444284174095, 59.562845708453985]]]),
    geometry3 = /* color: #0b4a8b */ee.Geometry.Polygon(
        [[[-168.6370065424095, 65.24347622528758],
          [-167.4944284174095, 61.75817281301769],
          [-171.3616159174095, 55.65976182018246],
          [-169.7795846674095, 51.43431036236757],
          [-152.6409127924095, 55.5107401331233],
          [-146.2248971674095, 59.11464514653933],
          [-141.1272409174095, 59.0694992580456],
          [-141.0393502924095, 70.57290934343737],
          [-149.3889596674095, 70.80542498106239],
          [-156.3323190424095, 71.68136289812652],
          [-159.2327096674095, 71.00667744916795],
          [-166.8791940424095, 68.86796758748727]]]),
    geometry4 = /* color: #ffc82d */ee.Geometry.Polygon(
        [[[-134.0081002924095, 51.92478055106039],
          [-125.7463815424095, 43.17412529505897],
          [-110.8049752924095, 43.684745132031324],
          [-111.1565377924095, 60.136710526994236],
          [-125.0432565424095, 60.18044499871564],
          [-142.0061471674095, 59.562845708453985]]]),
    geometry5 = /* color: #00ffff */ee.Geometry.Polygon(
        [[[-111.5081002924095, 44.00169424077857],
          [-94.2815377924095, 41.02237920573002],
          [-79.2522409174095, 40.88962697048983],
          [-80.4827096674095, 55.61015077904123],
          [-89.6233346674095, 57.87469641502499],
          [-91.0295846674095, 59.87307929780022],
          [-101.4006784174095, 59.9611899381141],
          [-111.9475534174095, 59.91716385649657]]]),
    geometry6 = /* color: #bf04c2 */ee.Geometry.Polygon(
        [[[-80.8342721674095, 55.90687590566543],
          [-79.5159127924095, 40.42289372465101],
          [-64.0471627924095, 41.22100678727289],
          [-51.215131542409495, 46.23399188128232],
          [-54.203412792409495, 54.70636594917007],
          [-61.937787792409495, 60.398245902537546],
          [-65.8928659174095, 61.0429890481677],
          [-74.2424752924095, 63.29848633688265],
          [-78.7248971674095, 62.94085069226689],
          [-80.98987303899276, 62.24363205905255],
          [-79.3401315424095, 57.921403894173444]]]);
/***** End of imports. If edited, may not auto-convert in the playground. *****/
/*
Map.addLayer(image, {min:0,max:100,palette:'006400,ffff00'},'1995')
Map.addLayer(image2, {min:0,max:100,palette:'006400,ffff00'},'2000')
Map.addLayer(image3, {min:0,max:100,palette:'006400,ffff00'},'2005')
Map.addLayer(image4, {min:0,max:100,palette:'006400,ffff00'},'2010')
Map.addLayer(image5, {min:0,max:100,palette:'006400,ffff00'},'2015')
*/
//Map.addLayer(boreal_h, {color:'ff0000'})


var start_year = 2013
var end_year = 2018
var year = 2015


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
       /* 
        ee.Image(img.select(['B2','B3','B4','B5','B6','B7', 'pixel_qa', 'radsat_qa'],
                    ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'PIXEL_QA', 'RADSAT_QA'])
            .int16()
            .copyProperties(img)
            .copyProperties(img, ['system:time_start', 'system:time_end', 'system:index', 'system:footprint']))
      */           
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
  
  return imgSeason1.addBands(imgSeason2).addBands(imgSeason3).addBands(topo_image)
}


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
//Map.addLayer(output_img.select([vis_band]),{min:0, max:10000, palette:"2e8b57,fff44f"},'output')

var output_img = ee.Image(makeLS(geometry1)).clip(geometry1)
print(output_img)

var out_name = 'ABoVE_median_SR_NDVI_1_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_LS8_corr',
  fileNamePrefix:  out_name,
  region: geometry1,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});


var output_img = ee.Image(makeLS(geometry2)).clip(geometry2)
print(output_img)

var out_name = 'ABoVE_median_SR_NDVI_2_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_LS8_corr',
  fileNamePrefix:  out_name,
  region: geometry2,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});



var output_img = ee.Image(makeLS(geometry3)).clip(geometry3)
print(output_img)

var out_name = 'ABoVE_median_SR_NDVI_3_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_LS8_corr',
  fileNamePrefix:  out_name,
  region: geometry3,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});



var output_img = ee.Image(makeLS(geometry4)).clip(geometry4)
print(output_img)

var out_name = 'ABoVE_median_SR_NDVI_4_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_LS8_corr',
  fileNamePrefix:  out_name,
  region: geometry4,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});



var output_img = ee.Image(makeLS(geometry5)).clip(geometry5)
print(output_img)

var out_name = 'ABoVE_median_SR_NDVI_5_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_LS8_corr',
  fileNamePrefix:  out_name,
  region: geometry5,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});



var output_img = ee.Image(makeLS(geometry6)).clip(geometry6)
print(output_img)

var out_name = 'ABoVE_median_SR_NDVI_6_' + year                         
print(out_name);

Export.image.toDrive({
  image: output_img,
  description: out_name,
  folder:'ABoVE_data_boreal_LS8_corr',
  fileNamePrefix:  out_name,
  region: geometry6,
  scale:30,
  crs:'EPSG:4326',
  maxPixels:1e13,
});



