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
    decid2000u = ee.Image("users/masseyr44/decid/decid_mosaic_2000_uncertainty_vis_nd_3"),
    decid2015u = ee.Image("users/masseyr44/decid/decid_mosaic_2015_uncertainty_vis_nd_3"),
    tc2000u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2000_tc_uncertainty_vis_nd"),
    tc2015u = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_tc_uncertainty_vis_nd"),
    canada = ee.Image("users/masseyr44/decid/canada_extent"),
    usa = ee.Image("users/masseyr44/decid/usa_extent"),
    geometry2 = 
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-155.80680700629483, 72.07505332283668],
          [-135.94352575629483, 70.78813066679383],
          [-134.44938513129483, 69.25746320387034],
          [-132.07633825629483, 64.36053632497004],
          [-124.78141638129483, 53.802841823327164],
          [-133.74626013129483, 52.858104240308876],
          [-141.83219763129483, 54.82814507275498],
          [-150.26969763129483, 54.318687194246635],
          [-166.77116247504483, 52.02774128881235],
          [-176.39518591254483, 50.98843429009763],
          [177.95784143120514, 50.038356506311025],
          [-179.40543981879483, 52.12227651444999],
          [-174.00016638129483, 58.724524888490535],
          [-174.08805700629483, 61.31423239840859],
          [-173.38493200629483, 63.47180177784182],
          [-169.78141638129483, 65.1476740938403],
          [-168.37516638129483, 67.13727081605765],
          [-165.56266638129483, 70.46744783699157]]]),
    geometry3 = 
    /* color: #98ff00 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[176.58936947959523, 49.88464219752121],
          [-177.17039614540477, 53.895199948885974],
          [-173.30320864540477, 57.31814744150824],
          [-175.93992739540477, 61.09329264908746],
          [-171.36961489540477, 64.39023477002657],
          [-168.29344302040477, 66.75112859276959],
          [-169.43602114540477, 68.71481116063457],
          [-161.52586489540477, 70.897193203831],
          [-155.19773989540477, 71.96058546381337],
          [-138.14695864540477, 71.46419438687242],
          [-128.21531802040477, 74.65591284831918],
          [-121.71141177040477, 77.78290886573868],
          [-111.77977114540477, 79.87156985844518],
          [-95.87156802040477, 81.8465562927456],
          [-87.34617739540477, 82.95999736211907],
          [-64.67039614540477, 83.38814695733231],
          [-62.033677395404766, 83.02433550908573],
          [-60.012193020404766, 82.60675852528352],
          [-60.803208645404766, 82.09210910670257],
          [-63.352036770404766, 80.96746943703498],
          [-68.36180239540477, 79.68440723375927],
          [-72.22898989540477, 77.80149402310667],
          [-70.64695864540477, 74.97816335939795],
          [-58.781724270404766, 70.4316048459928],
          [-53.068833645404766, 64.50396792991071],
          [-52.893052395404766, 58.11612842521147],
          [-47.065760639523546, 45.57444046927694],
          [-51.460291889523546, 41.76188159640533],
          [-59.194666889523546, 40.77096712755288],
          [-65.96224501452355, 40.837495645361],
          [-83.27669813952355, 40.10201861651301],
          [-89.51693251452355, 40.9039574622696],
          [-97.77865126452355, 43.76196337747021],
          [-109.90755751452355, 46.186289745605485],
          [-126.07943251452355, 45.81998874216508],
          [-135.57162001452355, 47.03156532188163],
          [-142.42708876452355, 51.33644057555614],
          [-148.40365126452355, 54.10353063709806],
          [-164.0069914829572, 51.719196194911255],
          [-171.4776946079572, 50.728452744695396],
          [-176.6632414829572, 49.886489044943104],
          [178.15121164204282, 48.21624893956041]]]),
    canada_ak = ee.Image("users/masseyr44/decid/canada_ak"),
    canlad_yrt = ee.Image("users/masseyr44/decid/CanLaD_20151984_latest_YRT2"),
    distr_type = ee.Image("users/masseyr44/decid/CanLaD_20151984_latest_type"),
    decid1992 = ee.Image("users/masseyr44/decid/decid_mosaic_1992_prediction_vis_nd_3"),
    decid2000 = ee.Image("users/masseyr44/decid/decid_mosaic_2000_prediction_vis_nd_3"),
    decid2005 = ee.Image("users/masseyr44/decid/decid_mosaic_2005_prediction_vis_nd_3"),
    decid2010 = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_3"),
    decid2015 = ee.Image("users/masseyr44/decid/decid_mosaic_2015_prediction_vis_nd_3"),
    cam5_mar = ee.Image("users/masseyr44/kernels/alb_kernel_FSNS_mar_250m"),
    alb_fal2000 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_fall_albedo_vis_v2"),
    alb_spr2000 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_spr_albedo_vis_v2"),
    alb_sum2000 = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_sum_albedo_vis_v2"),
    alb_fall2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_fall_albedo_vis_uncert"),
    alb_spr2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_spr_albedo_vis_uncert"),
    alb_sum2000_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2000_sum_albedo_vis_uncert"),
    alb_fal2015 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_fall_albedo_vis_v2"),
    alb_spr2015 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_spr_albedo_vis_v2"),
    alb_sum2015 = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_sum_albedo_vis_v2"),
    alb_fall2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_fall_albedo_vis_uncert"),
    alb_spr2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_spr_albedo_vis_uncert"),
    alb_sum2015_uncert = ee.Image("users/masseyr44/albedo_products/decid_tc_2015_sum_albedo_vis_uncert");
/***** End of imports. If edited, may not auto-convert in the playground. *****/
Map.setOptions('SATELLITE');
var canada_ak = ee.ImageCollection([usa.clip(geometry2), canada]).mosaic();
Map.addLayer(canada_ak, {}, 'canada_ak', false);
Map.addLayer(boreal_mask, {palette:"ffffff"}, 'boreal_mask', false);

Map.addLayer(distr_type, {min: 1, max:2, palette:"00ff00,ffff00"}, 'canlad_distr_type', false);

var fire_mask = distr_type.updateMask(distr_type.eq(1)).multiply(boreal_mask).multiply(0).add(1)
var harv_mask = distr_type.updateMask(distr_type.eq(2)).multiply(boreal_mask).multiply(0).add(1)

Map.addLayer(fire_mask, {palette:"ffff00"}, 'fire_mask', false);
Map.addLayer(harv_mask, {palette:"00ff00"}, 'harv_mask', false);

var area = ee.Image.pixelArea()
var fire_area = (distr_type.eq(1).multiply(area)).reduceRegion(ee.Reducer.sum(), boreal_geom, 90, null, null, false, 1e13);
var harv_area = (distr_type.eq(2).multiply(area)).reduceRegion(ee.Reducer.sum(), boreal_geom, 90, null, null, false, 1e13);

print('fire area: ', fire_area);
print('harv_area: ', harv_area);




var calc_scale = 90;
var version = 5;

//ecozones = ecozones.toList(ecozones.size())

var uncert_calc = function(img_old, img_new, uncert_old, uncert_new){
  return ee.Image(0.02)
           .multiply((ee.Image(img_old).toFloat()).multiply(ee.Image(uncert_new).toFloat())
                        .add((ee.Image(img_new)).toFloat().multiply(ee.Image(uncert_old).toFloat())))
           .divide((ee.Image(img_old).toFloat()).multiply(ee.Image(img_old).toFloat())).abs()
}

var change_calc = function(img_old, img_new){
  return ((ee.Image(img_new).toFloat()).subtract(ee.Image(img_old).toFloat())) //.divide(ee.Image(img_old).toFloat())
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

var top_fire_layer = top_fire_layer.updateMask(top_fire_layer.gt(0)).multiply(tc_mask_max).rename('top_fire_layer').toFloat();
Map.addLayer(top_fire_layer,{min:1900, max: 2018, palette:'A8FB9E,F4DD36,0B3D05'},'top_fire_layer', false);


var area_img = ee.Image.pixelArea().multiply(tc_mask_max);

var fire_mask = top_fire_layer.multiply(0).add(1);

//var decid_min = ee.ImageCollection([decid2000, decid2015]).reduce(ee.Reducer.min()); //decid2010,decid2005,
//var decid_mask = ee.Image(1).updateMask(decid_min.neq(0)); 

//var tc_mask0 = tc_mask
//var tc_mask = tc_mask.multiply(decid_mask)

decid2000 = decid2000.toFloat()
decid2005 = decid2005.toFloat()
decid2010 = decid2010.toFloat()
decid2015 = decid2015.toFloat()

tc2000 = tc2000.toFloat()
tc2005 = tc2005.toFloat()
tc2010 = tc2010.toFloat()
tc2015 = tc2015.toFloat()

var tc_diff = tc2015.subtract(tc2000).updateMask(tc_mask_max).multiply(land).multiply(0.01);
var tc_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5) * 0.5',{'a': tc2000u.toFloat().divide(4.0), 'b': tc2015u.toFloat().divide(4.0)}).updateMask(tc_mask_max).multiply(land).multiply(0.01);
//var tc_udiff = (ee.Image(tc2000u.toFloat()).add(ee.Image(tc2015u).toFloat())).divide(2.0).updateMask(tc_mask).multiply(land).multiply(0.01);

Map.addLayer(tc_diff,vis_tc_diff,'tc_diff',false);
Map.addLayer(tc_udiff,vis_tc_diff,'tc_udiff',false);

var decid_diff = ee.Image(decid2015).subtract(ee.Image(decid2000)).updateMask(tc_max.gt(25)).multiply(land).multiply(canada_ak).toFloat().multiply(0.01);
var decid_udiff = ee.Image().expression('((a**2 + b**2) ** 0.5) * 0.5',{'a': decid2000u.toFloat().divide(2.0), 'b': decid2015u.toFloat().divide(2.0)}).updateMask(tc_mask_max).multiply(land).clip(boreal_bounds).toFloat().multiply(0.01);

var decid_cdiff = ee.Image(decid2015.multiply(tc2015)).subtract(ee.Image(decid2000.multiply(tc2000))).updateMask(tc_max.gt(25)).multiply(land).multiply(canada_ak).toFloat().multiply(0.0001);
var evergrn_cdiff = tc_diff.subtract(decid_cdiff)


//var decid_udiff = (ee.Image(decid2000u.toFloat()).add(ee.Image(decid2015u).toFloat())).divide(2.0).updateMask(tc_mask).multiply(land).multiply(0.01);
//throw('stop')

Map.addLayer(decid_diff,vis_decid_diff,'decid_diff', false);
Map.addLayer(decid_cdiff,vis_decid_diff,'decid_cdiff', true);



//Map.addLayer(decid2000.multiply(tc2000.divide(100.0)).multiply(land),vis_decid,'decid_tc_2000', false);
//Map.addLayer(decid2005.multiply(tc2005.divide(100.0)).multiply(land),vis_decid,'decid_tc_2005', false);
//Map.addLayer(decid2010.multiply(tc2010.divide(100.0)).multiply(land),vis_decid,'decid_tc_2010', false);
//Map.addLayer(decid2015.multiply(tc2015.divide(100.0)).multiply(land),vis_decid,'decid_tc_2015', false);

Map.addLayer(decid2000.multiply(land),vis_decid,'decid2000', false);
//Map.addLayer(decid2000u.multiply(land),{min:0, max:50, palette:'286F09,ECC519'},'decid2000u', false);

Map.addLayer(decid2005.multiply(land),vis_decid,'decid2005', false);
Map.addLayer(decid2010.multiply(land),vis_decid,'decid2010', false);
Map.addLayer(decid2015.multiply(land),vis_decid,'decid2015', false);

//Map.addLayer(tc2000,vis_tc,'tc2000', false);
//Map.addLayer(tc2000u,vis_tc,'tc2000u', false);
//Map.addLayer(tc2005,vis_tc,'tc2005', false);
//Map.addLayer(tc2010,vis_tc,'tc2010', false);
//Map.addLayer(tc2015,vis_tc,'tc2015', false);
//Map.addLayer(tc2015u,vis_tc,'tc2015u', false);


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


var fall_diff = change_calc(alb_fal2000, alb_fal2015).updateMask(tc_mask_max).multiply(land);
var fall_udiff = uncert_calc(alb_fal2000, alb_fal2015, alb_fall2000_uncert, alb_fall2015_uncert).updateMask(tc_mask_max);
//Map.addLayer(fall_diff, {min:-.5, max:.5, palette: 'B62809,FFC560,1178C8'}, 'fall_alb_diff', true);
//Map.addLayer(fall_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'fall_alb_udiff', true);

var sum_diff = change_calc(alb_sum2000, alb_sum2015).updateMask(tc_mask_max).multiply(land);
var sum_udiff = uncert_calc(alb_sum2000, alb_sum2015, alb_fall2000_uncert, alb_fall2015_uncert).updateMask(tc_mask_max);
//Map.addLayer(sum_diff, {min:-.25, max:.25, palette: 'B62809,FFC560,1178C8'}, 'summer_alb_diff', true);
//Map.addLayer(sum_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'summer_alb_udiff', true);

var spr_diff = change_calc(alb_spr2000, alb_spr2015).updateMask(tc_mask_max).multiply(land);
var spr_udiff = uncert_calc(alb_spr2000, alb_spr2015, alb_spr2015_uncert, alb_spr2015_uncert).updateMask(tc_mask_max);
//Map.addLayer(spr_diff, {min:-.5, max:.5, palette: 'B62809,FFC560,1178C8'}, 'spring_alb_diff', true);
//Map.addLayer(spr_udiff, {min:-.05, max:.05, palette: 'B62809,FFC560,1178C8'}, 'spring_alb_udiff', true);


var spr_kernel = ee.ImageCollection([cam5_apr, cam5_may]).reduce(ee.Reducer.mean()).toFloat();
var sum_kernel = ee.ImageCollection([cam5_jun, cam5_jul, cam5_aug]).reduce(ee.Reducer.mean()).toFloat();
var fall_kernel = ee.ImageCollection([cam5_sep, cam5_oct]).reduce(ee.Reducer.mean()).toFloat();


var sum_forc = sum_kernel.multiply(sum_diff);
var spr_forc = spr_kernel.multiply(spr_diff);
var fall_forc = fall_kernel.multiply(fall_diff);

//Map.addLayer(sum_forc,{min:-.25, max:.25, palette:'B62809,FFC560,1178C8'},'sum');
//Map.addLayer(spr_forc,{min:-5, max:5, palette:'B62809,FFC560,1178C8'},'spr');
//Map.addLayer(fall_forc,{min:-2.5, max:2.5, palette:'B62809,FFC560,1178C8'},'fall');


var sum_uforc = sum_kernel.multiply(sum_udiff).abs()
var spr_uforc = spr_kernel.multiply(spr_udiff).abs();
var fall_uforc = fall_kernel.multiply(fall_udiff).abs();

//Map.addLayer(sum_uforc,{min:-.1, max:.1, palette:'B62809,FFC560,1178C8'},'sum_u');
//Map.addLayer(spr_uforc,{min:-1, max:1, palette:'B62809,FFC560,1178C8'},'spr_u');
//Map.addLayer(fall_uforc,{min:-.25, max:.25, palette:'B62809,FFC560,1178C8'},'fall_u');



//Map.addLayer(fire_mask, {palette:'1AFFFF'}, 'fire_mask')
//Map.addLayer(tc_mask, {palette:'FFAAFF'}, 'tc_mask')


// values ---------------------------------------------------------------------------------------------------------------------
var ulim = 0.1;
var llim = -0.1;

// mean increase in decid frac (rel abundance)
var decid_diff_pos = decid_diff.updateMask(decid_diff.gt(ulim)).unmask(0.0).multiply(area_img)
var decid_udiff_pos = decid_udiff.updateMask(decid_diff.gt(ulim)).unmask(0.0).multiply(area_img)
var decid_diff_pos_area = area_img.updateMask(decid_diff.gt(ulim)).unmask(0.0)
var decid_cdiff_pos_area = area_img.updateMask(decid_cdiff.gt(0.0)).unmask(0.0)

// mean decrease in decid frac (rel abundance)
var decid_diff_neg = decid_diff.updateMask(decid_diff.lte(llim)).unmask(0.0).multiply(area_img)
var decid_udiff_neg = decid_udiff.updateMask(decid_diff.lte(llim)).unmask(0.0).multiply(area_img)
var decid_diff_neg_area = area_img.updateMask(decid_diff.lte(llim)).unmask(0.0)
var decid_cdiff_neg_area = area_img.updateMask(decid_cdiff.lte(0.0)).unmask(0.0)


var decid_diff_neg = decid_diff.updateMask(decid_diff.lte(llim)).unmask(0.0).multiply(area_img)
var decid_udiff_neg = decid_udiff.updateMask(decid_diff.lte(llim)).unmask(0.0).multiply(area_img)
var decid_diff_neg_area = area_img.updateMask(decid_diff.lte(llim)).unmask(0.0)
var decid_cdiff_neg_area = area_img.updateMask(decid_cdiff.lte(0.0)).unmask(0.0)


// mean increase in tree canopy
var tc_diff_pos = tc_diff.updateMask(tc_diff.gt(0.0)).unmask(0.0).multiply(area_img)
var tc_udiff_pos = tc_udiff.updateMask(tc_diff.gt(0.0)).unmask(0.0).multiply(area_img)
var tc_diff_pos_area = area_img.updateMask(tc_diff.gt(0.0)).unmask(0.0)

// mean decrease in tree canopy
var tc_diff_neg = tc_diff.updateMask(tc_diff.lte(0.0)).unmask(0.0).multiply(area_img)
var tc_udiff_neg = tc_udiff.updateMask(tc_diff.lte(0.0)).unmask(0.0).multiply(area_img)
var tc_diff_neg_area = area_img.updateMask(tc_diff.lte(0.0)).unmask(0.0)



var spr_pos_mask = spr_forc.gt(0.0)
var spr_neg_mask = spr_forc.lte(0.0)

var spr_pforc = spr_forc.updateMask(spr_pos_mask).unmask(0.0).multiply(area_img)
var spr_nforc = spr_forc.updateMask(spr_neg_mask).unmask(0.0).multiply(area_img)

var spr_upforc = spr_uforc.updateMask(spr_pos_mask).unmask(0.0).multiply(area_img)
var spr_unforc = spr_uforc.updateMask(spr_neg_mask).unmask(0.0).multiply(area_img)


var sum_pos_mask = sum_forc.gt(0.0)
var sum_neg_mask = sum_forc.lte(0.0)

var sum_pforc = sum_forc.updateMask(sum_pos_mask).unmask(0.0).multiply(area_img)
var sum_nforc = sum_forc.updateMask(sum_neg_mask).unmask(0.0).multiply(area_img)

var sum_upforc = sum_uforc.updateMask(sum_pos_mask).unmask(0.0).multiply(area_img)
var sum_unforc = sum_uforc.updateMask(sum_neg_mask).unmask(0.0).multiply(area_img)


var fall_pos_mask = fall_forc.gt(0.0)
var fall_neg_mask = fall_forc.lte(0.0)

var fall_pforc = fall_forc.updateMask(fall_pos_mask).unmask(0.0).multiply(area_img)
var fall_nforc = fall_forc.updateMask(fall_neg_mask).unmask(0.0).multiply(area_img)

var fall_upforc = fall_uforc.updateMask(fall_pos_mask).unmask(0.0).multiply(area_img)
var fall_unforc = fall_uforc.updateMask(fall_neg_mask).unmask(0.0).multiply(area_img)


Map.addLayer(spr_pforc,{min:-2.5, max:2.5, palette:'B62809,FFC560,1178C8'},'spr_pforc');
Map.addLayer(spr_nforc,{min:-5, max:5, palette:'B62809,FFC560,1178C8'},'spr_nforc');
//Map.addLayer(fall_forc,{min:-2.5, max:2.5, palette:'B62809,FFC560,1178C8'},'fall');


var data_img = (decid_diff_pos.addBands(decid_udiff_pos)
                              .addBands(decid_diff_pos_area)
                              .addBands(decid_cdiff_pos_area)
                              .addBands(decid_diff_neg)
                              .addBands(decid_udiff_neg)
                              .addBands(decid_diff_neg_area)
                              .addBands(decid_cdiff_neg_area)
                              .addBands(tc_diff_pos)
                              .addBands(tc_udiff_pos)
                              .addBands(tc_diff_pos_area)
                              .addBands(tc_diff_neg)
                              .addBands(tc_udiff_neg)
                              .addBands(tc_diff_neg_area))
                              .addBands(spr_pforc)
                              .addBands(spr_upforc)
                              .addBands(spr_nforc)
                              .addBands(spr_unforc)
                              .addBands(sum_pforc)
                              .addBands(sum_upforc)
                              .addBands(sum_nforc)
                              .addBands(sum_unforc)
                              .addBands(fall_pforc)
                              .addBands(fall_upforc)
                              .addBands(fall_nforc)
                              .addBands(fall_unforc)
                              .addBands(area_img)

                              .rename(['decid_diff_pos',
                                       'decid_udiff_pos',
                                       'decid_diff_pos_area',
                                       'decid_cdiff_pos_area',
                                       'decid_diff_neg',
                                       'decid_udiff_neg',
                                       'decid_diff_neg_area',
                                       'decid_cdiff_neg_area',
                                       'tc_diff_pos',
                                       'tc_udiff_pos',
                                       'tc_diff_pos_area',
                                       'tc_diff_neg',
                                       'tc_udiff_neg',
                                       'tc_diff_neg_area',
                                       'spr_pforc',
                                       'spr_upforc',
                                       'spr_nforc',
                                       'spr_unforc',
                                       'sum_pforc',
                                       'sum_upforc',
                                       'sum_nforc',
                                       'sum_unforc',
                                       'fall_pforc',
                                       'fall_upforc',
                                       'fall_nforc',
                                       'fall_unforc',
                                       'area'
                                        ]).multiply(land)

print(ecozones)
print(data_img)

var data_coll_rec = (data_img.multiply(recent_fire_mask)).reduceRegions(ecozones, ee.Reducer.sum(), calc_scale).map(function(elem){return elem.setGeometry(null)})
var data_coll_intr = (data_img.multiply(interm_fire_mask)).reduceRegions(ecozones, ee.Reducer.sum(), calc_scale).map(function(elem){return elem.setGeometry(null)})
var data_coll_old = (data_img.multiply(old_fire_mask)).reduceRegions(ecozones, ee.Reducer.sum(), calc_scale).map(function(elem){return elem.setGeometry(null)})

var data_coll_all = data_img.reduceRegions(ecozones, ee.Reducer.sum(), calc_scale).map(function(elem){return elem.setGeometry(null)})

var data_coll_fire = (data_img.updateMask(fire_mask)).reduceRegions(ecozones, ee.Reducer.sum(), calc_scale).map(function(elem){return elem.setGeometry(null)})
var data_coll_harv = (data_img.updateMask(harv_mask)).reduceRegions(ecozones, ee.Reducer.sum(), calc_scale).map(function(elem){return elem.setGeometry(null)})

//Map.addLayer(data_img)
Map.addLayer(ecozones)
//Map.addLayer(recent_fire_mask)
//Map.addLayer(interm_fire_mask)
//Map.addLayer(old_fire_mask)

Export.table.toDrive({
  collection:data_coll_rec,
  fileNamePrefix:'ecozones_area_summary_rec_2000_2015_v' + version+ '_'+calc_scale,
  description:'ecozones_area_summary_rec_v' + version+ '_'+calc_scale,
  folder:'ecozones_area_summary_v' + version
});

Export.table.toDrive({
  collection:data_coll_intr,
  fileNamePrefix:'ecozones_area_summary_intr_2000_2015_v' + version+ '_'+calc_scale,
  description:'ecozones_area_summary_intr_v' + version+ '_'+calc_scale,
  folder:'ecozones_area_summary_v' + version
});

Export.table.toDrive({
  collection:data_coll_old,
  fileNamePrefix:'ecozones_area_summary_old_2000_2015_v' + version+ '_'+calc_scale,
  description:'ecozones_area_summary_old_v' + version+ '_'+calc_scale,
  folder:'ecozones_area_summary_v' + version
});


Export.table.toDrive({
  collection:data_coll_all,
  fileNamePrefix:'ecozones_area_summary_all_2000_2015_v' + version+ '_'+calc_scale,
  description:'ecozones_area_summary_all_v' + version+ '_'+calc_scale,
  folder:'ecozones_area_summary_v' + version
});


Export.table.toDrive({
  collection:data_coll_fire,
  fileNamePrefix:'ecozones_area_summary_fire_2000_2015_v' + version+ '_'+calc_scale,
  description:'ecozones_area_summary_fire_v' + version+ '_'+calc_scale,
  folder:'ecozones_area_summary_v' + version
});

Export.table.toDrive({
  collection:data_coll_harv,
  fileNamePrefix:'ecozones_area_summary_harv_2000_2015_v' + version+ '_'+calc_scale,
  description:'ecozones_area_summary_harv_v' + version+ '_'+calc_scale,
  folder:'ecozones_area_summary_v' + version
});

//Export.image.toDrive({
//  image:decid_diff,
//  region:geometry,
//  scale: 250,
//  maxPixels: 1e13,
//  fileNamePrefix:'decid_change_2000_2015',
//  folder: 'decid_change_2000_2015',
//  description: 'decid_change_2000_2015'
//})
//Map.addLayer(decid_diff, vis_decid_diff, 'decid_diff')
//
//Map.addLayer(land)
//Map.addLayer(canada_ak)
//Map.addLayer(usa)
//
//var canada_ak = ee.ImageCollection([usa.clip(geometry2), canada]).mosaic()
//
//Map.addLayer(canada_ak)
//Export.image.toAsset({
//  image:canada_ak,
//  region:geometry3,
//  scale: 30,
//  maxPixels: 1e13,
//  assetId:'users/masseyr44/decid/canada_ak',
//  description: 'canada_ak'
//})

