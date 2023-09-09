from geosoup import *
from osgeo import osr, gdal, ogr
import numpy as np
from sys import argv

if __name__ == '__main__':

    '''

    script, infile, outfile, fire_year_col, fire_id_col = argv


    filelist = ['D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/NFDB_poly_20171106_gt500ha_s1_multi.shp',
                'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/NFDB_poly_20171106_gt500ha_s2_multi.shp',
                'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/NFDB_poly_20171106_gt500ha_s3_multi.shp',
                'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/NFDB_poly_20171106_gt500ha_geo_east.shp',
                'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/ak_fire/FireAreaHistory_1940_2018.shp',
                "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/NFDB_poly_20171106_gt500ha_geo_v2.shp"]
    '''

    filelist = ['D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/ak_fire/FireAreaHistory_1940_2018.shp']

    for infile in filelist:

        outfile = infile.split('.shp')[0] + '_top_layer_250m.tif'

        Opt.cprint(outfile)

        fire_year_col = 'FIREYEAR'
        fire_id_col = 'FIREID'

        start_year = 1900
        end_year = 2020
        pixel_size = 0.0021

        vec = Vector(infile)
        Opt.cprint(vec)

        attr = vec.attributes[0]

        Opt.cprint(attr)

        attr_dict = dict()
        for k, v in attr.items():
            attr_dict[k] = Vector.string_to_ogr_type(v, 'name')

        order = np.argsort(np.array([int(attr_dict[fire_year_col]) for attr_dict in vec.attributes])).tolist()

        x_min, x_max, y_min, y_max = vec.layer.GetExtent()
        Opt.cprint((x_min, x_max, y_min, y_max))

        x_size = int((x_max - x_min) / pixel_size)
        y_size = int((y_max - y_min) / pixel_size)

        Opt.cprint('Raster size: {} {}'.format(str(x_size),
                                               str(y_size)))

        ras = Raster(outfile)
        ras.bnames = [vec.name]
        ras.dtype = 0
        ras.transform = [x_min,
                         pixel_size,
                         0.0,
                         y_max,
                         0.0,
                         -1.0 * pixel_size]

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

        total_count = 0

        for j, year in enumerate(range(start_year, end_year + 1)):

            if type(attr[fire_year_col]) in (int, float):

                layer = vec.datasource.ExecuteSQL("SELECT * from {} WHERE {}={}".format(vec.name,
                                                                                        fire_year_col,
                                                                                        str(year)))
            elif type(attr[fire_year_col]) == str:

                layer = vec.datasource.ExecuteSQL("SELECT * from {} WHERE {}='{}'".format(vec.name,
                                                                                          fire_year_col,
                                                                                          str(year)))
            else:
                raise ValueError("unknown or null property type for selected attribute")

            nfeat = layer.GetFeatureCount()

            if nfeat == 0:
                vec.datasource.ReleaseResultSet(layer)
                continue

            total_count += nfeat

            Opt.cprint('Processing year {} / {} - with {} geometries'.format(str(year),
                                                                             str(end_year),
                                                                             str(nfeat)),
                       newline='')

            # multi_geom = ogr.Geometry(ogr.wkbMultiPolygon)
            wkt_list = list()

            count = 0
            feat = layer.GetNextFeature()
            while feat:
                new_geom = feat.GetGeometryRef()
                new_wkt = new_geom.ExportToWkt()
                # multi_geom.AddGeometryDirectly(ogr.CreateGeometryFromWkt(new_wkt))
                wkt_list.append(new_wkt.replace(' 0,', ','))
                feat = layer.GetNextFeature()
                count += 1

            vec.datasource.ReleaseResultSet(layer)

            # res = multi_geom.UnionCascaded()

            Opt.cprint(' - {} found - '.format(str(count)),
                       newline='')

            # wkt_string = multi_geom.ExportToWkt().replace(' 0,', ',')

            temp_vec = Vector.vector_from_string(wkt_list,
                                                 spref=spref,
                                                 vector_type='multipolygon')
            temp_lyr = temp_vec.layer

            Opt.cprint(temp_vec, newline='')

            result = gdal.RasterizeLayer(ras.datasource,
                                         [1],
                                         temp_lyr,
                                         None,
                                         None,
                                         [year],
                                         ["ALL_TOUCHED=TRUE"])

            Opt.cprint(' - burned value {}'.format(str(year)))

        ras.datasource = None

        Opt.cprint(total_count)
        Opt.cprint('Written {}!\n\n'.format(outfile))
