from geosoup import MultiRaster, Handler, Raster, Opt
from sys import argv


if __name__ == '__main__':

    script, infolder, outfolder, outfile, year, band = argv

    filelist = Handler(dirname=infolder).find_all(pattern='*{}*.tif'.format(str(year)))

    raslist = []

    for filename in filelist:
        ras = Raster(filename)
        ras.initialize()

        rasname = outfolder + Handler(Handler(filename).basename).add_to_filename(band)
        ras.get_bands(band,
                      outfile=rasname,
                      return_raster=False)

        raslist.append(rasname)

        Opt.cprint('{} --> {}'.format(filename, rasname))

    Opt.cprint('Mosaicking {} files'.format(str(len(raslist))))
    mras = MultiRaster(filelist=raslist)

    Opt.cprint(mras)

    mras.mosaic(outfile=outfile,
                compress='lzw',
                bigtiff='yes',
                add_overviews=True,
                verbose=True)

    for rasfile in raslist:
        Handler(rasfile).file_delete()

    Opt.cprint('Outfile: {}'.format(outfile))
