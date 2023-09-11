import sys
import os
from geosoup import Vector

if __name__ == '__main__':



    infile = "C:/temp/arctic_oroarctic_wgs84.shp"
    outshpfile = "C:/temp/arctic_oroarctic_wgs84_2km.shp"
    outfile = "C:/temp/arctic_oroarctic_wgs84_2km.tif"

    buf_size = 0.0168
    pixel_size = (0.0168, 0.0168)

    vec = Vector(infile)

    print(vec)

    vec_buf = vec.buffer(buf_size, return_vector=True)

    print(vec_buf)

    vec_buf.write_vector(outshpfile)

    vec_buf.rasterize(outfile, pixel_size, 1, 0, None)
