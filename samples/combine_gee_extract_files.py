from geosoup import Handler, Opt
import sys


"""
Script to combine multiple GEE extracted CSV files
"""


def combine_files(in_folder,
                  out_file,
                  append=True,
                  pattern='.csv'):
    """
    Method to write data from multiple csv files into one
    :param in_folder: Folder with csv files
    :param out_file: Output csv file name
    :param append: if the data should be appended to outfile
    :param pattern: pattern to search for files (default: .csv)
    :return: None
    """

    files = Handler(dirname=in_folder).find_all(pattern=pattern)
    nfiles = len(files)

    Opt.cprint('Reading {} files'.format(nfiles))
    dict_list = []

    for ii, in_file in enumerate(files):

        file_dicts = Handler(in_file).read_from_csv(return_dicts=True)
        nlines = len(file_dicts)

        Opt.cprint("Working on file : {}  {} of {} with {} lines".format(in_file,
                                                                         str(ii + 1),
                                                                         str(nfiles),
                                                                         str(nlines)))
        if append:
            Handler.write_to_csv(file_dicts,
                                 outfile=out_file,
                                 append=append)
        else:
            dict_list += file_dicts

    if not append:
        return dict_list
    return 0


if __name__ == '__main__':

    script, infolder, outfile = sys.argv

    Handler(outfile).file_delete()

    combine_files(infolder, outfile)

    n_lines_out = Handler(outfile).file_lines()

    Opt.cprint('Outfile: {}'.format(outfile))
    Opt.cprint("Final number of lines in the out file: {}".format(str(n_lines_out)))
