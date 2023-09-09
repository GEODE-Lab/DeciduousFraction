from geosoup import Handler, Raster, Opt
from sys import argv


if __name__ == '__main__':
    '''
    script, infile, outfolder, year, band = argv

    '''
    infile = "C:/temp/Boreal_NA_pctl50_95_50_SR_NDVI_zone2_2010-0000055552-0000023808.tif"

    outfolder = "C:/temp/"

    band = 'ndvi_3'

    ras = Raster(infile)
    ras.initialize()

    rasname = outfolder + Handler(Handler(infile).basename).add_to_filename(band)

    Opt.cprint('{} --> {}'.format(infile, rasname))
    ras.get_bands(band, outfile=rasname, return_raster=False)

    '''    
    xmin = -58.9974851
    ymin = 53.2052380

    xmax = xmin + 0.25
    ymax = ymin + 0.25

    ras.clip_by_extent(xmin, ymin, xmax, ymax,
                       outfile=infile.replace('.tif', '_clip2.tif'))
    '''

