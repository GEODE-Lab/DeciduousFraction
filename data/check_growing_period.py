from geosoup import Handler
import json
import numpy as np


'''
This script is use to check the growing period times based on MLCD (MODIS land cover dataset)
The variables used are greenup day, peak day, and dormancy day. 
I am computing annual means for each epoch to check the time periods used for compositing.  
'''

if __name__ == '__main__':

    year_bins = {2000: (2000, 2003),
                 2005: (2003, 2008),
                 2010: (2008, 2013),
                 2015: (2013, 2019)}

    metrics = ['Greenup_1', 'Peak_1', 'Dormancy_1']

    delimiter = ','
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/MLCD_ran_samp_boreal_v1.csv"
    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/MLCD_ran_samp_boreal_v1_proper.csv"

    lines = Handler(infile).read_text_by_line()

    headers = list(elem.strip() for elem in lines[0].split(','))

    list_dicts = []

    for il, line in enumerate(lines):
        if il != 0:
            row_dict = {}
            col_elems = line.split(delimiter)
            for ic, col_header in enumerate(headers):
                if ic != (len(headers) - 1):
                    row_dict[col_header] = Handler.string_to_type(col_elems[ic])
                else:
                    geom_dict = json.loads(delimiter.join(col_elems[ic:])
                                           .replace('""', '"')
                                           .replace('"{', '{')
                                           .replace('}"', '}'))
                    row_dict['longitude'], row_dict['latitude'] = geom_dict['coordinates']

            list_dicts.append(row_dict)

    for list_dict in list_dicts[0:5]:
        print(list_dict)

    # Handler.write_to_csv(list_dicts, outfile=outfile)
    label_dict = {}
    for metric in metrics:
        for year, year_range in year_bins.items():
            label_dict[metric + '_' + str(year)] = \
                list(metric + '_' + str(range_year) for range_year in range(*year_range))

    sum_results = dict(zip(list(label_dict), list([] for _ in list(label_dict))))

    for samp_dict in list_dicts:
        for epoch_label, label_list in label_dict.items():
            for label in label_list:
                if label in samp_dict:
                    sum_results[epoch_label].append(samp_dict[label])

    greenup_arr = np.array([])
    peak_arr = np.array([])
    dornamcy_arr = np.array([])

    for epoch_label, _ in label_dict.items():
        arr = np.array(sum_results[epoch_label])

        if 'Greenup_1' in epoch_label:
            temp_arr = arr[np.where((arr > 60) & (arr <= 140))]
            greenup_arr = np.hstack([greenup_arr, temp_arr])

        elif 'Peak_1' in epoch_label:
            temp_arr = arr[np.where((arr > 90) & (arr <= 270))]
            peak_arr = np.hstack([peak_arr, temp_arr])

        elif 'Dormancy_1' in epoch_label:
            temp_arr = arr[np.where((arr > 120) & (arr <= 330))]
            dornamcy_arr = np.hstack([dornamcy_arr, temp_arr])

        else:
            raise ValueError('Epoch label not recognized')

        median = np.median(temp_arr)
        std = np.std(temp_arr)
        min = np.min(temp_arr)
        max = np.max(temp_arr)

        print('Epoch: {} | Median: {} | Std: {} | Min: {} | Max: {}'.format(epoch_label,
                                                                            median,
                                                                            std,
                                                                            min,
                                                                            max))

    print('===================================')

    arr_name_idx = 0
    for temp_arr in [greenup_arr, peak_arr, dornamcy_arr]:
        median = np.median(temp_arr)
        std = np.std(temp_arr)
        min = np.min(temp_arr)
        max = np.max(temp_arr)

        print('Overall {} | Median: {} | Std: {} | Min: {} | Max: {}'.format(metrics[arr_name_idx],
                                                                             median,
                                                                             std,
                                                                             min,
                                                                             max))
        arr_name_idx += 1

