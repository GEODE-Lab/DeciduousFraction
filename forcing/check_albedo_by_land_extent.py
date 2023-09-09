from geosoup import Raster, Vector, Handler, Opt
import sys


if __name__ == '__main__':

    # script, ras_file, vec_folder, out_folder = sys.argv

    ras_file = "D:/temp/land_extent_NA_250m.tif"
    vec_folder = "D:/temp/albedo/samples/"
    out_folder = vec_folder

    vec_files = Handler(dirname=vec_folder).find_all('*.shp')

    for filename in vec_files:
        print(filename)

    for vec_file in vec_files:

        Opt.cprint('----------------------------------------------------')
        outfile = out_folder + Handler(Handler(vec_file).add_to_filename('_land')).basename

        ras_obj = Raster(ras_file)
        ras_obj.initialize()

        Opt.cprint(ras_obj)

        vec_obj = Vector(vec_file)

        Opt.cprint(vec_obj)

        geom_extract_list = ras_obj.extract_geom(vec_obj.wktlist,
                                                 geom_ids=list(range(vec_obj.nfeat)),
                                                 pass_pixel_coords=True,
                                                 tile_size=(1024, 1024),
                                                 verbose=True)

        valid_geom_list = []
        for indx, geom_dict in enumerate(geom_extract_list):

            if len(geom_dict['values']) > 0 and geom_dict['values'][0][0] > 0:
                valid_geom_list.append({Vector.wkt_from_coords(geom_dict['coordinates'][0], 'point'):
                                        vec_obj.attributes[indx]})
        print(len(valid_geom_list))
        for elem in valid_geom_list[:5]:
            print(elem)

        vec = Vector(filename=outfile, name='albedo',
                     spref_str=vec_obj.spref_str, geom_type='point',
                     in_memory=True, attr_def={'albedo': 'int'})
        for elem in valid_geom_list:
            wkt, attr = list(elem.items())[0]
            vec.add_feat(Vector.get_osgeo_geom(wkt), attr=attr)

        vec.write_vector(outfile)

        exit()
