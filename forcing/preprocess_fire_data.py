import sys
import os

from geosoup import *
from eehelper import *
import numpy as np

if __name__ == '__main__':

    # script, folder, filename, res, version, use_limit = sys.argv

    folder = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/fires/'
    filelist = [  #'can_fire_multi_s1_extract_v2019_08_27T22_26_24.csv',
                'ak_fire_multi_extract_v2019_08_27T20_22_51.csv']

    res = 250
    version = 1
    fire_year_limit = (1950, 2018)

    for file_base_name in filelist:
        filename = folder + file_base_name
        Opt.cprint('File: {}'.format(file_base_name))

        OUTFILE = filename.split('.')[0] + 'reformat_{}_{}.csv'.format(str(res), str(version))

        # convert csv files to dicts
        list_dicts = Handler(filename).read_from_csv(return_dicts=True)

        Opt.cprint(len(list_dicts))

        outcolnames = ['ID', 'FIREID', 'SIZE_HA', 'longitude', 'latitude', 'decid1992', 'decid2000', 'decid2005',
                       'decid2010', 'decid2015', 'decid1992u', 'decid2000u', 'decid2005u', 'decid2010u', 'decid2015u',
                       'tc1992', 'tc2000', 'tc2005', 'tc2010', 'tc2015', 'tc1992u', 'tc2000u', 'tc2005u', 'tc2010u',
                       'tc2015u']

        samp_list = list()
        list_latlon = list()
        list_years = list()
        for elem in list_dicts:
            elem_list = [str(elem['FIREID']).replace('-', '').replace('_', '')\
                         .replace(' ', '').replace('(', '')\
                         .replace(')', '').replace('+', '') +
                         str(elem['YEAR']) +
                         str(elem['SIZE_HA']).replace('.', '')]

            for colname in outcolnames[1:]:
                elem_list.append(elem[colname])

            samp_list.append(elem_list)
            list_latlon.append((elem['latitude'], elem['longitude']))
            list_years.append(elem['YEAR'])

        list_all = np.vstack(samp_list)

        list_latlon = np.array(list_latlon)
        list_years = np.array(list_years)

        Opt.cprint(list_latlon.shape)
        Opt.cprint(list_all.shape)
        Opt.cprint(list_years.shape)

        uniq, indices, inverse, count = np.unique(ar=list_latlon,
                                                  axis=0,
                                                  return_index=True,
                                                  return_counts=True,
                                                  return_inverse=True)

        max_overlap = np.max(count)

        years_header = list('burnyear_{}'.format(str(i+1)) for i in range(max_overlap))

        Opt.cprint(max_overlap)

        Opt.cprint(uniq.shape)
        Opt.cprint(indices.shape)
        Opt.cprint(inverse.shape)
        Opt.cprint(count.shape)

        max_loc = np.where(count == max_overlap)[0]
        Opt.cprint(max_loc)

        uniq_max = uniq[max_loc][0]

        Opt.cprint(uniq_max)

        max_loc_orig = (np.where(inverse == max_loc[0])[0]).tolist()

        Opt.cprint(max_loc_orig)

        ll = list(list_dicts[i] for i in max_loc_orig)

        Opt.cprint(indices.shape)

        out_list = list_all[indices, :]

        years = np.zeros((indices.shape[0], max_overlap), dtype=np.int)

        single_count = np.where(count == 1)[0]
        Opt.cprint('Single fires: {}'.format(str(single_count.shape[0])))

        years[single_count, 0] = list_years[indices[single_count]]

        multiple_count = np.where(count > 1)[0]
        Opt.cprint('Multiple fires: {}'.format(str(multiple_count.shape[0])))

        def add_years(elem, inverse_arr):
            years_ = np.zeros(max_overlap, dtype=np.int)
            fyears_ = np.sort(list_years[np.where(inverse_arr == elem[0])[0]])[::-1]
            years_[0: fyears_.shape[0]] = fyears_
            return years_

        multi_year_matrix = np.apply_along_axis(add_years, 1, indices[multiple_count][:, np.newaxis], inverse)

        Opt.cprint(multi_year_matrix.shape)

        years[multiple_count, :] = multi_year_matrix

        out_matrix = np.hstack((out_list, years))

        Opt.cprint(out_matrix.shape)

        temp = (out_matrix[:, out_list.shape[1]].copy()).astype(np.int)
        year_loc = np.where((temp >= fire_year_limit[0]) & (temp <= fire_year_limit[1]))[0]

        out_matrix = out_matrix[year_loc, :]

        Opt.cprint(out_matrix.shape)
        Opt.cprint(out_matrix[0:20, :])

        Handler(OUTFILE).write_numpy_array_to_file(out_matrix, colnames=outcolnames + years_header)

        Opt.cprint('Written file: {}'.format(OUTFILE))
