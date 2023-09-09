from geosoup import Raster, Vector, Handler, Opt
import sys


if __name__ == '__main__':

    script, ras_file, vec_file, out_file = sys.argv

    Opt.cprint('----------------------------------------------------')

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
            out_attr = vec_obj.attributes[indx].copy()
            out_attr.update({'albedo': geom_dict['values'][0][0]})
            valid_geom_list.append({Vector.wkt_from_coords(geom_dict['coordinates'][0], 'point'):
                                    out_attr})
    Opt.cprint(len(valid_geom_list))
    for elem in valid_geom_list[:5]:
        Opt.cprint(elem)

    attr_def = vec_obj.attr_def.copy()
    attr_def.update({'albedo': 'float'})

    vec = Vector(filename=out_file, name='extracted_samples',
                 spref_str=vec_obj.spref_str, geom_type='point',
                 in_memory=True, attr_def=attr_def)

    for elem in valid_geom_list:
        wkt, attr = list(elem.items())[0]
        vec.add_feat(Vector.get_osgeo_geom(wkt), attr=attr)

    vec.write_vector(out_file)

    print(vec)

    Opt.cprint('----------------------------------------------------')
