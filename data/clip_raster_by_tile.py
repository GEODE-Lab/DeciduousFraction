from geosoup import Raster, Handler, Opt
import numpy as np
from sys import argv

"""
Script to clip raster .tif files in a folder to a set of bound coordinates
in the format: tile_x, tile_y, n_cols, n_rows
"""

if __name__ == '__main__':

    script, in_folder, out_folder, tile_x, tile_y, n_cols, n_rows = argv

    tile_x = int(tile_x)
    tile_y = int(tile_y)
    n_cols = int(n_cols)
    n_rows = int(n_rows)

    file_list = Handler(dirname=in_folder).find_all(pattern='.tif')

    Opt.cprint('Found {} files!\n'.format(str(len(file_list))))

    for indx, file_name in enumerate(file_list):
        ras = Raster(file_name)

        Opt.cprint('{} of {}: Getting tile with bounds {} : {}'.format(str(indx + 1),
                                                                       str(len(file_list)),
                                                                       str(','.join([str(elem) for
                                                                                     elem in
                                                                                     (tile_x, tile_y,
                                                                                      n_cols, n_rows)])),
                                                                       file_name))

        out_file = out_folder + Handler().sep + Handler(file_name).basename

        tile_arr = ras.get_tile(block_coords=(tile_x, tile_y, n_cols, n_rows))
        tile_arr = tile_arr[np.newaxis, :, :]

        out_ras = Raster(out_file,
                         array=tile_arr,
                         dtype=ras.dtype,
                         shape=tile_arr.shape,
                         crs_string=ras.crs_string)

        out_ras.transform = (ras.transform[0] + ras.transform[1] * tile_x,
                             ras.transform[1],
                             0,
                             ras.transform[3] + ras.transform[5] * tile_y,
                             0,
                             ras.transform[5])

        out_ras.bnames = ['band_1']
        out_ras.nodatavalue = ras.nodatavalue
        out_ras.write_to_file(compress='lzw')

    Opt.cprint('\nCompleted!')
