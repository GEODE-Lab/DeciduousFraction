from sys import argv
from geosoup import Handler, Raster, Vector

"""
This script goes through a folder of tif files and compiles 
their boundaries. Each boundary is then saved as a feature in 
a shapefile.
"""

# main program
if __name__ == '__main__':
    # import folder name containing all the rasters, and the shapefile to output
    if len(argv) == 3:
        script, rasterfiledir, outfile = argv
        boundary_file = None
    elif len(argv) == 4:
        script, rasterfiledir, outfile, boundary_file = argv
    else:
        raise ValueError('Incorrect number of arguments')

    sep = Handler().sep

    file_list = Handler(rasterfiledir).find_all('*.tif')

    print('------------------------------------------')
    print('Files found: {}'.format(str(len(file_list))))

    raster0 = Raster(file_list[0])
    raster0.initialize()
    print(raster0)

    print(boundary_file)

    if boundary_file is not None:
        area_bound = Vector(boundary_file)
        print(area_bound)
    else:
        area_bound = None

    temp_vec = Vector(name='tiles_vector',
                      spref_str=raster0.crs_string,
                      primary_key=None,
                      in_memory=True,
                      geom_type='polygon',
                      attr_def={'filename': 'str'})

    print('Total raster count: {}'.format(str(len(file_list))))

    if area_bound is not None:
        area_geom = Vector.get_osgeo_geom(area_bound.wktlist[0])
        area_geom.CloseRings()
    else:
        area_geom = None

    exclude_list = list()
    include_list = list()

    for i, file_name in enumerate(file_list):

        raster = Raster(file_name)
        raster.initialize()

        raster_bounds = Vector.get_osgeo_geom(temp_vec.wkt_from_coords(raster.bounds,
                                                                       geom_type='polygon'))
        raster_bounds.CloseRings()

        if area_geom is not None:

            if area_geom.Intersects(raster_bounds):
                print('{} : {} : included'.format(str(i + 2), raster))
                include_list += [file_name]
                temp_vec.add_feat(raster_bounds,
                                  attr={'filename': Handler(file_name).basename},
                                  primary_key=None)
            else:
                print('{} : {} : excluded'.format(str(i + 2), raster))
                exclude_list += [file_name]
        else:
            temp_vec.add_feat(raster_bounds,
                              attr={'filename': Handler(file_name).basename},
                              primary_key=None)
        print(raster)

    if len(exclude_list) > 0 or len(include_list) > 0:
        exclude_file = outfile.split('.')[0] + '_exclude.txt'
        include_file = outfile.split('.')[0] + '_include.txt'

        Handler(exclude_file).write_list_to_file(exclude_list)
        Handler(include_file).write_list_to_file(include_list)

    print('Total raster count: {}'.format(str(len(file_list))))
    print(temp_vec)

    temp_vec.write_vector(outfile)
