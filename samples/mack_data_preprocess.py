from geosoup import Handler, Opt
import numpy as np
from sys import argv


if __name__ == '__main__':

    # script, folder, filename, res, version, use_limit = argv

    folder = "C:/temp/decid/"
    filename = "gee_mack_data_extract_250_v2019_06_14T03_55_15.csv"
    res = 250
    version = 0
    use_limit = 0

    filename = folder + filename

    fire_year_limit = [2000, 2019]

    # top left and bottom right pixel longitude latitude
    if int(use_limit) == 1:
        limits = [(-151.5391818876974, 67.1375627875029), (
            -142.9478732939474, 64.23698454727263)]
        OUTFILE = filename.split('.')[0] + '_{}_{}_lim.csv'.format(str(res), str(version))
    else:
        limits = None
        OUTFILE = filename.split('.')[0] + '_{}_{}.csv'.format(str(res), str(version))

    list_dicts = Handler(filename).read_from_csv(return_dicts=True)


    def find_limits(vec_):
        if limits[0][0] <= float(vec_['longitude']) < limits[1][0] and \
                limits[1][1] <= float(vec_['latitude']) < limits[0][1]:
            return True
        else:
            return False


    if limits is not None:
        list_dicts = list(list_dicts[i] for i, elem in enumerate(map(find_limits, list_dicts)) if elem)

    Opt.cprint(len(list_dicts))

    list_all = np.vstack(list((elem['id'].replace('_', ''), elem['latitude'], elem['longitude'],
                               elem['EPA_DESIG'], elem['FIREID'],
                               elem['elevation'], elem['slope'], elem['aspect'],
                               float(elem['decid_frac']) * 0.01) for elem in list_dicts))

    out_cols_names = ['id', 'latitude', 'longitude',
                      'EPA_zone', 'fire_id',
                      'elevation', 'slope', 'aspect',
                      'decid_frac_2000']

    list_latlon = np.vstack(list((elem['latitude'], elem['longitude']) for elem in list_dicts))
    list_years = np.array(list(elem['FireYear'] for elem in list_dicts), dtype=np.int)

    Opt.cprint(list_latlon.shape)
    Opt.cprint(list_all.shape)
    Opt.cprint(list_years.shape)

    uniq, indices, inverse, count = np.unique(ar=list_latlon,
                                              axis=0,
                                              return_index=True,
                                              return_counts=True,
                                              return_inverse=True)

    max_overlap = np.max(count)

    years_header = list('burn_year_{}'.format(str(i + 1)) for i in range(max_overlap))

    Opt.cprint(max_overlap)

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

    Handler(OUTFILE).write_numpy_array_to_file(out_matrix, colnames=out_cols_names + years_header)

    Opt.cprint('Written file: {}'.format(OUTFILE))
