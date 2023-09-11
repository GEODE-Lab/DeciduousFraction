/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var bounds_all = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-166.552734375, 56.218923189166624],
          [-165.146484375, 52.268157373768176],
          [-155.126953125, 54.622978132690335],
          [-150.908203125, 57.98480801923985],
          [-145.810546875, 59.17592824927136],
          [-138.076171875, 58.12431960569374],
          [-131.044921875, 51.508742458803326],
          [-126.123046875, 47.57652571374621],
          [-111.005859375, 48.28319289548349],
          [-96.416015625, 48.2246726495652],
          [-90.703125, 47.45780853075031],
          [-83.14453125, 44.653024159812006],
          [-86.220703125, 40.58058466412762],
          [-82.705078125, 40.44694705960048],
          [-76.025390625, 43.70759350405294],
          [-73.125, 44.08758502824516],
          [-68.37890625, 45.9511496866914],
          [-67.763671875, 42.16340342422401],
          [-59.326171875, 43.834526782236814],
          [-50.537109375, 46.255846818480315],
          [-51.50390625, 51.12421275782688],
          [-51.064453125, 57.61010702068388],
          [-65.654296875, 62.062733258846514],
          [-85.341796875, 66.44310650816469],
          [-95.185546875, 67.57571741708057],
          [-113.466796875, 68.13885164925574],
          [-125.947265625, 70.4073476760681],
          [-140.09765625, 70.31873847853124],
          [-156.708984375, 71.63599288330609],
          [-167.431640625, 69.3493386397765],
          [-165.146484375, 66.72254132270653],
          [-168.662109375, 65.47650756256367],
          [-165.673828125, 63.31268278043484],
          [-168.837890625, 60.326947742998414]]]),
    all_samp_v8 = ee.FeatureCollection("users/masseyr44/shapefiles/all_samp_postbin_v8"),
    all_samp_v8_east = ee.FeatureCollection("users/masseyr44/shapefiles/all_samp_postbin_v8_east");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var samp = all_samp_v8
var bounds = bounds_all
var zone_name = 'all'
var buffer_dist = 14

var L = 0.5
var index = 'NDVI'
var min_pctl = 75
var max_pctl = 95

var vis_band = 'NDVI'

var startJulian1 = 90;
var endJulian1 = 165;
var startJulian2 = 180;
var endJulian2 = 240;
var startJulian3 = 255;
var endJulian3 = 330;

var bands = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2','PIXEL_QA', 'RADSAT_QA','NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])
var band_list = ee.List(['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'NDVI', 'NDWI', 'NBR', 'VARI', 'SAVI'])

//buffer samples
function buffer1(feat) { return ee.Feature(feat).buffer(buffer_dist);}

//define all image collections to use
var ls5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR"); 
var ls7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR");
var ls8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR");

//merge all collections
var all_images=ls5.merge(ls7).merge(ls8)

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
  in_image = in_image.float().divide(10000.0)
  return in_image.addBands(ndvi_calc(in_image))
                 .addBands(ndwi_calc(in_image))
                 .addBands(vari_calc(in_image))
                 .addBands(nbr_calc(in_image))
                 .addBands(savi_calc(in_image))
                 .toInt16()
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

/*
var interval_mean = function(collection, bounds){
  var temp_img = ee.ImageCollection(collection).reduce(ee.Reducer.intervalMean(min_pctl, max_pctl))
  return temp_img.select(ee.List.sequence(0, internal_bands.length().subtract(1)), internal_bands)
}
*/

var elevation = ee.Image('USGS/GMTED2010')
var slope = ee.Terrain.slope(elevation).multiply(10000)
var aspect = ee.Terrain.aspect(elevation)

var topo_image = elevation.addBands(slope).addBands(aspect).select([0, 1, 2],
                                                               ['elevation', 'slope', 'aspect']).int16()
                                                               

function makeLS(bounds, startDate, endDate){
  var allImages1 = getLandsatImages(all_images, bounds, startDate, endDate, startJulian1, endJulian1)
  var allImages2 = getLandsatImages(all_images, bounds, startDate, endDate, startJulian2, endJulian2)
  var allImages3 = getLandsatImages(all_images, bounds, startDate, endDate, startJulian3, endJulian3)

  var imgSeason1 = add_suffix(maxvalcompNDVI(allImages1,bounds).select(bands), '1');
  var imgSeason2 = add_suffix(maxvalcompNDVI(allImages2,bounds).select(bands), '2');
  var imgSeason3 = add_suffix(maxvalcompNDVI(allImages3,bounds).select(bands), '3');
  
  //var imgSeason1= maxvalcompNDVI(allImages1,bounds).select(['NDVI']);
  //var imgSeason2= maxvalcompNDVI(allImages2,bounds).select(['NDVI']);
  //var imgSeason3= maxvalcompNDVI(allImages3,bounds).select(['NDVI']);
  
  return imgSeason1.addBands(imgSeason2).addBands(imgSeason3).addBands(topo_image)
}


//print(samp.first())
//print('Total:',samp.size())

//samp = samp.map(buffer1)

var get_samp = function(year, margins){
  var start_year = ee.Number(year).subtract(margins)
  var end_year = ee.Number(year).add(margins)
  samp = samp.filterMetadata('year', 'not_less_than', start_year)
             .filterMetadata('year','not_greater_than', end_year)
  //print('Samples for ' + year + ' :',samp.size())
  
  var startDate = ee.Date.fromYMD(start_year,1,1);
  var endDate = ee.Date.fromYMD(end_year,12,31);
  
  //************************************************
  
  var output_img = makeLS(bounds,startDate, endDate)
  //print(output_img)
  
  var year_samp = output_img.sample(samp, 30)
  //print(year_samp)
  
  return year_samp
}


var samp1 = get_samp(1992, 5)
var samp2 = get_samp(2000, 2)
var samp3 = get_samp(2005, 2)
var samp4 = get_samp(2010, 2)
var samp5 = get_samp(2015, 2)

var out_samp = samp1.merge(samp2).merge(samp3).merge(samp4).merge(samp5)



Export.table.toDrive({
  collection: out_samp,
  description: 'out_samp_all_v8',
  folder: 'v8_samples',
  fileNamePrefix: 'out_samp_all_v8'
})

