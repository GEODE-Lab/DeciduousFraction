from sys import argv
import os
from geosoup import Handler, Raster, Vector

"""
This script goes through a folder of tif files and compiles 
their boundaries. Each boundary is then saved as a feature in 
a shapefile.
"""

years = [1992, 2000, 2005, 2010, 2015]

# main program
if __name__ == '__main__':
    # import folder name containing all the rasters, and the shapefile to output
    script, rasterfiledir, outfolder = argv

    sep = Handler().sep

    for year in years:

        file_list = Handler(rasterfiledir).find_all('*{}*.tif'.format(str(year)))

        print('------------------------------------------')
        print('Files found: {}'.format(str(len(file_list))))

        raster0 = Raster(file_list[0])
        raster0.initialize()
        print(raster0)

        temp_vec = Vector(name='tiles_vector',
                        spref_str=raster0.crs_string,
                        primary_key=None,
                        in_memory=True,
                        geom_type='polygon',
                        attr_def={'filename': 'str'})

        print('Total raster count: {}'.format(str(len(file_list))))

        for i, file_name in enumerate(file_list):

            raster = Raster(file_name)
            raster.initialize()

            raster_bounds = Vector.get_osgeo_geom(temp_vec.wkt_from_coords(raster.bounds,
                                                                        geom_type='polygon'))
            raster_bounds.CloseRings()

            temp_vec.add_feat(raster_bounds,
                            attr={'filename': Handler(file_name).basename},
                            primary_key=None)
            print(raster)

        print('Total raster count: {}'.format(str(len(file_list))))
        print(temp_vec)

        outfile = outfolder + sep + os.path.basename(rasterfiledir) + '_ras_bounds_{}.shp'.format(str(year))

        temp_vec.write_vector(outfile)
