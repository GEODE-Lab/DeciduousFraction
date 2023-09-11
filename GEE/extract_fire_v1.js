/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid_2000 = ee.Image("users/masseyr44/decid/ABoVE_decid_2000_mosaic_V5_L5_85pctl_vis"),
    decid_2005 = ee.Image("users/masseyr44/decid/ABoVE_decid_2005_mosaic_V1_L7_maxval_vis"),
    decid_2010 = ee.Image("users/masseyr44/decid/ABoVE_decid_2010_mosaic_V3_L7_maxval_vis"),
    decid_2015 = ee.Image("users/masseyr44/decid/ABoVE_decid_2015_mosaic_V2_L7_maxval_vis");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
//image collection to stack function
function layer_stack(collection){
  var collection_list=collection.toList({count: collection.size()});
  var first=ee.Image(collection.first());
  var nb = collection.size()
  function combine(img, prev){return ee.Image(prev).addBands(img)}
  return collection_list.slice(1,nb).iterate(combine,first);
}


var ak_fire_bounds = ee.FeatureCollection('ft:12mliiO0B2fxwuByLPkreRqNVK__xXlYjzBBVHHC8')
print(ak_fire_bounds.first())
print(ak_fire_bounds.size())


var decid_stack = layer_stack(ee.ImageCollection([decid_2000, decid_2005, decid_2010, decid_2015]))

var decid_means = ee.Image(decid_stack).reduceRegions(ak_fire_bounds, ee.Reducer.mean(), 30)

print(decid_means.first())

decid_means = decid_means.map(function(feat){return ee.Feature(feat).setGeometry(null)})

print(decid_means.first())

Export.table.toDrive(decid_means,'decid_means', 'work','ak_decid_means_v1' )

