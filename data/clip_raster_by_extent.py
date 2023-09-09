from geosoup import Raster, Handler, Opt
from sys import argv

"""
Script to clip raster .tif files in a folder to a set of extent coordinates
in the format: xmin, ymin, xmax, ymax
"""

if __name__ == '__main__':

    script, in_file, out_file, xmin, ymin, xmax, ymax = argv

    Handler(out_file).file_delete()

    xmin = float(xmin)
    ymin = float(ymin)
    xmax = float(xmax)
    ymax = float(ymax)

    Opt.cprint('Filename {}'.format(in_file))

    ras = Raster(in_file)
    ras.initialize()

    ras.clip_by_extent(xmin, ymin, xmax, ymax, outfile=out_file, verbose=True)
