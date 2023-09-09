from geosoup import *
from geosoupML import *

from osgeo import osr, gdal
import numpy as np
from sys import argv


if __name__ == '__main__':

    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/" + \
             "NFDB_poly_20171106_gt100ha_geo_east.shp"
    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/" + \
             "NFDB_poly_20171106_gt100ha_geo_east.tif"
    
    fire_year_col = 'YEAR'
    fire_id_col = 'FIRE_ID'

    start_year = 1950
    end_year = 2018

    '''

    script, infile, outfile, fire_year_col, fire_id_col = argv
    '''

    vec = Vector(infile)
    print(vec)

    attr = vec.attributes[0]

    attr_dict = dict()
    for k, v in attr.items():
        attr_dict[k] = Vector.string_to_ogr_type(v, 'name')

    for k, v in attr_dict.items():
        if v != 'nonetype':
            print(k, v)

    order = np.argsort(np.array([int(attr_dict[fire_year_col]) for attr_dict in vec.attributes])).tolist()

    print(len(order))

    # vec.datasource.ReleaseResultSet(ordered_layer)

    x_min, x_max, y_min, y_max = vec.layer.GetExtent()
    print(x_min, x_max, y_min, y_max)

    pixel_size = 0.00027

    x_size = int((x_max - x_min) / pixel_size)
    y_size = int((y_max - y_min) / pixel_size)

    ras = Raster(outfile)
    ras.bnames = [vec.name]
    ras.dtype = 0
    ras.transform = [x_min,
                     pixel_size,
                     0.0,
                     y_max,
                     0.0,
                     -1.0*pixel_size]

    spref = osr.SpatialReference()
    spref.ImportFromProj4('+proj=longlat +datum=WGS84')
    ras.crs_string = spref.ExportToWkt()

    ras.nodatavalue = 0
    ras.dtype = gdal.GDT_Int16

    ras.shape = [1, y_size, x_size]

    ras.datasource = gdal.GetDriverByName('GTiff').Create(ras.name,
                                                          ras.shape[2],
                                                          ras.shape[1],
                                                          ras.shape[0],
                                                          ras.dtype,
                                                          ['COMPRESS=LZW',
                                                           'BIGTIFF=YES'])

    ras.datasource.SetGeoTransform(ras.transform)
    ras.datasource.SetProjection(ras.crs_string)

    for j, i in enumerate(order[1:1000]):

        id_ = vec.attributes[i][fire_id_col]
        year_ = int(vec.attributes[i][fire_year_col])

        if id_ is None:
            id_ = '{}_{}'.format(str(j+1),
                                 str(vec.attributes[i][fire_year_col]))

        Opt.cprint('Processing fire ID {} from {}: {} of {}'.format(id_,
                                                                    year_,
                                                                    str(j + 1),
                                                                    str(vec.nfeat)),
                   newline='')

        if year_ < 1920:
            Opt.cprint('')
            continue

        wkt_string = vec.wktlist[i]

        temp_vec = Vector.vector_from_string(wkt_string,
                                             spref=spref)
        temp_lyr = temp_vec.layer

        result = gdal.RasterizeLayer(ras.datasource,
                                     [1],
                                     temp_lyr,
                                     None,
                                     None,
                                     [int(vec.attributes[i][fire_year_col])],
                                     ["ALL_TOUCHED=TRUE"])

        Opt.cprint(' - burned value {}'.format(year_))

    ras.datasource = None

