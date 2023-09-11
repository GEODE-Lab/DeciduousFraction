from geosoup import *
from sys import argv


if __name__ == '__main__':

    file1 = "C:/Users/Richard/Downloads/gadm36_CAN_shp/gadm36_CAN_0.shp"

    pixel_size = (0.0021, 0.0021)
    extent = (-179.9, -50.0, 10.0, 85.0)

    vector1 = Vector(file1,
                     in_memory=True)

    Opt.cprint(vector1)
    Opt.cprint(vector1.attributes)

    vector1.rasterize(pixel_size=pixel_size,
                      extent=extent)

    Opt.cprint('Completed!')
