from modules import *
import numpy as np


if __name__ == '__main__':

    folder = 'c:/temp/'
    version = 2
    outfile = folder + 'forc_summ_v{}.csv'.format(str(version))

    filelist = ['decid_diff_incl_east_2000_2015_albers.tif',
                'decid_diff_2000_2015_albers.tif',
                'tc_diff_2000_2015_albers.tif',
                'spr_forc_2000_2015_albers.tif',
                'sum_forc_2000_2015_albers.tif',
                'fall_forc_2000_2015_albers.tif',
                ]

    layer_list = ['decid_e', 'decid', 'tc', 'spr', 'sum', 'fall']

    forc_list = list()

    for i, infile in enumerate(filelist):

        ras = Raster(folder + infile)
        ras.initialize(get_array=True)

        print(ras)

        pos_avg = np.average(ras.array[np.where(ras.array > 0.0)])
        pos_sd = np.std(ras.array[np.where(ras.array > 0.0)])

        neg_avg = np.average(ras.array[np.where(ras.array < 0.0)])
        neg_sd = np.std(ras.array[np.where(ras.array < 0.0)])

        avg = np.average(ras.array[np.where(ras.array != 0.0)])
        avg_sd = np.std(ras.array[np.where(ras.array != 0.0)])

        forc_dict = {'file': infile,
                     'layer': layer_list[i],
                     'pos': pos_avg,
                     'pos_sd': pos_sd,
                     'neg': neg_avg,
                     'neg_sd': neg_sd,
                     'avg': avg,
                     'avg_sd': avg_sd}

        print(forc_dict)

        forc_list.append(forc_dict)

    Handler.write_to_csv(forc_list, outfile)


