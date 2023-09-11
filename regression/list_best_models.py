from geosoup import *
from geosoupML import *
import json


if __name__ == "__main__":

    # file1 = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_test/' \
    #        'results_summary_v28_median2_summer_mean.csv'
    # file1 = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_test/' \
    #        'results_summary_v28_median2_summer.csv'

    # file1 = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_test/' \
    #        'results_summary_v28_median2.csv'
    # file1 = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_test/' \
    #        'results_summary_v28_median2_mean.csv'

    file1 = "C:/Users/rm885/Downloads/results_summary_v1_1_summer.csv"

    flines = Handler(file1).read_from_csv(return_dicts=True)

    klines = list()
    for line in flines:
        if line['fold_sd'] < 2.0:

            line['x'] = line['rsq'] - line['fold_sd'] * 0.5
            klines.append(line)

    klines = list(reversed(sorted(klines, key=lambda x: x['x'])))

    for line in klines[:10]:
        print(line)

    print(len(klines))
    print('\n')

    file1 = "C:/Users/rm885/Downloads/results_summary_v1_2.csv"

    flines = Handler(file1).read_from_csv(return_dicts=True)

    klines = list()
    for line in flines:
        if line['fold_sd'] < 2.0:
            line['x'] = line['rsq'] - line['fold_sd'] * 0.5
            klines.append(line)

    klines = list(reversed(sorted(klines, key=lambda x: x['x'])))

    for line in klines[:10]:
        print(line)

    print(len(klines))
    print('\n')







