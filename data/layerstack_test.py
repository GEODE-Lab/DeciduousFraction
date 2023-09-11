from geosoup import *

if __name__ == '__main__':

    indir = 'c:/temp/albedo'

    files = Handler(dirname=indir).find_all('*.tif')

    mraster = MultiRaster(filelist=files).composite()

    print(mraster)


    out_ls = mraster.layerstack(verbose=True, return_vrt=False)



