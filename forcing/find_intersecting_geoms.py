from geosoup import *
from eehelper import *
import numpy as np


if __name__ == '__main__':

    file2 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/" \
            "NFDB_poly_20171106_gt500ha_ABoVE_geo_boreal_s2.shp"
    outfile2 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/NFDB_poly_20171106_gt500ha_s2_multi.shp"

    vec2 = Vector(file2)

    vec2.wktlist = list(elem.replace(' 0,', ',') for elem in vec2.wktlist)

    print(vec2)

    wkt_marker = list(0 for _ in vec2.wktlist)

    nsamp = vec2.nfeat
    intersect_count = 0

    for i in range(nsamp):
        for j in range(i, nsamp):
            if (wkt_marker[i] + wkt_marker[j] <= 1) and (i != j):

                if (Vector.get_osgeo_geom(vec2.wktlist[i])).Intersects(Vector.get_osgeo_geom(vec2.wktlist[j])):
                    wkt_marker[i] = 1
                    wkt_marker[j] = 1

                    intersect_count += 1
                    print('Can {} : {} : {} : True'.format(str(i + 1), str(j + 1), str(intersect_count)))

    intersect_mark = (np.where(np.array(wkt_marker) > 0)[0]).tolist()

    vec2_ = vec2
    vec2_.wktlist = list(vec2.wktlist[i] for i in intersect_mark)
    vec2_.attributes = list(vec2.attributes[i] for i in intersect_mark)

    vec2_.write_vector(outfile2)

    file2 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/can_fire/" \
            "NFDB_poly_20171106_gt500ha_ABoVE_geo_boreal_s1.shp"
    outfile2 = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/FIRE/NFDB_poly_20171106_gt500ha_s1_multi.shp"

    vec2 = Vector(file2)

    vec2.wktlist = list(elem.replace(' 0,', ',') for elem in vec2.wktlist)

    print(vec2)

    wkt_marker = list(0 for _ in vec2.wktlist)

    nsamp = vec2.nfeat
    intersect_count = 0

    for i in range(nsamp):
        for j in range(i, nsamp):
            if (wkt_marker[i] + wkt_marker[j] <= 1) and (i != j):

                if (Vector.get_osgeo_geom(vec2.wktlist[i])).Intersects(Vector.get_osgeo_geom(vec2.wktlist[j])):
                    wkt_marker[i] = 1
                    wkt_marker[j] = 1

                    intersect_count += 1
                    print('Can {} : {} : {} : True'.format(str(i + 1), str(j + 1), str(intersect_count)))

    intersect_mark = (np.where(np.array(wkt_marker) > 0)[0]).tolist()

    vec2_ = vec2
    vec2_.wktlist = list(vec2.wktlist[i] for i in intersect_mark)
    vec2_.attributes = list(vec2.attributes[i] for i in intersect_mark)

    vec2_.write_vector(outfile2)