"""
This script is used to classify a raster using a selected RF model.
This script also generates the uncertainty raster.
"""

from geosoup import *
from geosoupML import *
import sys
import os
import numpy as np

if __name__ == '__main__':


    # read in the input files
    script, pickledir, compfile, outfile, cutoff = sys.argv

    prefix = 'decid_samp_clean_data_v13_corr'

    nbins = 50
    min_decid = 0
    max_decid = 10000
    step = int(float(max_decid) / float(nbins))
    bin_edges = Sublist.frange(min_decid, max_decid, step)
    cutoff = float(cutoff)

    compdicts = Handler(compfile).read_from_csv(return_dicts=True)

    for comp_dict in compdicts:
        print(comp_dict)

    good_pickle_list = list()
    for elem_dict in compdicts:
        rsq = elem_dict['rsq']
        if type(rsq).__name__ in ('int', 'float'):
            print(rsq)
            if rsq > cutoff:
                good_pickle_list.append(prefix + elem_dict['name'] + '.pickle')

    print('Number of files matching criteria: {}'.format(len(good_pickle_list)))
    print(good_pickle_list)

    picklefiles = Handler(dirname=pickledir).find_all(pattern='.pickle')

    outlist = list()
    Opt.cprint('\\nTotal {} files to read'.format(str(len(good_pickle_list))))

    count = 0

    for picklefile in picklefiles:

        if Handler(picklefile).basename in good_pickle_list:

            # print('Script: ' + script)
            Opt.cprint('Reading Random Forest file {} : {} of {}'.format(Handler(picklefile).basename,
                                                                         str(count+1),
                                                                         str(len(good_pickle_list))))

            # load classifier from file
            rf_classifier = RFRegressor.load_from_pickle(picklefile)

            samp_labels = rf_classifier.data['labels']

            # construct a histogram of deciduous fraction values
            hist, bin_edges = np.histogram(samp_labels, bins=bin_edges)

            if rf_classifier.output['rsq'] > float(cutoff):
                name = Handler(picklefile).basename.split('.pickle')

                out_dict = dict()
                out_dict['name'] = name[0]
                out_dict['rsq'] = rf_classifier.output['rsq']

                bin_names = list()
                for j, elem in enumerate(hist):
                    bin_names.append('bin' + str(j+1))

                out_dict.update(dict(zip(bin_names, list(str(elem) for elem in hist))))
                outlist.append(out_dict)

            rf_classifier = None

            count += 1

    Handler.write_to_csv(outlist, outfile)

