from geosoup import Vector, Handler
import numpy as np
import sys


if __name__ == '__main__':

    start_year = 2000
    end_year = 2017
    pixel_size = 0.0021  # 250m MODIS resolution

    fire_year_col = 'FireYear'
    fire_id_col = 'FIREID'

    filelist = ['D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/ak_fire/FireAreaHistory.shp']
    outfolder = 'D:/temp/fire/'

    for infile in filelist:

        vec = Vector(infile)
        sys.stdout.write('========================\nInput Vector file: {}\n'.format(infile))

        attr = vec.attributes[0]
        attr_dict = dict()
        for k, v in attr.items():
            attr_dict[k] = Vector.string_to_ogr_type(v, 'name')

        order = np.argsort(np.array([int(attr_dict[fire_year_col]) for attr_dict in vec.attributes])).tolist()

        x_min, x_max, y_min, y_max = vec.layer.GetExtent()
        sys.stdout.write('Extent: {}\n'.format(' '.join([str(x_min), str(x_max), str(y_min), str(y_max)])))

        for year in range(start_year, end_year):
            outfile = outfolder + Handler(infile).basename.split('.shp')[0] + '_year_{}_250m.tif'.format(str(year))

            sys.stdout.write('---------------------\nOutfile: {}\n'.format(outfile))

            if type(attr[fire_year_col]) in (int, float, long):
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

            sys.stdout.write('Processed year {} - with {} geometries\n'.format(str(year),
                                                                               str(nfeat)))

            wkt_list = list()

            count = 0
            feat = layer.GetNextFeature()
            while feat:
                new_geom = feat.GetGeometryRef()
                if new_geom.GetGeometryType() < 0:
                    new_geom.FlattenTo2D()
                wkt_list.append(new_geom.ExportToWkt())
                feat = layer.GetNextFeature()
                count += 1

            vec.datasource.ReleaseResultSet(layer)

            temp_vec = Vector.vector_from_string(wkt_list,
                                                 spref=vec.spref,
                                                 vector_type='multipolygon')
            temp_lyr = temp_vec.layer

            temp_vec.rasterize(outfile=outfile,
                               pixel_size=(pixel_size, pixel_size),
                               extent=(x_min, y_max, x_max, y_min),
                               burn_values=[year],
                               all_touched=True,
                               nodatavalue=0,
                               compress='lzw')

            sys.stdout.write('Written {}!\n\n'.format(outfile))
