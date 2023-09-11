import sys
import os
from geosoup import  *
import numpy as np
import scipy

if __name__ == '__main__':
    '''
    folder = 'C:/temp/tc/decid2/in/'
    files = Handler(dirname=folder).find_all(pattern='*.tif')

    outfolder = 'C:/temp/tc/decid2/out/'
    '''
    files = ["C:/temp/albedo/" + \
        "forcing_2000_2015_tc25_500m.tif"]

    outfolder = "C:/temp/albedo/"

    for file_ in files:
        print(file_)

        outfile = outfolder + Handler(file_).basename.split('.')[0] + '_full.tif'

        ras1 = Raster(file_)
        ras1.initialize(get_array=True)
        print(ras1.array)

        print(ras1.array.max())
        print(ras1.array.min())

        # ras1.array[np.where(ras1.array > 100)] = 0

        ras1.nodatavalue = 0

        ras1.write_to_file(outfile)
