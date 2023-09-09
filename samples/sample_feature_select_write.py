import pandas as pd
from sys import argv

"""
This script is used to select features from an existing Samples class
 and write to a new csv file.
"""


def select_feat_n_save(infile, outfile, select_feat):
    """
    Method to select features in an existing file and write to output csv file
    :param infile: Input samples file
    :param outfile: Output samples file
    :param select_feat: Selected feature list
    :return: None
    """
    # make a samples() object
    samples = pd.read_csv(infile)

    samples = samples[select_feat]

    samples.to_csv(outfile, index=False)


if __name__ == '__main__':
    '''
    script, infile, outfile = argv

    '''
    codename = "v32_median1_4"

    infile_east = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
        "gee_extract_6_17_2020_formatted_md_east_data_only.csv"
    outfile_east = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
        "gee_extract_6_17_2020_formatted_md_east_reduced_feature.csv"

    infile_west = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
        "gee_extract_6_17_2020_formatted_md_west_data_only.csv"
    outfile_west = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/" + \
        "gee_extract_6_17_2020_formatted_md_west_reduced_feature.csv"

    # select features
    new_features = ['red_1', 'nir_1', 'swir1_1', 'ndwi_1', 'nbr_1', 'vari_1', 'savi_1',
                    'red_2', 'nir_2', 'swir1_2', 'ndwi_2', 'nbr_2', 'vari_2', 'savi_2',
                    'red_3', 'nir_3', 'swir1_3', 'ndwi_3', 'nbr_3', 'vari_3', 'savi_3',
                    'elevation', 'slope', 'aspect', 'decid_frac']

    select_feat_n_save(infile_west, outfile_west, new_features)
    select_feat_n_save(infile_east, outfile_east, new_features)
