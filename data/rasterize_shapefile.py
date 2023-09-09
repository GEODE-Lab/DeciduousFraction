if __name__ == '__main__':

    import sys
    import os

    module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(module_path)
    from modules import Vector

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
