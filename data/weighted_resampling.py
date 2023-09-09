from modules import *
import numpy as np
from sys import argv
from osgeo import gdal_array


if __name__ == '__main__':

    script, rasfile1, rasfile2, outrasfile = argv

    '''
    rasfile1 = "C:/temp/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis_nd.tif"
    rasfile2 = "C:/temp/ABoVE_median_SR_NDVI_boreal_2010_tc_prediction_vis_nd.tif"

    outrasfile = 'C:/temp/ABoVE_median_SR_NDVI_boreal_2010_prediction_vis_nd_low_res.tif'
    '''

    thresh = 25

    out_nodata = -9999.0
    out_dtype = np.float32

    out_resx = 0.0168
    out_resy = 0.0168

    ras1 = Raster(rasfile1)
    ras2 = Raster(rasfile2)

    ras1.initialize()
    ras2.initialize()

    print(ras1)
    print(ras2)

    outras = Raster(outrasfile)

    Handler(outrasfile).file_delete()

    outras.transform = (ras1.transform[0],
                        out_resx,
                        ras1.transform[2],
                        ras1.transform[3],
                        ras1.transform[4],
                        -1.0 * out_resy)

    outras.crs_string = ras1.crs_string

    in_resx = ras1.transform[1]
    in_resy = ras1.transform[5]

    nbands, nrows, ncols = ras1.shape

    ysize = float(nrows)*float(in_resy)
    xsize = float(ncols)*float(in_resx)

    n_xlargepix = np.abs(np.ceil(xsize/out_resx).astype(np.long))
    n_ylargepix = np.abs(np.ceil(ysize/out_resy).astype(np.long))

    print(n_ylargepix, n_xlargepix)

    outras.array = np.zeros([n_ylargepix, n_xlargepix],
                            dtype=out_dtype)

    outras.shape = [1, n_ylargepix, n_xlargepix]
    outras.bnames = [ras1.bnames[0]]

    ll = 1  # variable to iterate through output lines
    yi = 0  # starting point of finer res image lines
    row_list = list()  # list of tuple pairs for starting and ending line numbers for finer res
    while ll <= n_ylargepix:

        yf = (ll * out_resy) // in_resy  # ending point of finer pix lines

        if yf >= (nrows - 1):
            yf = nrows - 1
        elif (ll * out_resy) % in_resy == 0:  # if the value is 10.3 the smaller pixel y id is 10
            yf -= 1

        row_list.append((np.abs(np.long(yi)), np.abs(np.long(yf))))

        # next group of pixels include the overlapping finer pixels
        if yf >= (nrows - 1):
            break
        elif (ll * out_resy) % in_resy == 0:
            yi = yf + 1
        else:
            yi = yf

        ll += 1  # iterate

    cc = 1  # variable to iterate through output columns
    xi = 0  # starting point of finer res image columns
    col_list = list()  # list of tuple pairs for starting and ending column numbers for finer res
    while cc <= n_xlargepix:

        xf = (cc * out_resx) // in_resx  # ending point of finer pix columns

        if xf >= (ncols - 1):
            xf = ncols - 1
        elif (cc * out_resx) % in_resx == 0:  # if the value is 10.3 the smaller pixel x id is 10
            xf -= 1

        col_list.append((np.abs(np.long(xi)), np.abs(np.long(xf))))

        # next group of pixels include the overlapping finer pixels
        if xf >= (ncols - 1):
            break
        elif (cc * out_resx) % in_resx == 0:
            xi = xf + 1
        else:
            xi = xf

        cc += 1  # iterate

    # Reading a bunch of rows from finer res files
    # that overlap/contribute to larger res pix lines
    for k in range(nbands):

        for i, row in enumerate(row_list):

            py = row[0]
            ycount = row[1] - row[0] + 1

            ras1.read_array(offsets=(0, int(py), int(ncols), int(ycount)))
            ras2.read_array(offsets=(0, int(py), int(ncols), int(ycount)))

            out_row = np.zeros(n_xlargepix,
                               dtype=out_dtype) + out_nodata

            print('Row: {}'.format(str(i+1)))

            for j, col in enumerate(col_list):

                npix = np.float(np.abs(np.diff(row))[0] + 1) * np.float(np.abs(np.diff(col))[0] + 1)

                arr1 = (ras1.array[k, :, col[0]:col[1]]).astype(out_dtype)
                arr2 = (ras2.array[k, :, col[0]:col[1]]).astype(out_dtype)

                loc = np.where((arr2 >= thresh) & (arr2 != ras2.nodatavalue) & (arr1 != ras1.nodatavalue))

                nloc = np.float(loc[0].shape[0])

                if loc[0].shape[0] == 0:
                    out_row[j] = out_dtype(0)
                else:
                    out_row[j] = (np.sum(arr1[loc] * arr2[loc]) / np.sum(arr2[loc])) * (nloc / npix)

            outras.array[i, :] = out_row

    outras.shape = [1, n_ylargepix, n_xlargepix]
    outras.nodatavalue = out_nodata
    outras.bnames = ['decid']
    outras.dtype = gdal_array.NumericTypeCodeToGDALTypeCode(out_dtype)

    outras.write_to_file(outrasfile)

    exit()
