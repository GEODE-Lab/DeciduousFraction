from geosoup import MultiRaster


if __name__ == '__main__':
    files = ["D:/temp/book_chapter/sentinel_img_2017_v3-0000000000-0000000000.tif",
             "D:/temp/book_chapter/sentinel_img_2017_v3-0000000000-0000023296.tif"]


    '''
    files = ["D:/temp/decid/decid_change_2000_2015_f3-0000023296-0000046592.tif",
             "D:/temp/decid/decid_change_2000_2015_f3-0000000000-0000023296.tif",
             "D:/temp/decid/decid_change_2000_2015_f3-0000000000-0000000000.tif",
             "D:/temp/decid/decid_change_2000_2015_f3-0000000000-0000046592.tif",
             "D:/temp/decid/decid_change_2000_2015_f3-0000023296-0000000000.tif",
             "D:/temp/decid/decid_change_2000_2015_f3-0000023296-0000023296.tif"]
    '''

    # outfile = "D:/temp/decid/decid_change_2000_2015_f3.tif"

    outfile = "D:/temp/book_chapter/sentinel_img_2017_v3.tif"

    mras = MultiRaster(files)

    mras.mosaic(add_overviews=True,
                outfile=outfile,
                nodata_values=None,
                compress='LZW',
                bigtiff='YES',
                output_resolution=(0.00018, 0.00018))
