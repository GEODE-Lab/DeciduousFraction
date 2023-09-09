from modules import *


if __name__ == '__main__':


    folder = 'd:/temp/'
    filelist = ['new_decid_diff_2000_2015v2_25_land.tif'
                ]

    out_proj4 = '+proj=aea +lat_1=50 +lat_2=70 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs'

    for infile in filelist:

        ras = Raster(folder + infile)
        ras.initialize()

        print(ras)

        outfile = folder + Handler(infile).add_to_filename('_albers')

        ras.reproject(outfile=outfile,
                      out_proj4=out_proj4,
                      verbose=True,
                      resampling='bilinear',
                      output_res=(250, 250),
                      out_nodatavalue=None,
                      bigtiff='yes',
                      compress='lzw')

        Raster(outfile).add_overviews(bigtiff='yes',
                                      compress='lzw')
        '''
        Raster(outfile).clip("D:/Shared/Dropbox/projects/NAU/" +
                             "landsat_deciduous/data/STUDY_AREA/canada_ak_combined_albers.shp",
                             bigtiff='yes',
                             compress='lzw')
        '''
        




