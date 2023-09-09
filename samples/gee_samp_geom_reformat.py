from geosoup import Vector, Handler
import json


if __name__ == '__main__':

    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/tc_decid_extract_samp_2000_2005_2010.csv"
    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/tc_decid_extract_samp_2000_2005_2010_wkt.csv"
    shpfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/tc_decid_extract_samp_2000_2005_2010.shp"

    lines = Handler(infile).read_text_by_line()

    headers = lines[0].split(',')
    print(headers)

    useful_headers = ['aspect', 'decid2000', 'decid2000u', 'decid2005', 'decid2005u', 'decid2010', 'decid2010u',
                      'elevation', 'pt_id', 'slope', 'tc2000', 'tc2000u', 'tc2005', 'tc2005u', 'tc2010', 'tc2010u',
                      'geom']

    attr_dict = dict(zip(useful_headers[:-1], list('int' for _ in useful_headers[:-1])))

    headers[-1] = 'geom'

    useful_header_indices = list(headers.index(elem) for elem in useful_headers)

    vec = Vector(filename=shpfile,
                 name='decid_tc_samp',
                 epsg=4326,
                 geom_type='point',
                 verbose=True,
                 primary_key=None,
                 attr_def=attr_dict)

    out_list = []
    for line in lines[1:]:

        elems = line.split(',')
        vals = list(Handler.string_to_type(elem) for elem in elems[:(len(headers)-1)])

        geom_str = ','.join(elems[(len(headers)-1):])
        geom = Vector.get_osgeo_geom(geom_str.replace('""', '"')
                                     .replace('"{', "{")
                                     .replace('}"', "}")
                                     .replace('""', '","'),
                                     geom_type='json')

        vals += [geom.ExportToWkt()]
        print(vals)

        out_vals = list(vals[indx] for indx in useful_header_indices)

        vec.add_feat(geom,
                     primary_key=None,
                     attr=dict(zip(useful_headers[:-1], out_vals[:-1])))

        out_list.append(dict(zip(useful_headers, out_vals)))

    Handler.write_to_csv(out_list, outfile=outfile)

    vec.datasource = None
    print('Outfile: {}'.format(outfile))
    print('Vecfile: {}'.format(shpfile))


