from geosoup import *
from eehelper import *
import numpy as np
import os
import sys


if __name__ == '__main__':




    file1 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/kernels/albedo_sw_clr_kernel.tif"
    outfile1 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/kernels/albedo_sw_clr_kernel_reproj_NA.tif"

    ras1 = Raster(file1)
    ras1.initialize(get_array=True)

    print(ras1)
    print(ras1.bnames)
    print(ras1.transform)
    print(ras1.shape)

    tie_pt = [ras1.transform[0], ras1.transform[3]]
    pixel_size = [ras1.transform[1], ras1.transform[5]]

    print(tie_pt)
    print(pixel_size)

    lc = ras1.array[:, -2]
    rc = ras1.array[:, 0]

    ras1.array[:, -1] = np.mean(np.vstack([ras1.array[:, -2], ras1.array[:, 0]]), 0)

    cutcol = 0

    for i in range(ras1.shape[2]):
        if i > 0:
            tie_pt[0] += pixel_size[0]

        if tie_pt[0] > 180.0:
            tie_pt[0] = tie_pt[0] - 360.0
            print(tie_pt)
            print(i)
            cutcol = i
            break

    print(ras1.array)

    arr1 = ras1.array[0:31, cutcol:]

    print(arr1)

    ras1.array = arr1

    ras1.shape = [1, arr1.shape[0], arr1.shape[1]]

    print(ras1.array.shape)
    print(ras1.array)

    ras1.transform = (tie_pt[0],
                      ras1.transform[1],
                      ras1.transform[2],
                      tie_pt[1],
                      ras1.transform[4],
                      ras1.transform[5])

    print(ras1)
    ras1.nodatavalue = -9999.0
    ras1.bnames = ['band_1']
    print(ras1)
    ras1.write_to_file(outfile1)
