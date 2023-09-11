/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var land = ee.Image("users/masseyr44/decid/land_extent_NA"),
    tiles = ee.FeatureCollection("users/masseyr44/shapefiles/decid_tc_layerstack_tiles"),
    ak_fire = ee.FeatureCollection("users/masseyr44/shapefiles/ak_fire_multi"),
    alb_sum2000_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_sum_albedo_vis_v2"),
    alb_sum2015_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_sum_albedo_vis_v2"),
    alb_fall2000_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_fall_albedo_vis_v2"),
    alb_fall2015_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_fall_albedo_vis_v2"),
    alb_spr2000_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_spr_albedo_vis_v2"),
    alb_spr2015_v2 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_spr_albedo_vis_v2"),
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
    alb_fall2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_fall_albedo_vis_uncert"),
    alb_spr2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_spr_albedo_vis_uncert"),
    alb_sum2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_sum_albedo_vis_uncert"),
    alb_fall2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_fall_albedo_vis_uncert"),
    alb_spr2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_spr_albedo_vis_uncert"),
    alb_sum2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_sum_albedo_vis_uncert"),
    tc1992 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_1992_tc_prediction_vis_nd"),
    tc2005 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2005_tc_prediction_vis_nd"),
    tc2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd"),
    NABoreal_boreal_10km_buffer = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal_10km_buffer"),
    boreal = ee.FeatureCollection("users/masseyr44/shapefiles/NABoreal_boreal_geo_merged"),
    aci = ee.ImageCollection("AAFC/ACI"),
    ecozones = ee.FeatureCollection("users/masseyr44/shapefiles/boreal_ecozones"),
    may_kernel = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_may_250m"),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3_blended"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3_blended"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3_blended"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3_blended"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3_blended"),
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
    boreal_mask = ee.Image("users/masseyr44/decid/borealMask");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
Map.setOptions('SATELLITE');

var lim = 0.1;
var calc_scale = 250;
print(lim);

var uncert_calc = function(img_old, img_new, uncert_old, uncert_new){
  return ee.Image(0.02)
           .multiply((ee.Image(img_old).toFloat()).multiply(ee.Image(uncert_new).toFloat())
                        .add((ee.Image(img_new)).toFloat().multiply(ee.Image(uncert_old).toFloat())))
           .divide((ee.Image(img_old).toFloat()).multiply(ee.Image(img_old).toFloat())).abs()
}

var change_calc = function(img_old, img_new){
  return ((ee.Image(img_new).toFloat()).subtract(ee.Image(img_old).toFloat())).divide(ee.Image(img_old).toFloat())
}

var vis_decid = {min:0, max:100, palette:'286F09,ECC519'};
var vis_decid_diff = {min:-0.25, max:0.25, palette:'286F09,ECC519'};
var vis_tc = {min:0, max:100, palette:'B62809,FFC560,1178C8'};
var vis_tc_diff = {min:-0.25, max:0.25, palette:'B62809,FFC560,1178C8'};

//Map.addLayer(boreal_geom);

//Map.addLayer(alb_spr2015_v2.float().divide(100.0), {min:0, max:1, palette: 'B62809,FFC560,1178C8'}, 'alb_spr_2015', false);
//Map.addLayer(alb_spr2000_v2.float().divide(100.0), {min:0, max:1, palette: 'B62809,FFC560,1178C8'}, 'alb_spr_2000', false);
//Map.addLayer(albedo_2015r.float().divide(1000.0), {min:0, max:1, palette: 'B62809,FFC560,1178C8'}, 'alb_spr_2013', false);
//Map.addLayer(may_kernel, {min:-5, max:0}, 'may_kernel')

//var spr_pdiff = ee.Image(alb_spr2015_v2.subtract(alb_spr2000_v2)).divide(alb_spr2000_v2).clip(boreal_bounds).toFloat();

//Map.addLayer(spr_pdiff, {min:-2, max:2, palette: 'B62809,FFC560,1178C8'}, 'spr_alb_pdiff', false);
//Map.addLayer(decid2000.multiply(land), vis_decid, 'decid2000')

//throw('stop')

var tc_max = ee.ImageCollection([tc2000,tc2010,tc2005,tc2015]).reduce(ee.Reducer.max()); 
var tc_min = ee.ImageCollection([tc2000,tc2010,tc2005,tc2015]).reduce(ee.Reducer.min()); 

var tc_mask = boreal_mask.updateMask(tc_max.gt(25));

var top_fire_layer = top_fire_layer.updateMask(top_fire_layer.gt(0)).multiply(tc_mask).rename('top_fire_layer').toFloat();
//Map.addLayer(top_fire_layer,{min:1900, max: 2018, palette:'A8FB9E,F4DD36,0B3D05'},'top_fire_layer');

//alb_spr2000_v2 = alb_spr2000_v2.toFloat();
//alb_spr2015_v2 = alb_spr2015_v2.toFloat();
//
//alb_sum2000_v2 = alb_sum2000_v2.toFloat();
//alb_sum2015_v2 = alb_sum2015_v2.toFloat();
//
//alb_fall2000_v2 = alb_fall2000_v2.toFloat();
//alb_fall2015_v2 = alb_fall2015_v2.toFloat();



//var decid_min = ee.ImageCollection([decid2000, decid2015]).reduce(ee.Reducer.min()); //decid2010,decid2005,
//var decid_mask = ee.Image(1).updateMask(decid_min.neq(0));

//var tc_mask0 = tc_mask
//var tc_mask = tc_mask.multiply(decid_mask)

var fall_diff = change_calc(alb_fall2000_v2, alb_fall2015_v2).updateMask(tc_mask).multiply(land);
var fall_udiff = uncert_calc(alb_fall2000_v2, alb_fall2015_v2, alb_fall2000_uncert, alb_fall2015_uncert).updateMask(tc_mask);
//Map.addLayer(fall_diff, {min:-.5, max:.5, palette: 'B62809,FFC560,1178C8'}, 'fall_alb_diff', true);
//Map.addLayer(fall_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'fall_alb_udiff', true);

var sum_diff = change_calc(alb_sum2000_v2, alb_sum2015_v2).updateMask(tc_mask).multiply(land);
var sum_udiff = uncert_calc(alb_sum2000_v2, alb_sum2015_v2, alb_fall2000_uncert, alb_fall2015_uncert).updateMask(tc_mask);
//Map.addLayer(sum_diff, {min:-.25, max:.25, palette: 'B62809,FFC560,1178C8'}, 'summer_alb_diff', true);
//Map.addLayer(sum_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'summer_alb_udiff', true);

var spr_diff = change_calc(alb_spr2000_v2, alb_spr2015_v2).updateMask(tc_mask).multiply(land);
var spr_udiff = uncert_calc(alb_spr2000_v2, alb_spr2015_v2, alb_spr2015_uncert, alb_spr2015_uncert).updateMask(tc_mask);
//Map.addLayer(spr_diff, {min:-.5, max:.5, palette: 'B62809,FFC560,1178C8'}, 'spring_alb_diff', true);
//Map.addLayer(spr_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'spring_alb_udiff', true);


//tc2015 = tc2015.multiply(1.07);
//var tc2015_gt100 = tc2015.updateMask(tc2015.gt(100)).subtract(100).unmask(0);
//tc2015 = tc2015.subtract(tc2015_gt100).floor();


var tc_diff = tc2015.subtract(tc2000).updateMask(tc_mask).multiply(land).toFloat().multiply(0.01);
//Map.addLayer(tc_diff,{min:-0.25, max:0.25, palette: 'B62809,FFC560,1178C8'},'tc_diff');

var decid_diff = ee.Image(decid2015).subtract(ee.Image(decid2000)).updateMask(tc_mask).multiply(land).toFloat().multiply(0.01);
//var decid_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5) * 0.5',{'a': decid2000u.toFloat().divide(2.0), 'b': decid2015u.toFloat().divide(2.0)}).updateMask(tc_mask).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);

//throw('stop')

//Map.addLayer(decid_diff,vis_decid_diff,'decid_diff');

//Map.addLayer(decid_diff0,vis_decid_diff,'decid_diff0');

//Map.addLayer(decid2000.updateMask(tc_mask).multiply(land),vis_decid,'decid2000', false);
//Map.addLayer(decid2015.updateMask(tc_mask).multiply(land),vis_decid,'decid2015', false);

//Map.addLayer(tc2000,vis_tc,'tc2000', false);
//Map.addLayer(tc2015,vis_tc,'tc2015', false);


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

var spr_kernel = ee.ImageCollection([cam5_apr, cam5_may]).reduce(ee.Reducer.mean()).toFloat();

var sum_kernel = ee.ImageCollection([cam5_jun, cam5_jul, cam5_aug]).reduce(ee.Reducer.mean()).toFloat();

var fall_kernel = ee.ImageCollection([cam5_sep, cam5_oct]).reduce(ee.Reducer.mean()).toFloat();


var sum_forc = sum_kernel.multiply(sum_diff);
var spr_forc = spr_kernel.multiply(spr_diff);
var fall_forc = fall_kernel.multiply(fall_diff);

//Map.addLayer(sum_forc,{min:-.25, max:.25, palette:'B62809,FFC560,1178C8'},'sum');
//Map.addLayer(spr_forc,{min:-5, max:5, palette:'B62809,FFC560,1178C8'},'spr');
//Map.addLayer(fall_forc,{min:-2.5, max:2.5, palette:'B62809,FFC560,1178C8'},'fall');


var sum_uforc = sum_kernel.multiply(sum_udiff).abs();
var spr_uforc = spr_kernel.multiply(spr_udiff).abs();
var fall_uforc = fall_kernel.multiply(fall_udiff).abs();

//Map.addLayer(sum_uforc,{min:-.1, max:.1, palette:'B62809,FFC560,1178C8'},'sum_u');
//Map.addLayer(spr_uforc,{min:-1, max:1, palette:'B62809,FFC560,1178C8'},'spr_u');
//Map.addLayer(fall_uforc,{min:-.25, max:.25, palette:'B62809,FFC560,1178C8'},'fall_u');


var area_img = ee.Image.pixelArea().multiply(tc_mask);

var fire_mask = top_fire_layer.multiply(0).add(1);

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


Map.addLayer(fire_mask, {palette:'1AFFFF'}, 'fire_mask')
Map.addLayer(tc_mask, {palette:'FFAAFF'}, 'tc_mask')

throw('stop')

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

// spr
var pos_spr_area_image = area_img.updateMask(spr_forc.gt(0));
var pos_spr_area_val = pos_spr_area_image.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');
var pos_spr_area_val_fire_mask = pos_spr_area_image.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_spr_area_val_recent_fire_mask = pos_spr_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_spr_area_val_interm_fire_mask = pos_spr_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');                                                           
var pos_spr_area_val_old_fire_mask = pos_spr_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                          
                                                              
                                                              
var neg_spr_area_image = area_img.updateMask(spr_forc.lt(0))
var neg_spr_area_val = neg_spr_area_image.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');
var neg_spr_area_val_fire_mask = neg_spr_area_image.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var neg_spr_area_val_recent_fire_mask = neg_spr_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 
var neg_spr_area_val_interm_fire_mask = neg_spr_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');                                                           
var neg_spr_area_val_old_fire_mask = neg_spr_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;    
// sum
var pos_sum_area_image = area_img.updateMask(sum_forc.gt(0));
var pos_sum_area_val = pos_sum_area_image.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');
var pos_sum_area_val_fire_mask = pos_sum_area_image.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_sum_area_val_recent_fire_mask = pos_sum_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_sum_area_val_interm_fire_mask = pos_sum_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                          
var pos_sum_area_val_old_fire_mask = pos_sum_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');   

var neg_sum_area_image = area_img.updateMask(sum_forc.lt(0));
var neg_sum_area_val = neg_sum_area_image.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');
var neg_sum_area_val_fire_mask = neg_sum_area_image.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var neg_sum_area_val_recent_fire_mask = neg_sum_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var neg_sum_area_val_interm_fire_mask = neg_sum_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                          
var neg_sum_area_val_old_fire_mask = neg_sum_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ; 
// fall
var pos_fall_area_image = area_img.updateMask(fall_forc.gt(0));
var pos_fall_area_val = pos_fall_area_image.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');
var pos_fall_area_val_fire_mask = pos_fall_area_image.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_fall_area_val_recent_fire_mask = pos_fall_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_fall_area_val_interm_fire_mask = pos_fall_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ;                                                         
var pos_fall_area_val_old_fire_mask = pos_fall_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')   ;
                                                              
var neg_fall_area_image = area_img.updateMask(fall_forc.lt(0));
var neg_fall_area_val = neg_fall_area_image.reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');
var neg_fall_area_val_fire_mask = neg_fall_area_image.multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 
var neg_fall_area_val_recent_fire_mask = neg_fall_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 
var neg_fall_area_val_interm_fire_mask = neg_fall_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');                                                           
var neg_fall_area_val_old_fire_mask = neg_fall_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 

// uncertainty vals ------------------------------------------------------------------------------------------------------------------------

// spr

var pos_spr_area_u_val_recent_fire_mask = pos_spr_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 
var pos_spr_area_u_val_interm_fire_mask = pos_spr_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');                                                           
var pos_spr_area_u_val_old_fire_mask = pos_spr_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');                                                           
                                                              
                                                              
var neg_spr_area_u_val_recent_fire_mask = neg_spr_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var neg_spr_area_u_val_interm_fire_mask = neg_spr_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                          
var neg_spr_area_u_val_old_fire_mask = neg_spr_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');     
// sum
var pos_sum_area_u_val_recent_fire_mask = pos_sum_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 
var pos_sum_area_u_val_interm_fire_mask = pos_sum_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ;                                                         
var pos_sum_area_u_val_old_fire_mask = pos_sum_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ; 

var neg_sum_area_u_val_recent_fire_mask = neg_sum_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var neg_sum_area_u_val_interm_fire_mask = neg_sum_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;                                                          
var neg_sum_area_u_val_old_fire_mask = neg_sum_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  
// fall
var pos_fall_area_u_val_recent_fire_mask = pos_fall_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var pos_fall_area_u_val_interm_fire_mask = pos_fall_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ;                                                         
var pos_fall_area_u_val_old_fire_mask = pos_fall_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')  ; 

var neg_fall_area_u_val_recent_fire_mask = neg_fall_area_image.multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area') ;
var neg_fall_area_u_val_interm_fire_mask = neg_fall_area_image.multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area');                                                     
var neg_fall_area_u_val_old_fire_mask = neg_fall_area_image.multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area'); 



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
                                                              

// ---------------------------------------------------------------------------------------------------------------------------------
//seasons

// recent fire
var pos_spr_area_val_rec = ee.Number(pos_spr_area_image.multiply(spr_forc).multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_spr_area_val_recent_fire_mask);
var neg_spr_area_val_rec = ee.Number(neg_spr_area_image.multiply(spr_forc).multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(neg_spr_area_val_recent_fire_mask)  ;

var pos_sum_area_val_rec = ee.Number(pos_sum_area_image.multiply(sum_forc).multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_sum_area_val_recent_fire_mask);    
var neg_sum_area_val_rec = ee.Number(neg_sum_area_image.multiply(sum_forc).multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(neg_sum_area_val_recent_fire_mask) ;       

var pos_fall_area_val_rec = ee.Number(pos_fall_area_image.multiply(fall_forc).multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_fall_area_val_recent_fire_mask);   
var neg_fall_area_val_rec = ee.Number(neg_fall_area_image.multiply(fall_forc).multiply(recent_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(neg_fall_area_val_recent_fire_mask);    


// interm fire
var pos_spr_area_val_intr = ee.Number(pos_spr_area_image.multiply(spr_forc).multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_spr_area_val_interm_fire_mask) ;   
var neg_spr_area_val_intr = ee.Number(neg_spr_area_image.multiply(spr_forc).multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_spr_area_val_interm_fire_mask);    

var pos_sum_area_val_intr = ee.Number(pos_sum_area_image.multiply(sum_forc).multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_sum_area_val_interm_fire_mask) ;    
var neg_sum_area_val_intr = ee.Number(neg_sum_area_image.multiply(sum_forc).multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(neg_sum_area_val_interm_fire_mask);     

var pos_fall_area_val_intr = ee.Number(pos_fall_area_image.multiply(fall_forc).multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_fall_area_val_interm_fire_mask) ;    
var neg_fall_area_val_intr = ee.Number(neg_fall_area_image.multiply(fall_forc).multiply(interm_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(neg_fall_area_val_interm_fire_mask);     
                                                              
                                                              
// old fire                                                              
var pos_spr_area_val_old = ee.Number(pos_spr_area_image.multiply(spr_forc).multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_spr_area_val_old_fire_mask);    
var neg_spr_area_val_old = ee.Number(neg_spr_area_image.multiply(spr_forc).multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_spr_area_val_old_fire_mask) ;   

var pos_sum_area_val_old = ee.Number(pos_sum_area_image.multiply(sum_forc).multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_sum_area_val_old_fire_mask);     
var neg_sum_area_val_old = ee.Number(neg_sum_area_image.multiply(sum_forc).multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(neg_sum_area_val_old_fire_mask) ;    

var pos_fall_area_val_old = ee.Number(pos_fall_area_image.multiply(fall_forc).multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,
                                                              maxPixels:1e13}).get('area')).divide(pos_fall_area_val_old_fire_mask) ;    
var neg_fall_area_val_old = ee.Number(neg_fall_area_image.multiply(fall_forc).multiply(old_fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,                      
                                                              maxPixels:1e13}).get('area')).divide(neg_fall_area_val_old_fire_mask);    
                                                              
//fire
var pos_spr_area_val_fc= ee.Number(pos_spr_area_image.multiply(spr_forc).multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(pos_spr_area_val_fire_mask) ;   
var neg_spr_area_val_fc= ee.Number(neg_spr_area_image.multiply(spr_forc).multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(pos_spr_area_val_fire_mask);
                                                         
var pos_sum_area_val_fc= ee.Number(pos_sum_area_image.multiply(sum_forc).multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(pos_sum_area_val_fire_mask);     
var neg_sum_area_val_fc= ee.Number(neg_sum_area_image.multiply(sum_forc).multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(neg_sum_area_val_fire_mask) ;    

var pos_fall_area_val_fc = ee.Number(pos_fall_area_image.multiply(fall_forc).multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(pos_fall_area_val_fire_mask) ;
                                                         
var neg_fall_area_val_fc = ee.Number(neg_fall_area_image.multiply(fall_forc).multiply(fire_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,                      
                                                         maxPixels:1e13}).get('area')).divide(neg_fall_area_val_fire_mask)  ;        
                                                              
//all
var pos_spr_area_val_all= ee.Number(pos_spr_area_image.multiply(spr_forc).multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(boreal_area_tc)    ;
var neg_spr_area_val_all= ee.Number(neg_spr_area_image.multiply(spr_forc).multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(boreal_area_tc) ;   

var pos_sum_area_val_all= ee.Number(pos_sum_area_image.multiply(sum_forc).multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(boreal_area_tc)  ;   
var neg_sum_area_val_all= ee.Number(neg_sum_area_image.multiply(sum_forc).multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(boreal_area_tc) ;    

var pos_fall_area_val_all = ee.Number(pos_fall_area_image.multiply(fall_forc).multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                         geometry:boreal_geom,
                                                         scale:calc_scale,
                                                         maxPixels:1e13}).get('area')).divide(boreal_area_tc) ;    
var neg_fall_area_val_all = ee.Number(neg_fall_area_image.multiply(fall_forc).multiply(tc_mask).reduceRegion({reducer:ee.Reducer.sum(),
                                                              geometry:boreal_geom,
                                                              scale:calc_scale,                      
                                                              maxPixels:1e13}).get('area')).divide(boreal_area_tc) ;   
                                                              

// uncertainty -------------------------------------------------------------------------------------------------------------------------------------


//Map.addLayer(pos_spr_area_image);

var rms_u = function(img){
  
  return ee.Number(ee.Image(img).reduceRegion(ee.Reducer.stdDev(), boreal_geom, 1000, null, null, false, 1e13).get('area'));
  // var num_pix = ee.Image(ee.Image(img).multiply(0).add(1)).reduceRegion(ee.Reducer.sum(),boreal_geom, 1000, null, null, false, 1e13).get('area');
  // var u_var = ee.Number(ee.Image(img.multiply(img)).reduceRegion(ee.Reducer.sum(),boreal_geom, 1000, null, null, false, 1e13).get('area'));
  //return ee.Number(u_var).divide(num_pix);
};

// recent fire
var pos_spr_area_u_val_rec = ee.Number(rms_u(pos_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(recent_fire_mask)));
//print('pos_spr_area_u_val_rec:',  pos_spr_area_u_val_rec);
//throw('stop')
var neg_spr_area_u_val_rec = ee.Number(rms_u(neg_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(recent_fire_mask)));

var pos_sum_area_u_val_rec = ee.Number(rms_u(pos_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(recent_fire_mask)));
var neg_sum_area_u_val_rec = ee.Number(rms_u(neg_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(recent_fire_mask)));

var pos_fall_area_u_val_rec = ee.Number(rms_u(pos_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(recent_fire_mask)));
var neg_fall_area_u_val_rec = ee.Number(rms_u(neg_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(recent_fire_mask)));

// interm fire
var pos_spr_area_u_val_intr = ee.Number(rms_u(pos_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(interm_fire_mask)));
var neg_spr_area_u_val_intr = ee.Number(rms_u(neg_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(interm_fire_mask)));
 
var pos_sum_area_u_val_intr = ee.Number(rms_u(pos_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(interm_fire_mask)));
var neg_sum_area_u_val_intr = ee.Number(rms_u(neg_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(interm_fire_mask)));

var pos_fall_area_u_val_intr = ee.Number(rms_u(pos_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(interm_fire_mask)));
var neg_fall_area_u_val_intr = ee.Number(rms_u(neg_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(interm_fire_mask)));

// old fire
var pos_spr_area_u_val_old = ee.Number(rms_u(pos_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(old_fire_mask)));
var neg_spr_area_u_val_old = ee.Number(rms_u(neg_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(old_fire_mask)));

var pos_sum_area_u_val_old = ee.Number(rms_u(pos_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(old_fire_mask)));
var neg_sum_area_u_val_old = ee.Number(rms_u(neg_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(old_fire_mask)));

var pos_fall_area_u_val_old = ee.Number(rms_u(pos_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(old_fire_mask)));
var neg_fall_area_u_val_old = ee.Number(rms_u(neg_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(old_fire_mask)));


// fire
var pos_spr_area_u_val_fc = ee.Number(rms_u(pos_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(fire_mask)));
var neg_spr_area_u_val_fc = ee.Number(rms_u(neg_spr_area_image.multiply(0).add(1).multiply(spr_uforc).multiply(fire_mask)));

var pos_sum_area_u_val_fc = ee.Number(rms_u(pos_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(fire_mask)));
var neg_sum_area_u_val_fc = ee.Number(rms_u(neg_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(fire_mask)));

var pos_fall_area_u_val_fc = ee.Number(rms_u(pos_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(fire_mask)));
var neg_fall_area_u_val_fc = ee.Number(rms_u(neg_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(fire_mask)));


// all
var pos_spr_area_u_val_all = ee.Number(rms_u(pos_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(boreal_mask)));
var neg_spr_area_u_val_all = ee.Number(rms_u(neg_spr_area_image.multiply(0).add(1).multiply(spr_forc).multiply(boreal_mask)));

var pos_sum_area_u_val_all = ee.Number(rms_u(pos_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(boreal_mask)));
var neg_sum_area_u_val_all = ee.Number(rms_u(neg_sum_area_image.multiply(0).add(1).multiply(sum_forc).multiply(boreal_mask)));

var pos_fall_area_u_val_all = ee.Number(rms_u(pos_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(boreal_mask)));
var neg_fall_area_u_val_all = ee.Number(rms_u(neg_fall_area_image.multiply(0).add(1).multiply(fall_forc).multiply(boreal_mask)));                                            




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

//throw('stop')

print('decid_area_val_lim:',   decid_area_val_lim);
print('decid_area_val_0_lim:',   decid_area_val_0_lim);
print('decid_area_val__lim_0:',  decid_area_val__lim_0);
print('decid_area_val__lim:',   decid_area_val__lim);


print('decid_area_val_lim_all:',   decid_area_val_lim_all);
print('decid_area_val_0_lim_all:',   decid_area_val_0_lim_all);
print('decid_area_val__lim_0_all:',  decid_area_val__lim_0_all);
print('decid_area_val__lim_all:',   decid_area_val__lim_all);

throw('stop')

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


print('pos_spr_area_val_rec:',  pos_spr_area_val_rec);
print('neg_spr_area_val_rec:',  neg_spr_area_val_rec);
print('pos_sum_area_val_rec:',  pos_sum_area_val_rec);
print('neg_sum_area_val_rec:',  neg_sum_area_val_rec);
print('pos_fall_area_val_rec:',  pos_fall_area_val_rec);
print('neg_fall_area_val_rec:',  neg_fall_area_val_rec)                                                    

print('pos_spr_area_val_intr:',  pos_spr_area_val_intr);
print('neg_spr_area_val_intr:',  neg_spr_area_val_intr);
print('pos_sum_area_val_intr:',  pos_sum_area_val_intr);
print('neg_sum_area_val_intr:',  neg_sum_area_val_intr);
print('pos_fall_area_val_intr:',  pos_fall_area_val_intr);
print('neg_fall_area_val_intr:',  neg_fall_area_val_intr)      

print('pos_spr_area_val_old:',  pos_spr_area_val_old);
print('neg_spr_area_val_old:',  neg_spr_area_val_old);
print('pos_sum_area_val_old:',  pos_sum_area_val_old);
print('neg_sum_area_val_old:',  neg_sum_area_val_old);
print('pos_fall_area_val_old:',  pos_fall_area_val_old);
print('neg_fall_area_val_old:',  neg_fall_area_val_old)    

//throw('stop')

print('pos_spr_area_val_fc:',  pos_spr_area_val_fc);
print('neg_spr_area_val_fc:',  neg_spr_area_val_fc);
print('pos_sum_area_val_fc:',  pos_sum_area_val_fc);
print('neg_sum_area_val_fc:',  neg_sum_area_val_fc);
print('pos_fall_area_val_fc:',  pos_fall_area_val_fc);
print('neg_fall_area_val_fc:',  neg_fall_area_val_fc);

print('pos_spr_area_val_all:',  pos_spr_area_val_all);
print('neg_spr_area_val_all:',  neg_spr_area_val_all);
print('pos_sum_area_val_all:',  pos_sum_area_val_all);
print('neg_sum_area_val_all:',  neg_sum_area_val_all);
print('pos_fall_area_val_all:',  pos_fall_area_val_all);
print('neg_fall_area_val_all:',  neg_fall_area_val_all)     

//throw('stop')


print('pos_spr_area_u_val_rec:',  pos_spr_area_u_val_rec);
print('neg_spr_area_u_val_rec:',  neg_spr_area_u_val_rec);
print('pos_sum_area_u_val_rec:',  pos_sum_area_u_val_rec);
print('neg_sum_area_u_val_rec:',  neg_sum_area_u_val_rec);
print('pos_fall_area_u_val_rec:',  pos_fall_area_u_val_rec);
print('neg_fall_area_u_val_rec:',  neg_fall_area_u_val_rec)                                                    

print('pos_spr_area_u_val_intr:',  pos_spr_area_u_val_intr);
print('neg_spr_area_u_val_intr:',  neg_spr_area_u_val_intr);
print('pos_sum_area_u_val_intr:',  pos_sum_area_u_val_intr);
print('neg_sum_area_u_val_intr:',  neg_sum_area_u_val_intr);
print('pos_fall_area_u_val_intr:',  pos_fall_area_u_val_intr);
print('neg_fall_area_u_val_intr:',  neg_fall_area_u_val_intr)      

print('pos_spr_area_u_val_old:',  pos_spr_area_u_val_old);
print('neg_spr_area_u_val_old:',  neg_spr_area_u_val_old);
print('pos_sum_area_u_val_old:',  pos_sum_area_u_val_old);
print('neg_sum_area_u_val_old:',  neg_sum_area_u_val_old);
print('pos_fall_area_u_val_old:',  pos_fall_area_u_val_old);
print('neg_fall_area_u_val_old:',  neg_fall_area_u_val_old)      

//throw('stop')

print('pos_spr_area_u_val_fc:',  pos_spr_area_u_val_fc);
print('neg_spr_area_u_val_fc:',  neg_spr_area_u_val_fc);
print('pos_sum_area_u_val_fc:',  pos_sum_area_u_val_fc);
print('neg_sum_area_u_val_fc:',  neg_sum_area_u_val_fc);
print('pos_fall_area_u_val_fc:',  pos_fall_area_u_val_fc);
print('neg_fall_area_u_val_fc:',  neg_fall_area_u_val_fc)      

print('pos_spr_area_u_val_all:',  pos_spr_area_u_val_all);
print('neg_spr_area_u_val_all:',  neg_spr_area_u_val_all);
print('pos_sum_area_u_val_all:',  pos_sum_area_u_val_all);
print('neg_sum_area_u_val_all:',  neg_sum_area_u_val_all);
print('pos_fall_area_u_val_all:',  pos_fall_area_u_val_all);
print('neg_fall_area_u_val_all:',  neg_fall_area_u_val_all)      




