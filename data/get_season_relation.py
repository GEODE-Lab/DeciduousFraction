from modules import *
import numpy as np
from sys import argv

if __name__ == '__main__':

    script, file_dir, out_dir = argv

    # file_dir = 'c:/temp/check/'
    # out_dir = 'c:/temp/check/'

    tc_cutoff = 25
    filler_val = -32567

    filelist = Handler(dirname=file_dir).find_all(pattern='.tif')

    band_list = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']

    outfiles = list(out_dir + band + '.csv' for band in band_list)

    for filename in filelist:

        print('Processing : {}'.format(Handler(filename).basename))

        # outfile = out_dir + Handler(filename).basename.split('.tif')[0] + '.csv'

        raster_name = Handler(filename).basename
        raster = Raster(filename)
        raster.initialize(get_array=False)

        bandnames = list()

        for ii in (1, 2, 3):
            bandnames += list(band + '_' + str(ii) for band in band_list)
        bandnames += ['b1']

        band_locs = tuple((Sublist(raster.bnames) == band) + 1 for band in bandnames)

        val_list = list()

        for tie_pt, tile_arr in raster.get_next_tile(bands=band_locs):

            tile_shape = tile_arr.shape

            vals = np.where(tile_arr[-1, :, :] >= tc_cutoff, tile_arr, filler_val)
            vals = vals.reshape(tile_shape[0], tile_shape[1] * tile_shape[2]).T
            vals = vals[np.where(vals[:, 0] != filler_val)].tolist()

            val_dicts = list(dict(zip(bandnames, val)) for val in vals)

            for outfile in outfiles:

                bandname = Handler(outfile).basename.split('.csv')[0]

                bands = list(bandname + '_{}'.format(str(jj)) for jj in (1, 2, 3))

                out_list = list()

                for val_dict in val_dicts:
                    out_dict = dict()
                    for band in bands:
                        out_dict[band] = val_dict[band]
                    out_list.append(out_dict)

                if Handler(outfile).file_exists():
                    Handler.write_to_csv(out_list, outfile, append=True)
                else:
                    Handler.write_to_csv(out_list, outfile, append=False)
