/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var land = ee.Image("users/masseyr44/decid/land_extent_NA"),
    tiles = ee.FeatureCollection("users/masseyr44/shapefiles/decid_tc_layerstack_tiles"),
    ak_fire = ee.FeatureCollection("users/masseyr44/shapefiles/ak_fire_multi"),
    boreal_bounds = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal"),
    ak_fire_all = ee.FeatureCollection("users/masseyr44/shapefiles/AK_fire_database"),
    ak_fire_new = ee.FeatureCollection("users/masseyr44/shapefiles/AlaskaFireAreaHistory_1940_2018"),
    can_fire = ee.FeatureCollection("users/masseyr44/shapefiles/Can_fire"),
    tc2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_prediction_vis_nd"),
    tc2000 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_prediction_vis_nd"),
    cam5_apr = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_apr_250m"),
    cam5_aug = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_aug_250m"),
    cam5_jul = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_jul_250m"),
    cam5_jun = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_jun_250m"),
    cam5_may = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_may_250m"),
    cam5_nov = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_nov_250m"),
    cam5_oct = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_oct_250m"),
    cam5_sep = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_sep_250m"),
    image = ee.Image("users/masseyr44/decid/FireAreaHistory_1940_2018_v2_30m"),
    image2 = ee.Image("users/masseyr44/decid/NFDB_poly_20171106_gt500ha_geo_v2_30m"),
    geometry = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-178.87095379237064, 72.45163111786071],
          [179.01967120762936, 49.95727882073875],
          [-156.37095379237064, 43.45975470768747],
          [-114.88657879237064, 41.25185262811164],
          [-72.5229153112474, 26.713481333704397],
          [-39.30064129237064, 39.103271032573964],
          [-49.14439129237064, 64.40100690048561],
          [-64.78892254237064, 70.32190977142183]]]),
    top_fire_layer = ee.Image("users/masseyr44/decid/NA_fire_top_layer_30m_lzw"),
    tc1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_prediction_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    NABoreal_boreal_10km_buffer = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal_10km_buffer"),
    boreal = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal_geo_merged"),
    aci = ee.ImageCollection("AAFC/ACI"),
    ecozones = ee.FeatureCollection("users/masseyr44/shapefiles/boreal_ecozones"),
    may_kernel = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_may_250m"),
    boreal_geom = 
    /* color: #d63000 */
    /* shown: false */
    /* locked: true */
    ee.Geometry.Polygon(
        [[[-155.54616073676453, 57.105632445071265],
          [-152.51393417426453, 60.429406422970054],
          [-150.66823104926453, 59.528012748925256],
          [-148.03151229926453, 61.39076529708879],
          [-146.62526229926453, 61.39076529708879],
          [-146.44948104926453, 60.92438997317348],
          [-143.98854354926453, 60.55926714736291],
          [-141.08815292426453, 60.537659800808484],
          [-140.86842636176453, 61.285375638302504],
          [-139.63795761176453, 60.98839302154567],
          [-138.75905136176453, 59.23705516746174],
          [-135.90260604926453, 58.37215839513638],
          [-135.15553573676453, 59.483412443301816],
          [-131.06862167426453, 56.21200861651861],
          [-128.43190292426453, 56.62522385524633],
          [-124.38893417426452, 54.05208875060158],
          [-123.07057479926452, 55.046079169366045],
          [-116.87428573676452, 51.14398566769408],
          [-114.58912948676452, 51.14398566769408],
          [-113.71022323676452, 51.85524427946458],
          [-112.12819198676452, 53.63726600196818],
          [-108.56862167426452, 53.112942139350366],
          [-104.52565292426452, 52.233641265513775],
          [-101.09791854926452, 50.75639359974265],
          [-99.07643417426452, 49.80160643042131],
          [-98.50514511176452, 50.44958680974694],
          [-96.87916854926452, 49.029715592587],
          [-94.81373886176452, 49.28836171516787],
          [-94.06666854926452, 49.57416327295657],
          [-90.930161254366, 48.47437220446809],
          [-86.33229354926452, 47.419674336336264],
          [-81.93776229926452, 46.459567828998836],
          [-79.30104354926452, 47.36017191583677],
          [-75.08229354926452, 46.82162560630439],
          [-71.12721542426452, 46.64089956988809],
          [-68.31471542426452, 48.27491757060441],
          [-67.17213729926452, 47.952174919594455],
          [-63.74440292426453, 48.128467660762915],
          [-63.48073104926453, 48.856534068414696],
          [-61.81080917426453, 48.856534068414696],
          [-60.27272323676453, 48.653729059241456],
          [-59.39381698676453, 46.64089956988809],
          [-53.94459823676453, 46.30799520346268],
          [-51.79127792426453, 46.21684961197018],
          [-52.09889511176453, 48.33338032125625],
          [-53.81276229926453, 50.64505891225922],
          [-55.39479354926453, 54.41169415375931],
          [-59.43776229926453, 56.47989557178355],
          [-61.59108261176453, 58.670472739384515],
          [-72.79713729926452, 58.943594002165895],
          [-76.66432479926452, 58.41821812264657],
          [-77.80690292426452, 55.69534761705261],
          [-79.91627792426452, 55.19685668519536],
          [-82.86061386176452, 55.571314977501025],
          [-86.24440292426452, 56.50415571409894],
          [-89.67213729926452, 57.53274224703207],
          [-94.55006698676452, 60.18997474421175],
          [-94.85768417426452, 62.72890383762949],
          [-98.02174667426452, 62.48628394329625],
          [-100.39479354926452, 63.22802686350919],
          [-100.92213729926452, 63.87391496126039],
          [-99.86744979926452, 64.65619526336555],
          [-102.50416854926452, 64.8062645677211],
          [-105.00905136176452, 64.22008509517586],
          [-105.84401229926452, 63.128883459034654],
          [-110.98561386176452, 64.52420019332571],
          [-112.04030136176452, 65.08540777696625],
          [-112.39186386176452, 66.5083042691309],
          [-115.39538679323685, 67.62471286484337],
          [-116.49401960573685, 67.82460538536094],
          [-119.04284773073685, 67.65814660642091],
          [-121.10827741823685, 67.74152369405466],
          [-122.69030866823685, 68.26817922842571],
          [-122.86608991823685, 68.97299336601763],
          [-125.19519148073685, 69.30164134596089],
          [-127.26062116823685, 69.79300916872155],
          [-129.76550398073687, 69.70173664435487],
          [-132.09460554323687, 69.64066905343647],
          [-132.53405866823687, 69.17702506630384],
          [-134.55554304323687, 69.27055427866036],
          [-135.82995710573687, 69.17702506630384],
          [-136.79675398073687, 68.68733522141225],
          [-136.88464460573687, 68.31694102411524],
          [-138.68640241823687, 68.75113294785633],
          [-138.37878523073687, 69.34818838221733],
          [-140.00476179323687, 69.54873771493372],
          [-142.81726179323687, 69.20824619371864],
          [-146.55261335573687, 68.90983127301062],
          [-148.44226179323687, 68.30069867359498],
          [-150.68347273073687, 68.23561341144107],
          [-152.96862898073687, 68.08849189286131],
          [-155.63314632497614, 67.7959929876957],
          [-157.63265804372614, 67.6961374011629],
          [-159.34652523122614, 67.74611835708892],
          [-159.41244319997614, 67.9697196033285],
          [-160.26937679372614, 68.35386631951286],
          [-162.02718929372614, 68.3619699963949],
          [-163.01595882497614, 68.24011109499597],
          [-163.63119319997614, 67.82918376488985],
          [-163.52132991872614, 67.24149302252874],
          [-161.58773616872614, 66.84729503973915],
          [-160.48910335622614, 66.56927370092244],
          [-161.03841976247614, 66.19071988152145],
          [-161.03841976247614, 65.61661374289723],
          [-161.36800960622614, 65.49842009815443],
          [-162.68636898122614, 65.71620543489942],
          [-163.56527523122614, 65.5439426847384],
          [-164.20248226247614, 64.9366103828441],
          [-163.89486507497614, 64.38177622699668],
          [-162.02718929372614, 64.41026256902111],
          [-161.23617366872614, 64.45767416611785],
          [-161.54379085622614, 63.64044203421132],
          [-162.99398616872614, 63.07888183590593],
          [-164.29037288747614, 62.2618247058201],
          [-163.76302913747614, 61.31670902561745],
          [-162.64242366872614, 60.95608315404705],
          [-161.71957210622614, 60.22239602234156],
          [-159.65414241872614, 60.752758300813404],
          [-159.47836116872614, 59.661122748597805],
          [-160.79672054372614, 58.965912605993715],
          [-159.19271663747614, 58.1521991256935],
          [-159.03890804372614, 57.30758074184499],
          [-163.19174007497614, 55.9049285217731],
          [-167.01498226247614, 54.58993637873281],
          [-168.64095882497614, 53.51945831749226],
          [-169.65170101247614, 52.501559192764034],
          [-166.81722835622614, 52.715048735461835],
          [-164.90560726247614, 53.675934493020044],
          [-160.66488460622614, 54.11614218194133],
          [-159.67611507497614, 54.98270362826218],
          [-157.78646663747614, 55.81861250896579]]]),
    boreal_mask = ee.Image("users/masseyr44/decid/borealMask"),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    cam5_mar = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_mar_250m"),
    alb_sum2000 = ee.Image("users/masseyr44/albedo_products/albedo_composite_mean_2000_2002_150_240"),
    alb_fal2000 = ee.Image("users/masseyr44/albedo_products/albedo_composite_mean_2000_2002_240_300"),
    alb_spr2000 = ee.Image("users/masseyr44/albedo_products/albedo_composite_mean_2000_2002_60_150"),
    alb_sum2015 = ee.Image("users/masseyr44/albedo_products/albedo_composite_mean_2013_2018_150_240"),
    alb_fal2015 = ee.Image("users/masseyr44/albedo_products/albedo_composite_mean_2013_2018_240_300"),
    alb_spr2015 = ee.Image("users/masseyr44/albedo_products/albedo_composite_mean_2013_2018_60_150"),
    decid2000_east_new = ee.Image("users/masseyr44/decid/decid2000_median_output_east_lzw_v4"),
    decid2000_west_new = ee.Image("users/masseyr44/decid/decid2000_median_output_west_lzw_v4"),
    decid2015_east_new = ee.Image("users/masseyr44/decid/decid2015_median_output_east_lzw_v4"),
    decid2015_west_new = ee.Image("users/masseyr44/decid/decid2015_median_output_west_lzw_v4");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
Map.setOptions('SATELLITE');

var decid2015_new = ee.ImageCollection([decid2015_west_new, decid2015_east_new]).mosaic()
var decid2000_new = ee.ImageCollection([decid2000_west_new, decid2000_east_new]).mosaic()

var lim = 0.1;
var calc_scale = 500;
print(lim);

var uncert_calc = function(img_old, img_new, uncert_old, uncert_new){
  return ee.Image(0.01)
           .multiply((ee.Image(img_old).toFloat()).multiply(ee.Image(uncert_new).toFloat())
                        .add((ee.Image(img_new)).toFloat().multiply(ee.Image(uncert_old).toFloat())))
           .divide((ee.Image(img_old).toFloat()).multiply(ee.Image(img_old).toFloat())).abs()
}

var change_calc = function(img_old, img_new){
  return ((ee.Image(img_new).toFloat()).subtract(ee.Image(img_old).toFloat())).divide(ee.Image(img_old).toFloat())
}

var vis_decid = {min:0, max:100, palette:'286F09,ECC519'};
var vis_decid_diff = {min:-0.25, max:0.25, palette:'D13730,FCDC64,1965C7'};
var vis_tc = {min:0, max:100, palette:'B62809,FFC560,1178C8'};
var vis_tc_diff = {min:-0.25, max:0.25, palette:'B62809,FFC560,1178C8'};
 
//Map.addLayer(boreal_geom);


var tc_max = ee.ImageCollection([tc2000,tc2010,tc2005,tc2015]).reduce(ee.Reducer.max()); 
var tc_min = ee.ImageCollection([tc2000,tc2010,tc2005,tc2015]).reduce(ee.Reducer.min()); 

var tc_mask = boreal_mask.updateMask(tc_max.gt(25));

var tc_mask_max = boreal_mask.updateMask(tc_max);
var tc_mask_min = boreal_mask.updateMask(tc_min);

var top_fire_layer = top_fire_layer.updateMask(top_fire_layer.gt(0)).rename('top_fire_layer').toFloat();
//Map.addLayer(top_fire_layer,{min:1900, max: 2018, palette:'A8FB9E,F4DD36,0B3D05'},'top_fire_layer', false);


var area_img = ee.Image.pixelArea().multiply(tc_mask_max);

var fire_mask = top_fire_layer.multiply(0).add(1);
Map.addLayer(fire_mask,{palette:'A8FB9E'},'fire_mask', false);

//var decid_min = ee.ImageCollection([decid2000, decid2015]).reduce(ee.Reducer.min()); //decid2010,decid2005,
//var decid_mask = ee.Image(1).updateMask(decid_min.neq(0));

//var tc_mask0 = tc_mask
//var tc_mask = tc_mask.multiply(decid_mask)

decid1992 = decid1992.toFloat()
decid2000 = decid2000.toFloat()
decid2005 = decid2005.toFloat()
decid2010 = decid2010.toFloat()
decid2015 = decid2015.toFloat()

tc1992 = tc1992.toFloat()
tc2000 = tc2000.toFloat()
tc2005 = tc2005.toFloat()
tc2010 = tc2010.toFloat()
tc2015 = tc2015.toFloat()

var tc_diff = tc2015.subtract(tc2000).updateMask(tc_mask).multiply(land).multiply(0.01);
//var tc_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5)',{'a': tc2000u.toFloat(), 'b': tc2015u.toFloat()}).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);
Map.addLayer(tc_diff,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'tc_diff',false);

var decid_diff = ee.Image(decid2015).subtract(ee.Image(decid2000)).updateMask(tc_mask).multiply(land).toFloat().multiply(0.01);
var decid_diff_new = ee.Image(decid2015_new).subtract(ee.Image(decid2000_new)).updateMask(tc_mask).multiply(land).toFloat().multiply(0.01);
var decid_diff_tc = ee.Image(decid2015.multiply(tc2015)).subtract(ee.Image(decid2000.multiply(tc2000))).updateMask(tc_mask).multiply(land).toFloat().multiply(0.0001);
var decid_diff_tc_new = ee.Image(decid2015_new.multiply(tc2015)).subtract(ee.Image(decid2000_new.multiply(tc2000))).updateMask(tc_mask).multiply(land).toFloat().multiply(0.0001);
//var evergrn_diff_tc = tc_diff.subtract(decid_diff_tc)

//var decid_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5)',{'a': decid2000u.toFloat(), 'b': decid2015u.toFloat()}).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);
Map.addLayer(decid_diff,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'decid_diff',false);
Map.addLayer(decid_diff_new,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'decid_diff_new',false);
Map.addLayer(decid_diff_tc,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'decid_diff_tc',false);
Map.addLayer(decid_diff_tc_new,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'decid_diff_tc_new',false);
//throw('stop')

//Map.addLayer(decid_diff,vis_decid_diff,'decid_diff');
//Map.addLayer(decid_diff_tc,vis_decid_diff,'decid_diff_tc');
//Map.addLayer(evergrn_diff_tc,vis_decid_diff,'evergrn_diff_tc');

//Map.addLayer(decid_diff0,vis_decid_diff,'decid_diff0');

Map.addLayer(tc1992.multiply(land),vis_tc,'tc_1992', false);

Map.addLayer(decid1992.multiply(tc1992.divide(100.0)).multiply(land),vis_tc,'decid_tc_1992', false);
Map.addLayer(decid2000.multiply(tc2000.divide(100.0)).multiply(land),vis_decid,'decid_tc_2000', false);
Map.addLayer(decid2005.multiply(tc2005.divide(100.0)).multiply(land),vis_decid,'decid_tc_2005', false);
Map.addLayer(decid2010.multiply(tc2010.divide(100.0)).multiply(land),vis_decid,'decid_tc_2010', false);
Map.addLayer(decid2015.multiply(tc2015.divide(100.0)).multiply(land),vis_decid,'decid_tc_2015', false);


Map.addLayer(decid2000.multiply(land),vis_decid,'decid2000', false);
//Map.addLayer(decid2005.multiply(land),vis_decid,'decid2005', false);
//Map.addLayer(decid2010.multiply(land),vis_decid,'decid2010', false);
Map.addLayer(decid2015.multiply(land),vis_decid,'decid2015', false);

Map.addLayer(tc2000,vis_tc,'tc2000', false);
//Map.addLayer(tc2005,vis_tc,'tc2005', false);
//Map.addLayer(tc2010,vis_tc,'tc2010', false);
Map.addLayer(tc2015,vis_tc,'tc2015', false);


/*
Export.image.toDrive({
  image:decid_diff,
  fileNamePrefix:'new_decid_diff_2000_2015',
  description:'new_decid_diff_2000_2015',
  scale:calc_scale,
  maxPixels:1e13,
  region:geometry
  
});
*/

//Map.addLayer(tiles,{}, 'tiles', false);

//throw('stop');



var recent_fire_mask = fire_mask.updateMask(top_fire_layer.gt(2000));
var interm_fire_mask = fire_mask.updateMask(top_fire_layer.gt(1980).and(top_fire_layer.lte(2000)));
var old_fire_mask = fire_mask.updateMask(top_fire_layer.lte(1980).and(top_fire_layer.gte(1950)));

//Map.addLayer(recent_fire_mask,{palette:'ff3300'},'recent', false);
//Map.addLayer(interm_fire_mask,{palette:'0033ff'},'interm', false);
//Map.addLayer(old_fire_mask,{palette:'ff33ff'},'old', false);


var boreal_area_tc = ee.Image.pixelArea().multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                    geometry:boreal_bounds.geometry(),
                                                    scale:calc_scale,
                                                    maxPixels:1e13}).get('area')                                              
                                              
print('area_tc:', boreal_area_tc);

//throw('stop')
//Map.addLayer(fire_mask, {palette:'1AFFFF'}, 'fire_mask')
//Map.addLayer(tc_mask, {palette:'FFAAFF'}, 'tc_mask')


// values ---------------------------------------------------------------------------------------------------------------------

// decid
var decid_area_image_lim_ = area_img.updateMask(decid_diff.gte(lim));
var decid_area_image_0_lim = area_img.updateMask(decid_diff.gt(0.0).and(decid_diff.lt(lim)));
var decid_area_image__lim_0 = area_img.updateMask(decid_diff.lte(0.0).and(decid_diff.gt(-lim)));
var decid_area_image__lim = area_img.updateMask(decid_diff.lte(-lim));

// TC
var tc_area_image_lim_ = area_img.updateMask(tc_diff.gte(lim));
var tc_area_image_0_lim = area_img.updateMask(tc_diff.gt(0.0).and(tc_diff.lt(lim)));
var tc_area_image__lim_0 = area_img.updateMask(tc_diff.lte(0.0).and(tc_diff.gt(-lim)));
var tc_area_image__lim = area_img.updateMask(tc_diff.lte(-lim));

// decid_tc
var decid_tc_area_image_lim_ = area_img.updateMask(decid_diff_tc.gte(lim));
var decid_tc_area_image_0_lim = area_img.updateMask(decid_diff_tc.gt(0.0).and(decid_diff_tc.lt(lim)));

var decid_tc_area_image__lim_0 = area_img.updateMask(decid_diff_tc.lte(0.0).and(decid_diff_tc.gt(-lim)));
var decid_tc_area_image__lim = area_img.updateMask(decid_diff_tc.lte(-lim));

var evrgrn_diff_tc = tc_diff.subtract(decid_diff_tc);

Map.addLayer(evrgrn_diff_tc,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'evrgrn_diff_tc',false);

// evrgrn_tc
var evrgrn_tc_area_image_lim_ = area_img.updateMask(evrgrn_diff_tc.gte(lim));
var evrgrn_tc_area_image_0_lim = area_img.updateMask(evrgrn_diff_tc.gt(0.0).and(evrgrn_diff_tc.lt(lim)));
var evrgrn_tc_area_image__lim_0 = area_img.updateMask(evrgrn_diff_tc.gte(lim));
var evrgrn_tc_area_image__lim = area_img.updateMask(evrgrn_diff_tc.gt(0.0).and(evrgrn_diff_tc.lt(lim)));


// DECID vals-------------------------------------------------------------------------------------------------------------------------------
// recent
var decid_area_val_lim_rec = decid_area_image_lim_.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var decid_area_val_0_lim_rec = decid_area_image_0_lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_area_val__lim_0_rec = decid_area_image__lim_0.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var decid_area_val__lim_rec = decid_area_image__lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;       
                                                              
// interm
var decid_area_val_lim_intr = decid_area_image_lim_.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');   

var decid_area_val_0_lim_intr = decid_area_image_0_lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                          
var decid_area_val__lim_0_intr = decid_area_image__lim_0.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var decid_area_val__lim_intr = decid_area_image__lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                                 

// old    
var decid_area_val_lim_old = decid_area_image_lim_.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var decid_area_val_0_lim_old = decid_area_image_0_lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_area_val__lim_0_old = decid_area_image__lim_0.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var decid_area_val__lim_old = decid_area_image__lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area')  ;           
                                                              
                                                              
// all fire

var decid_area_val_lim = decid_area_image_lim_.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var decid_area_val_0_lim = decid_area_image_0_lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_area_val__lim_0 = decid_area_image__lim_0.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var decid_area_val__lim = decid_area_image__lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 
                                                              
                                                              
// all
var decid_area_val_lim_all = decid_area_image_lim_.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var decid_area_val_0_lim_all = decid_area_image_0_lim.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_area_val__lim_0_all = decid_area_image__lim_0.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var decid_area_val__lim_all = decid_area_image__lim.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 

// TC vals-------------------------------------------------------------------------------------------------------------------------------
//recent
var tc_area_val_lim_rec = tc_area_image_lim_.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var tc_area_val_0_lim_rec = tc_area_image_0_lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var tc_area_val__lim_0_rec = tc_area_image__lim_0.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ;  
                                                              
var tc_area_val__lim_rec = tc_area_image__lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');            

// interm
var tc_area_val_lim_intr = tc_area_image_lim_.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var tc_area_val_0_lim_intr = tc_area_image_0_lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                          
var tc_area_val__lim_0_intr = tc_area_image__lim_0.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var tc_area_val__lim_intr = tc_area_image__lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ;                                                                 

// old    
var tc_area_val_lim_old = tc_area_image_lim_.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var tc_area_val_0_lim_old = tc_area_image_0_lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                          
var tc_area_val__lim_0_old = tc_area_image__lim_0.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var tc_area_val__lim_old = tc_area_image__lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 
                                                              
//all fire
var tc_area_val_lim = tc_area_image_lim_.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')    ;

var tc_area_val_0_lim = tc_area_image_0_lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ;  
                                                          
var tc_area_val__lim_0 = tc_area_image__lim_0.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var tc_area_val__lim = tc_area_image__lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')    ;        


//all

var tc_area_val_lim_all = tc_area_image_lim_.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var tc_area_val_0_lim_all = tc_area_image_0_lim.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                          
var tc_area_val__lim_0_all = tc_area_image__lim_0.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var tc_area_val__lim_all = tc_area_image__lim.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;           
                                                              

// DECID TC vals-------------------------------------------------------------------------------------------------------------------------------
// recent
var decid_tc_area_val_lim_rec = decid_tc_area_image_lim_.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var decid_tc_area_val_0_lim_rec = decid_tc_area_image_0_lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_tc_area_val__lim_0_rec = decid_tc_area_image__lim_0.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var decid_tc_area_val__lim_rec = decid_tc_area_image__lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;       
                                                              
// interm
var decid_tc_area_val_lim_intr = decid_tc_area_image_lim_.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');   

var decid_tc_area_val_0_lim_intr = decid_tc_area_image_0_lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                          
var decid_tc_area_val__lim_0_intr = decid_tc_area_image__lim_0.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var decid_tc_area_val__lim_intr = decid_tc_area_image__lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                                 

// old    
var decid_tc_area_val_lim_old = decid_tc_area_image_lim_.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var decid_tc_area_val_0_lim_old = decid_tc_area_image_0_lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_tc_area_val__lim_0_old = decid_tc_area_image__lim_0.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var decid_tc_area_val__lim_old = decid_tc_area_image__lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area')  ;           
                                                              
                                                              
// all fire

var decid_tc_area_val_lim = decid_tc_area_image_lim_.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var decid_tc_area_val_0_lim = decid_tc_area_image_0_lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_tc_area_val__lim_0 = decid_tc_area_image__lim_0.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var decid_tc_area_val__lim = decid_tc_area_image__lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 
                                                              
                                                              
// all
var decid_tc_area_val_lim_all = decid_tc_area_image_lim_.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var decid_tc_area_val_0_lim_all = decid_tc_area_image_0_lim.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var decid_tc_area_val__lim_0_all = decid_tc_area_image__lim_0.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var decid_tc_area_val__lim_all = decid_tc_area_image__lim.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 

// EVRGRN TC vals-------------------------------------------------------------------------------------------------------------------------------
// recent
var evrgrn_tc_area_val_lim_rec = evrgrn_tc_area_image_lim_.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var evrgrn_tc_area_val_0_lim_rec = evrgrn_tc_area_image_0_lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var evrgrn_tc_area_val__lim_0_rec = evrgrn_tc_area_image__lim_0.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var evrgrn_tc_area_val__lim_rec = evrgrn_tc_area_image__lim.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;       
                                                              
// interm
var evrgrn_tc_area_val_lim_intr = evrgrn_tc_area_image_lim_.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');   

var evrgrn_tc_area_val_0_lim_intr = evrgrn_tc_area_image_0_lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                          
var evrgrn_tc_area_val__lim_0_intr = evrgrn_tc_area_image__lim_0.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var evrgrn_tc_area_val__lim_intr = evrgrn_tc_area_image__lim.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                                 

// old    
var evrgrn_tc_area_val_lim_old = evrgrn_tc_area_image_lim_.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var evrgrn_tc_area_val_0_lim_old = evrgrn_tc_area_image_0_lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var evrgrn_tc_area_val__lim_0_old = evrgrn_tc_area_image__lim_0.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var evrgrn_tc_area_val__lim_old = evrgrn_tc_area_image__lim.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area')  ;           
                                                              
                                                              
// all fire

var evrgrn_tc_area_val_lim = evrgrn_tc_area_image_lim_.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   

var evrgrn_tc_area_val_0_lim = evrgrn_tc_area_image_0_lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var evrgrn_tc_area_val__lim_0 = evrgrn_tc_area_image__lim_0.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                              
var evrgrn_tc_area_val__lim = evrgrn_tc_area_image__lim.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 
                                                              
                                                              
// all
var evrgrn_tc_area_val_lim_all = evrgrn_tc_area_image_lim_.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    

var evrgrn_tc_area_val_0_lim_all = evrgrn_tc_area_image_0_lim.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');    
                                                          
var evrgrn_tc_area_val__lim_0_all = evrgrn_tc_area_image__lim_0.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;   
                                                              
var evrgrn_tc_area_val__lim_all = evrgrn_tc_area_image__lim.multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,     
                                                              maxPixels:1e13}).get('area') ; 



print('decid_area_val_lim_rec:',   decid_area_val_lim_rec);
print('decid_area_val_0_lim_rec:',  decid_area_val_0_lim_rec);
print('decid_area_val__lim_0_rec:',   decid_area_val__lim_0_rec);
print('decid_area_val__lim_rec:',   decid_area_val__lim_rec);

print('decid_area_val_lim_intr:',   decid_area_val_lim_intr);
print('decid_area_val_0_lim_intr:',   decid_area_val_0_lim_intr);
print('decid_area_val__lim_0_intr:',   decid_area_val__lim_0_intr);
print('decid_area_val__lim_intr:',   decid_area_val__lim_intr);

print('decid_area_val_lim_old:',   decid_area_val_lim_old);
print('decid_area_val_0_lim_old:',   decid_area_val_0_lim_old);
print('decid_area_val__lim_0_old:',  decid_area_val__lim_0_old);
print('decid_area_val__lim_old:',   decid_area_val__lim_old);


print('decid_area_val_lim:',   decid_area_val_lim);
print('decid_area_val_0_lim:',   decid_area_val_0_lim);
print('decid_area_val__lim_0:',  decid_area_val__lim_0);
print('decid_area_val__lim:',   decid_area_val__lim);


print('decid_area_val_lim_all:',   decid_area_val_lim_all);
print('decid_area_val_0_lim_all:',   decid_area_val_0_lim_all);
print('decid_area_val__lim_0_all:',  decid_area_val__lim_0_all);
print('decid_area_val__lim_all:',   decid_area_val__lim_all);


print('tc_area_val_lim_rec:',   tc_area_val_lim_rec);
print('tc_area_val_0_lim_rec:',  tc_area_val_0_lim_rec);
print('tc_area_val__lim_0_rec:',   tc_area_val__lim_0_rec);
print('tc_area_val__lim_rec:',   tc_area_val__lim_rec);

print('tc_area_val_lim_intr:',   tc_area_val_lim_intr);
print('tc_area_val_0_lim_intr:',   tc_area_val_0_lim_intr);
print('tc_area_val__lim_0_intr:',   tc_area_val__lim_0_intr);
print('tc_area_val__lim_intr:',   tc_area_val__lim_intr);

print('tc_area_val_lim_old:',   tc_area_val_lim_old);
print('tc_area_val_0_lim_old:',   tc_area_val_0_lim_old);
print('tc_area_val__lim_0_old:',  tc_area_val__lim_0_old);
print('tc_area_val__lim_old:',   tc_area_val__lim_old);

//throw('stop')

print('tc_area_val_lim:',   tc_area_val_lim);
print('tc_area_val_0_lim:',   tc_area_val_0_lim);
print('tc_area_val__lim_0:',  tc_area_val__lim_0);
print('tc_area_val__lim:',   tc_area_val__lim);

print('tc_area_val_lim_all:',   tc_area_val_lim_all);
print('tc_area_val_0_lim_all:',   tc_area_val_0_lim_all);
print('tc_area_val__lim_0_all:',  tc_area_val__lim_0_all);
print('tc_area_val__lim_all:',   tc_area_val__lim_all);

//throw('stop')

print('decid_tc_area_val_lim_rec:',   decid_tc_area_val_lim_rec);
print('decid_tc_area_val_0_lim_rec:',  decid_tc_area_val_0_lim_rec);
print('decid_tc_area_val__lim_0_rec:',   decid_tc_area_val__lim_0_rec);
print('decid_tc_area_val__lim_rec:',   decid_tc_area_val__lim_rec);

print('decid_tc_area_val_lim_intr:',   decid_tc_area_val_lim_intr);
print('decid_tc_area_val_0_lim_intr:',   decid_tc_area_val_0_lim_intr);
print('decid_tc_area_val__lim_0_intr:',   decid_tc_area_val__lim_0_intr);
print('decid_tc_area_val__lim_intr:',   decid_tc_area_val__lim_intr);

print('decid_tc_area_val_lim_old:',   decid_tc_area_val_lim_old);
print('decid_tc_area_val_0_lim_old:',   decid_tc_area_val_0_lim_old);
print('decid_tc_area_val__lim_0_old:',  decid_tc_area_val__lim_0_old);
print('decid_tc_area_val__lim_old:',   decid_tc_area_val__lim_old);


print('decid_tc_area_val_lim:',   decid_tc_area_val_lim);
print('decid_tc_area_val_0_lim:',   decid_tc_area_val_0_lim);
print('decid_tc_area_val__lim_0:',  decid_tc_area_val__lim_0);
print('decid_tc_area_val__lim:',   decid_tc_area_val__lim);


print('decid_tc_area_val_lim_all:',   decid_tc_area_val_lim_all);
print('decid_tc_area_val_0_lim_all:',   decid_tc_area_val_0_lim_all);
print('decid_tc_area_val__lim_0_all:',  decid_tc_area_val__lim_0_all);
print('decid_tc_area_val__lim_all:',   decid_tc_area_val__lim_all);

//throw('stop')

print('evrgrn_tc_area_val_lim_rec:',   evrgrn_tc_area_val_lim_rec);
print('evrgrn_tc_area_val_0_lim_rec:',  evrgrn_tc_area_val_0_lim_rec);
print('evrgrn_tc_area_val__lim_0_rec:',   evrgrn_tc_area_val__lim_0_rec);
print('evrgrn_tc_area_val__lim_rec:',   evrgrn_tc_area_val__lim_rec);

print('evrgrn_tc_area_val_lim_intr:',   evrgrn_tc_area_val_lim_intr);
print('evrgrn_tc_area_val_0_lim_intr:',   evrgrn_tc_area_val_0_lim_intr);
print('evrgrn_tc_area_val__lim_0_intr:',   evrgrn_tc_area_val__lim_0_intr);
print('evrgrn_tc_area_val__lim_intr:',   evrgrn_tc_area_val__lim_intr);

print('evrgrn_tc_area_val_lim_old:',   evrgrn_tc_area_val_lim_old);
print('evrgrn_tc_area_val_0_lim_old:',   evrgrn_tc_area_val_0_lim_old);
print('evrgrn_tc_area_val__lim_0_old:',  evrgrn_tc_area_val__lim_0_old);
print('evrgrn_tc_area_val__lim_old:',   evrgrn_tc_area_val__lim_old);


print('evrgrn_tc_area_val_lim:',   evrgrn_tc_area_val_lim);
print('evrgrn_tc_area_val_0_lim:',   evrgrn_tc_area_val_0_lim);
print('evrgrn_tc_area_val__lim_0:',  evrgrn_tc_area_val__lim_0);
print('evrgrn_tc_area_val__lim:',   evrgrn_tc_area_val__lim);


print('evrgrn_tc_area_val_lim_all:',   evrgrn_tc_area_val_lim_all);
print('evrgrn_tc_area_val_0_lim_all:',   evrgrn_tc_area_val_0_lim_all);
print('evrgrn_tc_area_val__lim_0_all:',  evrgrn_tc_area_val__lim_0_all);
print('evrgrn_tc_area_val__lim_all:',   evrgrn_tc_area_val__lim_all);
