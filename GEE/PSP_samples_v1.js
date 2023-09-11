/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var ls5_1 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR"),
    ls7_1 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR"),
    ls8_1 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR"),
    boundary = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-171.2109375, 43.45291889355465],
          [-73.30078125, 25.005972656239187],
          [-46.0546875, 46.92025531537451],
          [-170.68359375, 71.58053179556501]]]),
    ls5_2 = ee.ImageCollection("LANDSAT/LT05/C01/T2_SR"),
    ls7_2 = ee.ImageCollection("LANDSAT/LE07/C01/T2_SR"),
    ls8_2 = ee.ImageCollection("LANDSAT/LC08/C01/T2_SR");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
// constant variables
var BUFFER_DIST = 15
var CRS = 'EPSG:4326'
var SCALE = 30
var KEY = 'Plot_ID'
var PROPERTY_LIST = ee.List(['CLOUD_COVER','CLOUD_COVER_LAND','IMAGE_QUALITY','PIXEL_QA_VERSION','SR_APP_VERSION','GEOMETRIC_RMSE_MODEL', 'LANDSAT_ID','SOLAR_ZENITH_ANGLE'])

var outfile = 'PSP_samples_v1'


// Get squares around each point with side (2 x BUFFER_DIST)
var sites = ee.FeatureCollection('ft:1niHHwDUIBCau9W2SqnoTBVHpPwqti4kPietvJBKb')
            .map(function(feature){ return feature.buffer(BUFFER_DIST).bounds()})


// add to map
Map.addLayer(sites, {color:'ff0000'}, 'sites')


// merge all collections in one
var LS_COLL = ee.ImageCollection(ls5_1.merge(ls7_1.merge(ls8_1.merge(ls5_2.merge(ls7_2.merge(ls8_2)))))) 
              .filterBounds(boundary)
              .select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'pixel_qa', 'radsat_qa'])
              .map(function(image){return image.toFloat()})

print(LS_COLL.first())

// extract properties from collection
function get_coll_dict(collection){
  
  // get size of collection
  var n = ee.ImageCollection(collection).size()
  
  // convert collection to list
  var coll_list = ee.ImageCollection(collection).toList(n)
  
  // extract properties specified in PROPERTY_LIST and id
  // output each image as a dictionary of properties
  return coll_list.map(function(image){
    var dict = ee.Image(image).toDictionary()
    var val_list = PROPERTY_LIST.map(function(property){return dict.get(property)})
                   .add(ee.Image(image).id())
    return ee.Dictionary.fromLists(PROPERTY_LIST.add('id'), val_list)
  })
}


// extract regions from Image Collection and add scene metadata 
function get_regions(feature){
  
  // get images that intersect with the feature
  var coll = LS_COLL.filterBounds(ee.Feature(feature).geometry())
  
  // get dictionary of properties as specified in PROPERTY_LIST and the list of image IDs
  var coll_dicts = get_coll_dict(coll)
  var coll_index_list = coll_dicts.map(function(dict){return ee.Dictionary(dict).get('id')})
  
  // extract pixel values from collection
  var temp_list = coll.getRegion(ee.Feature(feature).geometry(), SCALE)
  var n = temp_list.length()
  
  // get index for the site: here it is Plot_ID
  var feature_index = ee.Feature(feature).get(KEY)
  
  // add name of index to the existing names
  var keys = ee.List(temp_list.get(0)).add(KEY)
  
  // prepare dictionary of extracted site values
  var val_list = temp_list.slice(1, n).map(function(list){ return ee.List(list).add(feature_index)})
  var key_list = ee.List.repeat(keys, n.subtract(1))
  var feat_dict = ee.List.sequence(0, n.subtract(2)).map(function(i){ 
    return  ee.Dictionary.fromLists(key_list.get(i), val_list.get(i))})
  
  // add image properties and output list of dictionaries for the site
  return feat_dict.map(function(dict){ return ee.Feature(null, ee.Dictionary(dict).combine(ee.List(coll_dicts)
                                                  .get(coll_index_list.indexOf(ee.Dictionary(dict).get('id')))))})
}


// convert site feature collection to list
var site_list = sites.toList(ee.FeatureCollection(sites).size());

// get list of features for first site
var first = get_regions(site_list.get(0))

// Iterate over the entire list of sites
var site_data = ee.FeatureCollection(site_list.slice(1, site_list.length().subtract(1))
                                    .iterate(function(feat, prev){ return ee.List(prev).cat(get_regions(feat))}, first))


// Export the FeatureCollection as CSV
Export.table.toDrive({
  collection: site_data,
  fileNamePrefix: outfile,
  description: outfile,
  fileFormat: 'CSV'
});




