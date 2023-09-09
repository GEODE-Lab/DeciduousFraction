from modules import *
from sys import argv


if __name__ == '__main__':

    script, year, folder, extractfolder, regionfile, wrsfile = argv

    # find the wrs2 path and row that intersect with region boundary
    path_row = find_path_row(regionfile, wrsfile)

    # prepare list of tuples based on the path, row, and year
    tile_list = list()
    for pr in path_row:
        tile_list.append((pr[0], pr[1], year))

    # get server name
    server = TCserver
    print(server)

    # create ftp handle and connect
    ftp = FTPHandler(ftpserv=server,
                     dirname=folder)
    ftp.connect()

    # get a list of tile links on the ftp
    ftp.ftpfilepath = list()
    for tile_param in tile_list:
        tile_link = get_TCdata_filepath(*tile_param)['filestr']
        ftp.ftpfilepath.append(tile_link)

    # download all the ftp tiles in list
    ftp.getfiles()

    # disconnect the ftp
    ftp.disconnect()

    # extrat gz files
    gzfiles = Handler(dirname=folder).find_all('.gz')
    for gzfile in gzfiles:
        h = Handler(gzfile)
        if h.get_size() > 0:
            h.extract_gz(dirname=extractfolder)
        else:
            h.file_delete()

    print('Done!')
