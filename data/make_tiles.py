from sys import argv
from modules import *

"""
This script makes tiles of given size tile_size_x, tile_size_y
from the given raster file. The tiles are stored in GeoTiff
format with inherited attributes from the parent raster.
"""

# main program
if __name__ == '__main__':

    # import filename from file arguments
    script, filename, outdir, tile_size_x, tile_size_y = argv

    # query for metadata
    raster_obj = Raster.initialize(filename)

    bands, rows, cols = raster_obj.shape
    proj = raster_obj.crs_string

    # make tiles
    try:
        raster_obj.make_tiles(int(tile_size_x), int(tile_size_y), outdir)
    except AttributeError:
        print('Initialize the raster using Raster.initialize() or ' +
              'get metadata using Raster.get_raster_metadict()')
    except ValueError:
        print('Tile size should be smaller than original raster {}x{}.'.format(rows, cols))

