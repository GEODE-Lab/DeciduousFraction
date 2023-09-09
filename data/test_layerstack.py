from geosoup import Raster, MultiRaster, Opt, Handler
import numpy as np


MIN_QA_PIXELS = 1
TILE_SIZE = (1440, 1440)
IMAGE_BOUNDS = (-179.999, -50.0, 30.0, 75.0)  # x min, x max, y min, y max
VALID_QA = [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23]
VALID_QA2 = list(range(0, 64))


if __name__ == '__main__':

    infolder = 'D:/temp/albedo/geographic_clip/'
    outdir = 'D:/temp/albedo/geo_out/'
    outfile = 'D:/temp/albedo/geo_out/lraster_test.tif'

    ver = 2
    startyear = 2000
    endyear = 2002
    startdate = 150
    enddate = 240

    startyear = int(startyear)
    endyear = int(endyear)
    startdate = int(startdate)
    enddate = int(enddate)

    # find albedo files
    albedo_files = Handler(dirname=infolder).find_all('*_albedo.tif')

    # list of quality files
    quality_files = [elem.replace('_albedo.tif', '_quality.tif') for elem in albedo_files]

    # list of date and year
    num_list = np.array(list(list(int(elem_) for elem_
                                  in Handler(elem).basename
                                  .replace('_albedo.tif', '')
                                  .replace('bluesky_albedo_', '')
                                  .split('_'))
                             for elem in albedo_files))

    Opt.cprint((startdate, enddate))
    Opt.cprint((startyear, endyear))
    Opt.cprint(len(albedo_files))

    # sort files by date and year to composite
    file_loc_on_list = np.where((num_list[:, 0] >= startyear) & (num_list[:, 0] <= endyear) &
                                (num_list[:, 1] >= startdate) & (num_list[:, 1] <= enddate))[0]

    # make list of files
    filelist = list(albedo_files[i] for i in file_loc_on_list.tolist())

    lraster = MultiRaster(filelist=filelist)

    Opt.cprint(lraster)

    # layer stack VRTs
    ls_vrt = lraster.layerstack(return_vrt=True, outfile=outfile)

    lras = Raster('alb_layerstack')
    lras.datasource = ls_vrt
    lras.initialize()

    Opt.cprint(lras)

