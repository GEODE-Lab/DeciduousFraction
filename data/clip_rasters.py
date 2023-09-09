from geosoup import Raster, Handler, Opt
from sys import argv


"""
Script to clip raster .tif files in a folder to a boundary using
a single polygon shapefile
"""


if __name__ == '__main__':

    script, in_folder, out_folder, cut_file = argv

    file_list = Handler(dirname=in_folder).find_all(pattern='.tif')

    Opt.cprint('Found {} files!\n'.format(str(len(file_list))))

    for indx, file_name in enumerate(file_list):
        Opt.cprint('{} of {}: Sub-setting: {}'.format(str(indx + 1),
                                                      str(len(file_list)),
                                                      file_name))
        out_file = out_folder + Handler().sep + Handler(file_name).basename
        ras = Raster(file_name)
        ras.clip(cutline_file=cut_file,
                 outfile=out_file,
                 compress='lzw')

    Opt.cprint('\nCompleted!')
