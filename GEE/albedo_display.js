/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var albedo = ee.ImageCollection("users/masseyr44/bluesky_albedo"),
    bounds = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-169.4893032125242, 70.05473555295136],
          [-168.4346157125242, 66.69258487072796],
          [-171.2471157125242, 64.81672046410877],
          [-174.4111782125242, 59.76250554277479],
          [-174.7627407125242, 53.8078158423812],
          [-164.5674282125242, 51.6800787794595],
          [-130.4658657125242, 40.78972800805037],
          [-107.26274071252419, 37.23998807533373],
          [-66.12992821252419, 32.334527709246835],
          [-49.95805321252419, 37.23998807533373],
          [-40.11430321252419, 48.05682010799279],
          [-40.11430321252419, 63.12012367973885],
          [-69.64555321252419, 76.37547777101534],
          [-53.12211571252419, 82.18006700413171],
          [-69.29399071252419, 83.37106793404855],
          [-134.6846157125242, 79.9271849699663],
          [-170.8955532125242, 74.94642282295271]]]),
    ad2000 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_median_2000"),
    ad2005 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_median_2005"),
    ad2010 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_median_2010"),
    am2000 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_mean_2000"),
    am2005 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_mean_2005"),
    am2010 = ee.Image("users/masseyr44/albedo_products/bluesky_albedo_mean_2010");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
var band = 'season_1'

Map.addLayer(ad2000.select([band]),{min:0, max:1000, palette:"3338FF,33C3FF,33FFB7,33FF4B,94FF33,FCFF33,FF9933,FF4533,FC958B,FFFFFF"},'albedo_median')

Map.addLayer(am2000.select([band]),{min:0, max:1000, palette:"3338FF,33C3FF,33FFB7,33FF4B,94FF33,FCFF33,FF9933,FF4533,FC958B,FFFFFF"},'albedo_mean')

Map.addLayer(am2000.select([band]).subtract(ad2000.select([band])),{min:-500, max:500, palette:"3338FF,33C3FF,33FFB7,33FF4B,94FF33,FCFF33,FF9933,FF4533,FC958B,FFFFFF"},'albedo_diff')

throw('stop')


var start_year = 2008
var end_year = 2012
var year = '2010'

var startJulian1 = 90;
var endJulian1 = 165;
var startJulian2 = 180;
var endJulian2 = 240;
var startJulian3 = 255;
var endJulian3 = 330;
var startJulian4 = 345
var endJulian4 = 75

var startDate = ee.Date.fromYMD(start_year,1,1);
var endDate = ee.Date.fromYMD(end_year,12,31);


var get_albedo_median = function(start_date, end_date, startJulian, endJulian){
  return albedo.filterDate(start_date,end_date)
                  .filter(ee.Filter.calendarRange(startJulian,endJulian))
                  .reduce(ee.Reducer.median())
}

var img1_median = get_albedo_median(startDate, endDate, startJulian1, endJulian1)
var img2_median = get_albedo_median(startDate, endDate, startJulian2, endJulian2)
var img3_median = get_albedo_median(startDate, endDate, startJulian3, endJulian3)
var img4_median = get_albedo_median(startDate, endDate, startJulian4, endJulian4)

var output_img_median = img1_median.addBands(img2_median).addBands(img3_median).addBands(img4_median)
output_img_median = output_img_median.select([0,1,2,3],['season_1', 'season_2', 'season_3', 'season_4'])


print(output_img_median)

Map.addLayer(output_img_median.select(['season_3']),{min:0, max:1000, palette:"3338FF,33C3FF,33FFB7,33FF4B,94FF33,FCFF33,FF9933,FF4533,FC958B,FFFFFF"},'albedo_median')

var out_name = 'bluesky_albedo_median_' +year
print(out_name);

Export.image.toAsset({
  image: output_img_median,
  description: out_name,
  assetId:  'albedo_products/' + out_name,
  region: bounds,
  scale:500,
  maxPixels:1e13,
});




var get_albedo_mean = function(start_date, end_date, startJulian, endJulian){
  return albedo.filterDate(start_date,end_date)
                  .filter(ee.Filter.calendarRange(startJulian,endJulian))
                  .reduce(ee.Reducer.mean())
}

var img1_mean = get_albedo_mean(startDate, endDate, startJulian1, endJulian1)
var img2_mean = get_albedo_mean(startDate, endDate, startJulian2, endJulian2)
var img3_mean = get_albedo_mean(startDate, endDate, startJulian3, endJulian3)
var img4_mean = get_albedo_mean(startDate, endDate, startJulian4, endJulian4)

var output_img_mean = img1_mean.addBands(img2_mean).addBands(img3_mean).addBands(img4_mean)
output_img_mean = output_img_mean.select([0,1,2,3],['season_1', 'season_2', 'season_3', 'season_4'])

print(output_img_mean)

Map.addLayer(output_img_mean.select(['season_3']),{min:0, max:1000, palette:"3338FF,33C3FF,33FFB7,33FF4B,94FF33,FCFF33,FF9933,FF4533,FC958B,FFFFFF"},'albedo_median')

var out_name = 'bluesky_albedo_mean_' +year
print(out_name);

Export.image.toAsset({
  image: output_img_mean,
  description: out_name,
  assetId:  'albedo_products/' + out_name,
  region: bounds,
  scale:500,
  maxPixels:1e13,
});
