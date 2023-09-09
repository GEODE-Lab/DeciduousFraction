from geosoup import *


if __name__ == '__main__':

    folder = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/tree_cover/"
    file1 = folder + "hansen_tc_2010_mosaic_vis_v1.shp"
    file2 = folder + "hansen_tc_2010_mosaic_vis_v1_100.shp"

    out_name = 'hansen_tc_2010'

    size = 5

    vec1 = Vector(file1)
    vec2 = Vector(file2)

    print(vec1)
    print(vec2)

    for i, geom_wkt in enumerate(vec2.wktlist):
        vec1.add_feat(vec1.get_osgeo_geom(geom_wkt),
                      attr=vec2.attributes[i])

    print(vec1)

    vec1.write_vector(outfile=folder + out_name + '_full.shp')

    divisions = [list(range(vec1.nfeat))[i::size] for i in xrange(size)]

    div_lengths = list(len(division) for division in divisions)
    print(div_lengths)

    for i, division in enumerate(divisions):
        print('Writing part {}'.format(str(i+1)))
        outfile = folder + out_name + '_part_{}.shp'.format(str(i+1))

        out_vec = Vector(name=out_name + '_part_{}'.format(str(i+1)),in_memory=True,
                         epsg=4326,
                         attr_def={'tc_value': 'int'},
                         primary_key=None,
                         geom_type='point')

        for feat_index in division:

            geom_wkt = vec1.wktlist[feat_index]

            attr = vec1.attributes[feat_index]

            out_vec.add_feat(out_vec.get_osgeo_geom(geom_wkt),
                             attr=attr)

        print(out_vec)
        out_vec.write_vector(outfile)

    exit(0)
