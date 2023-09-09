from geosoup import Handler, Vector
from geosoupML import Samples
import numpy as np
import json


"""
Use this script to prepare training and validation samples for TC-decid-albedo RF models
after dealing with non-numeric columns in the csv files
"""


# main program
if __name__ == '__main__':

    # script, infolder, outfile, label_colname, suffix, ncpus = argv

    suffix = 'fal'
    label_colname = 'albedo'

    tc_cutoff = 25

    infolder = 'D:/temp/albedo/albedo_decid_tc_samp_v2/clean/'

    all_sampfile = 'D:/temp/albedo/albedo_decid_tc_samp_v2/all_samp_{}.csv'.format(suffix)

    trn_sampfile = 'D:/temp/albedo/albedo_decid_tc_samp_v2/{}_training_samples_{}.csv'.format(label_colname, suffix)
    val_sampfile = 'D:/temp/albedo/albedo_decid_tc_samp_v2/{}_validation_samples_{}.csv'.format(label_colname, suffix)

    files = Handler(dirname=infolder).find_all('*{}.csv'.format(suffix))

    all_samp_dict = []

    for filename in files:
        print(filename)
        lines = Handler(filename).read_text_by_line()
        headers = lines[0].split(',')
        year = None
        out_header = []
        for header in headers:
            if 'tc' in header:
                year = int(header.replace('tc', ''))
                header = 'tc'
                out_header.append(header)
            elif 'decid' in header:
                header = 'decid'
                out_header.append(header)
            else:
                out_header.append(header)
        out_header = out_header[:-1] + ['wkt', 'year']

        print(out_header)

        out_dicts = []
        for line in lines[1:]:
            non_geom, geom = line.split(',"{')
            geom = ('"{' + geom).replace('""', '"').replace('"{', '{').replace('}"', '}')
            osgeo_geom = Vector.get_osgeo_geom(geom, geom_type='json')
            wkt = osgeo_geom.ExportToWkt()

            samp_dict = dict(zip(out_header, non_geom.split(',') + [wkt, year]))

            out_dicts.append(samp_dict)

            if samp_dict['tc'] != '':
                try:
                    temp = float(samp_dict['tc'])
                    all_samp_dict.append(samp_dict)
                except:
                    pass

        for out_dict in out_dicts[:5]:
            print(out_dict)

    print(len(all_samp_dict))
    # print('Writing {}'.format(all_sampfile))

    # Handler.write_to_csv(all_samp_dict, outfile=all_sampfile)

    all_samp = Samples(all_sampfile, label_colname=label_colname)

    print('All samples combined:')
    print(all_samp)

    tc_loc = all_samp.x_name.index('tc')

    print(all_samp.x)

    bad_samp_loc = np.where(all_samp.x[:, tc_loc].astype(np.float) < tc_cutoff)

    working_samp = all_samp.select_inverse(bad_samp_loc[0])

    trn_samp, val_samp = working_samp.random_partition(75)

    print(trn_samp)
    print(val_samp)

    trn_samp.save_to_file(trn_sampfile)
    val_samp.save_to_file(val_sampfile)
