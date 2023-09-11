if __name__ == '__main__':
    import sys
    import os
    from geosoup import *

    script, filename, cutfile, outfolder = sys.argv

    # epsg = 3571
    out_proj4 = '+proj=laea +lat_0=90 +lon_0=180 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs '

    tempfile = outfolder + Handler(Handler(filename.replace('EPSG-4326', ''))
                                   .add_to_filename('_NPLAEA')).basename
    outfile = outfolder + Handler(Handler(filename.replace('EPSG-4326', ''))
                                  .add_to_filename('_NPLAEA_clipped')).basename

    ras = Raster(filename)
    ras.initialize()

    print(ras)

    ras.reproject(outfile=tempfile,
                  out_proj4=out_proj4,
                  output_res=(100, 100),
                  out_nodatavalue=0.0,
                  bigtiff='yes',
                  compress='lzw')

    temp_ras = Raster(tempfile)
    temp_ras.clip(cutline_file=cutfile,
                  outfile=outfile)

    Handler(tempfile).file_delete()

    Raster(outfile).add_overviews(bigtiff='yes',
                                  compress='lzw')


