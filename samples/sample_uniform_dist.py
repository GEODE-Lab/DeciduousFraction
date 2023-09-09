from geosoupML import Samples
from geosoup import Handler
import numpy as np


"""
Script to remove sample skew at end bins and create a roughly uniform distribution
"""


def uniform_dist_samp(samples, bin_cutoff_pctl, nbins=10):
    """
    Method to Convert skewed samples to a near-uniform distribution
    :param samples: Samples() object
    :param bin_cutoff_pctl: Percentile at which to cutoff bins
    :param nbins: Number of bins
    :return:  Samples() object
    """
    samples.calc_histograms(nbins_x=nbins,
                            nbins_y=nbins)

    max_y = samples.y_bin_edges[-1]

    hist_bins = list(zip(samples.y_bin_edges[:-1], samples.y_bin_edges[1:]))

    bin_cutoff = np.percentile(samples.y_hist, [bin_cutoff_pctl], interpolation='nearest')

    samp_list = []
    other_list = []
    for bin_lower, bin_upper in hist_bins:
        if bin_upper < max_y:
            samp_indx = np.where((samples.y >= bin_lower) & (samples.y < bin_upper))[0]
        else:
            samp_indx = np.where((samples.y >= bin_lower) & (samples.y <= bin_upper))[0]

        if samp_indx.shape[0] <= bin_cutoff:
            samp_list += samp_indx.tolist()
        else:
            chosen_samp = np.random.choice(samp_indx, size=bin_cutoff, replace=False).tolist()
            other_samp = np.setdiff1d(samp_indx, np.array(chosen_samp), assume_unique=False).tolist()

            samp_list += chosen_samp
            other_list += other_samp

    outsamp = samples.subsample(samp_list)
    outsamp_other = samples.subsample(other_list)

    return outsamp, outsamp_other


if __name__ == '__main__':

    bin_cut_off_percentile = 67

    infile_east = "C:/Shared/projects/NAU/landsat_deciduous/data/samples/" \
                  "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_east_boreal_samp_useful.csv"
    outfile_east = Handler(infile_east).add_to_filename('_uniform_dist{}'.format(str(bin_cut_off_percentile)))

    infile_west = "C:/Shared/projects/NAU/landsat_deciduous/data/samples/" \
                  "gee_extract_ls5_ls8_ls7_v3_50_95_50pctl_uncorr_formatted_samples_west_boreal_samp_useful.csv"
    outfile_west = Handler(infile_west).add_to_filename('_uniform_dist{}'.format(str(bin_cut_off_percentile)))

    east_samp = Samples(csv_file=infile_east,
                        label_colname='decid_frac')

    west_samp = Samples(csv_file=infile_west,
                        label_colname='decid_frac')

    print(east_samp)
    print(west_samp)

    east_samp.calc_histograms(nbins_y=50)
    west_samp.calc_histograms(nbins_y=50)

    print(east_samp.y_hist)
    print(west_samp.y_hist)

    print('=====================')

    uniform_dist_samp_east, uniform_dist_samp_east_other_remaining = \
        uniform_dist_samp(east_samp, bin_cut_off_percentile, nbins=50)

    print(uniform_dist_samp_east)
    print(np.histogram(uniform_dist_samp_east.y, bins=50)[0])
    print('Removed {} samples'.format(str(east_samp.nsamp - uniform_dist_samp_east.nsamp)))
    uniform_dist_samp_east.save_to_file(outfile_east)

    other_east_file_name = Handler(outfile_east).add_to_filename('_other_remaining')
    uniform_dist_samp_east_other_remaining.save_to_file(other_east_file_name)

    uniform_dist_samp_west, uniform_dist_samp_west_other_remaining = \
        uniform_dist_samp(west_samp, bin_cut_off_percentile, nbins=50)
    print(uniform_dist_samp_west)
    print(np.histogram(uniform_dist_samp_west.y, bins=50)[0])
    print('Removed {} samples'.format(str(west_samp.nsamp - uniform_dist_samp_west.nsamp)))
    uniform_dist_samp_west.save_to_file(outfile_west)

    other_west_file_name = Handler(outfile_west).add_to_filename('_other_remaining')
    uniform_dist_samp_west_other_remaining.save_to_file(other_west_file_name)
