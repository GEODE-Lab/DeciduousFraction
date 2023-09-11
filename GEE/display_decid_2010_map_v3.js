/**** Start of imports. If edited, may not auto-convert in the playground. ****/
var decid = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis"),
    tc2010 = ee.Image("users/masseyr44/decid/hansen_tc_2010_mosaic_vis"),
    bounds = ee.FeatureCollection("users/masseyr44/decid/NAboreal_10kmbuffer"),
    check = ee.Image("users/masseyr44/ak_decid_2010_pred"),
    bounds2 = ee.FeatureCollection("users/masseyr44/decid/NABoreal_boreal_10km_buffer"),
    geometry2 = /* color: #98ff00 */ee.Geometry.Point([-109.5931434629947, 57.24449344118846]),
    uncert = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_uncertainty_vis"),
    ak2015 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2015_prediction_vis_ak"),
    ak2010 = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis_ak"),
    uncert_ = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_uncertainty_vis_v2_byte"),
    decid_ = ee.Image("users/masseyr44/decid/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis_v2_byte"),
    decid__ = ee.Image("users/masseyr44/decid/decid_mosaic_2010_prediction_vis_nd_2"),
    geometry = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-179.65112859142755, 53.18238935207438],
          [-179.60718327892755, 51.21657286299374],
          [-177.54175359142755, 50.59305672204701],
          [-170.13696843517755, 50.70451467770589],
          [-158.35962468517755, 52.87846543151919],
          [-153.61353093517755, 55.97015787836148],
          [-150.0319879664275, 59.00123579397527],
          [-139.0896051539275, 58.19993318795768],
          [-136.4968317164275, 55.89408580631578],
          [-135.0686090601775, 53.41638793737198],
          [-132.4978082789275, 48.480546664624896],
          [-130.6740778101775, 42.05530968528491],
          [-124.2580621851775, 41.49819038032717],
          [-123.1154840601775, 41.48173128305638],
          [-121.3356989039275, 41.49819038032717],
          [-119.7316949976775, 41.48173128305638],
          [-116.7214410914275, 41.49819038032717],
          [-113.8430231226775, 41.51464529583106],
          [-111.0524957789275, 41.48173128305638],
          [-108.1081598414275, 41.465268004314524],
          [-104.7463434351775, 41.465268004314524],
          [-100.8132379664275, 41.41585308224267],
          [-96.9460504664275, 41.41585308224267],
          [-93.1228082789275, 41.41585308224267],
          [-87.4318903101775, 41.37201082020265],
          [-81.5871637476775, 41.42145909838983],
          [-75.5007379664275, 41.43793349743767],
          [-68.1618707789275, 41.37201082020265],
          [-66.0744684351775, 41.962905293616465],
          [-55.94507390392755, 44.63284162693686],
          [-50.97925359142755, 47.40889361171501],
          [-53.15454656017755, 52.77231787824733],
          [-57.41724187267755, 56.276411392430056],
          [-58.62573796642755, 57.108913203639446],
          [-65.0417535914275, 61.17194996519546],
          [-69.9416559351775, 62.27517131136313],
          [-71.3039606226775, 62.45861037360572],
          [-73.9187067164275, 62.76185719837153],
          [-78.2473199976775, 62.74173701236693],
          [-80.5105035914275, 59.686699381762594],
          [-84.9489801539275, 59.18391011924436],
          [-88.4426324976775, 60.33465927964565],
          [-90.0905817164275, 61.65555986080588],
          [-94.6389215601775, 64.76203328103126],
          [-98.5939996851775, 66.11347874390776],
          [-101.8679254664275, 67.073502958468],
          [-105.6691949976775, 68.00517661905205],
          [-108.8332574976775, 68.63022119213598],
          [-111.1623590601775, 68.35634111740568],
          [-111.8215387476775, 68.43723921252789],
          [-113.3376520289275, 68.4210826623827],
          [-113.4475153101775, 68.60618875991364],
          [-113.9968317164275, 68.9560951583841],
          [-114.9196832789275, 69.08981800940532],
          [-116.7214410914275, 69.36257793590788],
          [-120.4567926539275, 70.1605758618875],
          [-124.3239801539275, 70.42729828589086],
          [-127.2902887476775, 70.62507582971794],
          [-128.1911676539275, 70.74861509845252],
          [-131.6848199976775, 71.00057831898224],
          [-137.1120660914275, 71.26348515854242],
          [-140.7595270289275, 71.41814190563288],
          [-145.4397028101775, 71.48105502648004],
          [-148.2302301539275, 71.60626518074305],
          [-152.55884343517755, 71.64090049891819],
          [-158.75513249767755, 71.43913582294941],
          [-159.54614812267755, 71.28464757248113],
          [-164.05054265392755, 70.18293534619471],
          [-166.51341313419334, 69.04319371544138],
          [-167.74388188419334, 67.74916636746077],
          [-168.00755375919334, 66.4849593990686],
          [-168.88646000919334, 64.74386093703552],
          [-171.96263188419334, 63.751114568285566],
          [-177.23606938419334, 60.160861413814224],
          [-179.87278813419334, 58.68573190787208]]]);
/***** End of imports. If edited, may not auto-convert in the playground. *****/



// Display a grid of linked maps, each with a different visualization. 
var image = [decid_.clip(geometry), decid__];

var NAMES = ['Deciduous Fraction','Uncertainty'];
var titlename = ['Decid frac','Uncertainty']
  
//Legend for continuous scale
var vis1 = {min:0, max:100, palette:['065D18','FFD905']};
var vis2 = {min:0, max:50, palette:['1153AE','FE7932']};

var VIS_PARAMS = [vis1, vis1];

function makeLegend(vis, index) {
  var lon = ee.Image.pixelLonLat().select('latitude');
  var gradient = lon.multiply((vis.max-vis.min)/100.0).add(vis.min);
  var legendImage = gradient.visualize(vis);



  // Otherwise, add it to a panel and add the panel to the map.
  var thumb = ui.Thumbnail({
    image: legendImage, 
    params: {bbox:'0,0,8,100', dimensions:'50x150'},  
    style: {padding: '0 0 0 0', position: 'bottom-left'}
  });
  

  // Create and add the legend title.
  var legendTitle = ui.Label({
    value: titlename[index],
    style: {
      fontWeight: 'bold',
      fontSize: '14px',
      margin: '0 0 0 0',
      padding: '0 0 0 0'
    }
  });
  
  var lp = ui.Panel({
    widgets: [legendTitle,thumb],
    layout: ui.Panel.Layout.Flow('vertical')
  }); 
  
  //print(lp)
  var rp = ui.Panel({
    widgets: [
      ui.Label(),
      ui.Label(vis['max']), 
      ui.Label({style: {stretch: 'vertical'}}), 
      ui.Label(vis['min'])
    ],
    layout: ui.Panel.Layout.Flow('vertical'),
    style: {stretch: 'vertical',fontWeight: 'bold',
      fontSize: '14px',
      margin: '0 0 0 0',
      padding: '0'}
  });
  //print(rp)
  
  return ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '10 5 0 0'
  },
  layout: ui.Panel.Layout.Flow('horizontal')
  }).add(lp).add(rp)

}

// Create a map for each visualization option.
var maps = [];
NAMES.forEach(function(name, index) {
  var map = ui.Map();
  map.add(ui.Label({value:name, style:{fontWeight: 'bold', fontSize: '14px'}}))
  map.addLayer(image[index], VIS_PARAMS[index], name);
  map.setOptions({mapTypeId:'HYBRID'})
  map.setControlVisibility({layerList:true, mapTypeControl:false, scaleControl: true, zoomControl: false, fullscreenControl:false });
  maps.push(map);
});
maps[0].add(makeLegend(vis1,0));
maps[1].add(makeLegend(vis2,1))

//maps[0].addLayer(ak2010, {min:0, max:1, palette:['065D18','FFD905']},'ak2010' )
//maps[0].addLayer(ak2015, {min:0, max:1, palette:['065D18','FFD905']},'ak2015' )
var linker = ui.Map.Linker(maps);

// Create a title.
var title = ui.Label('2010 Deciduous Mapping analysis', {
  stretch: 'horizontal',
  textAlign: 'center',
  fontWeight: 'bold',
  fontSize: '24px'
});

// Create a grid of maps.
var mapGrid = ui.Panel([
    ui.Panel([maps[0]], null, {stretch: 'both'}),
    ui.Panel([maps[1]], null, {stretch: 'both'}),

  ],
  ui.Panel.Layout.Flow('horizontal'), {stretch: 'both'}
);

// Add the maps and title to the ui.root.
ui.root.widgets().reset([title, mapGrid]);
ui.root.setLayout(ui.Panel.Layout.Flow('vertical'));


maps[0].centerObject(decid,5);
