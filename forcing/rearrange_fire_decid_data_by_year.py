from geosoup import Handler, Opt

"""
This script only reformts the GEE extracted data to be plotted in a different script. 
The data is resampled from 30 m to 250 m using bilinear interpolation in GEE and then extracted to a csv
The decid fraction is not thresholded using %treecover. 
"""


if __name__ == '__main__':

    in_dir = "d:/shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/fires/"
    out_dir = in_dir + "burn_samp_250_by_5yr/"

    filelist = ['ak_fire_multi_extract_v2019_08_27T20_22_51reformat_250_1.csv',
                'can_fire_multi_s2_extract_v2019_08_27T20_37_27reformat_250_1.csv',
                'can_fire_multi_s1_extract_v2019_08_27T22_26_24reformat_250_1.csv',
                'can_fire_multi_s3_extract_v2019_08_27T20_22_56reformat_250_1.csv']

    decid_bands = ['decid1992', 'decid2000', 'decid2005', 'decid2010', 'decid2015']
    tc_bands = ['tc1992', 'tc2000', 'tc2005', 'tc2010', 'tc2015']

    decid_uncertainty_bands = ['decid1992u', 'decid2000u', 'decid2005u', 'decid2010u', 'decid2015u']
    tc_uncertainty_bands = ['tc1992u', 'tc2000u', 'tc2005u', 'tc2010u', 'tc2015u']

    fire_cols = ['ID', 'FIREID', 'SIZE_HA', 'longitude', 'latitude']
    burn_cols = list('burnyear_{}'.format(str(i+1)) for i in range(20))

    # year_edges = [(1950, 1960), (1960, 1970), (1970, 1980),
    #               (1980, 1990), (1990, 2000), (2000, 2010), (2010, 2018)]

    year_edges = [(1950, 1955), (1955, 1960), (1960, 1965), (1965, 1970), (1970, 1975), (1975, 1980),
                  (1980, 1985), (1985, 1990), (1990, 1995), (1995, 2000), (2000, 2005),  (2005, 2010),
                  (2010, 2015)]
    year_names = list('year{}_{}'.format(str(year_edge[0])[2:], str(year_edge[1])[2:]) for year_edge in year_edges)

    ncheck = 100000  # number at which to write to files
    count = 0  # count of dictionaries in memory, each dict is info on one 250m pixel

    # list of files
    outfile_single_list = list(out_dir + year_name + '_single_fire.csv' for year_name in year_names)
    outfile_multiple_list = list(out_dir + year_name + '_multiple_fire.csv' for year_name in year_names)

    # list of values
    # initialize list of lists
    single_burns = list(list() for _ in year_edges)
    multiple_burns = list(list() for _ in year_edges)

    # iterate thru files
    for fi, filename in enumerate(filelist):
        Opt.cprint('Reading file : {}'.format(filename))

        # filepath
        infile = in_dir + filename

        # read dictionaries
        val_dicts = Handler(infile).read_from_csv(return_dicts=True)

        print('Number of samp in file {}: {}'.format(filename,
                                                     str(len(val_dicts))))

        # iterate thru dictionaries
        for val_dict in val_dicts:

            out_dict = dict()

            # copy all band/column values to output dict
            for key in decid_bands + tc_bands + decid_uncertainty_bands + tc_uncertainty_bands + fire_cols:
                out_dict[key] = val_dict[key]

            year_list = list()

            # add all the burn column names to output dict
            for burn_col in burn_cols:
                if burn_col in val_dict:
                    if int(val_dict[burn_col]) > 0:
                        year_list.append(int(val_dict[burn_col]))

            # sort year list from earliest to latest
            year_list = sorted(year_list)

            for i, burn_col in enumerate(burn_cols):
                if i < len(year_list):
                    out_dict[burn_col] = year_list[i]
                else:
                    out_dict[burn_col] = 0

            # find year of first fire
            start_year = year_list[0]

            # check start year and append to multiple or single
            # list of lists based on the year bin edges
            for i, year_edge in enumerate(year_edges):

                # assign start year bin
                if year_edge[0] <= start_year < year_edge[1]:

                    # check for multiple fires and append to the correct list
                    if len(year_list) > 1:
                        multiple_burns[i].append(out_dict)
                    else:
                        single_burns[i].append(out_dict)
                    break

            count += 1

            # write all the list items to the appropriate file
            # all lists should empty
            if count > ncheck:
                count = 0

                # find all the samples in the multiple and single lists
                for i in range(len(year_edges)):

                    if len(multiple_burns[i]) > 0:

                        # write to a new file if it doesnt exist
                        if Handler(outfile_multiple_list[i]).file_exists():
                            Opt.cprint('---- Writing {} samples to existing file {}'.format(str(len(multiple_burns[i])),
                                                                                       outfile_multiple_list[i]))
                            Handler.write_to_csv(multiple_burns[i],
                                                 outfile_multiple_list[i],
                                                 append=True)
                        else:
                            Opt.cprint('---- Writing {} samples to new file {}'.format(str(len(multiple_burns[i])),
                                                                                       outfile_multiple_list[i]))
                            Handler.write_to_csv(multiple_burns[i],
                                                 outfile_multiple_list[i])
                        multiple_burns[i] = list()

                    if len(single_burns[i]) > 0:
                        if Handler(outfile_single_list[i]).file_exists():
                            Opt.cprint('---- Writing {} samples to existing file {}'.format(str(len(single_burns[i])),
                                                                                       outfile_single_list[i]))
                            Handler.write_to_csv(single_burns[i],
                                                 outfile_single_list[i],
                                                 append=True)
                        else:
                            Opt.cprint('---- Writing {} samples to new file {}'.format(str(len(single_burns[i])),
                                                                                  outfile_single_list[i]))
                            Handler.write_to_csv(single_burns[i],
                                                 outfile_single_list[i])
                        single_burns[i] = list()



