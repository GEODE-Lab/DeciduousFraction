from geosoup import *
import pandas as pd
import math
import numpy as np
from osgeo import ogr
import geopy.distance as dist


def convert_usable(elem):
    if not math.isnan(elem):
        try:
            return int(elem)
        except ValueError:
            try:
                return float(elem)
            except ValueError:
                try:
                    return str(elem)
                except:
                    return ''
    else:
        return ''


if __name__ == '__main__':

    age_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/raw/" +\
               "All_Stands_Transect_age.csv"

    samp_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/raw/" + \
        "Alaska_Biomass_by_Species_1_28_14_data.csv"
    coord_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/raw/" + \
        "All_Stands_Transect_Waypoints_5_16_12_coords.csv"

    out_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects_ba_with_age.shp"
    log_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects_ba_with_age.log"

    age_dicts = Handler(age_file).read_from_csv(return_dicts=True)

    age_dict = dict()
    for temp_dict in age_dicts:
        site = temp_dict['Site'].strip()

        if site not in ('MATDEC', 'UBHW') and 'TKN' not in site:

            out_site = site[:2] + str(temp_dict['Tran'])

        elif 'TKN' in site:
            out_site = site

        else:
            out_site = site + str(temp_dict['Tran'])

        age_dict[out_site] = temp_dict['Age']

    mack_vec = Vector(in_memory=True,
                      primary_key=None,
                      epsg=4326,  # geographic projection
                      geom_type='line')

    mack_vec.name = 'bnz_lter'

    year = 2009

    site_attr = ogr.FieldDefn('site', ogr.OFTString)
    site_attr.SetWidth(32)

    year_attr = ogr.FieldDefn('year', ogr.OFTInteger)
    year_attr.SetWidth(8)

    age_attr = ogr.FieldDefn('age', ogr.OFTInteger)
    age_attr.SetWidth(8)

    decid_attr = ogr.FieldDefn('decid_frac', ogr.OFTReal)
    decid_attr.SetPrecision(5)
    decid_attr.SetWidth(8)

    length_attr = ogr.FieldDefn('length_mts', ogr.OFTReal)
    length_attr.SetPrecision(5)
    length_attr.SetWidth(16)

    mack_vec.layer.CreateField(site_attr)
    mack_vec.layer.CreateField(year_attr)
    mack_vec.layer.CreateField(age_attr)
    mack_vec.layer.CreateField(decid_attr)
    mack_vec.layer.CreateField(length_attr)

    mack_vec.fields = mack_vec.fields + [site_attr, year_attr, age_attr, decid_attr, length_attr]

    log = Logger('SAMP',
                 filename=log_file)

    log.lprint('Sample file: {}'.format(Handler(samp_file).basename))
    log.lprint('Coords file: {}'.format(Handler(coord_file).basename))
    log.lprint('Output file: {}'.format(Handler(out_file).basename))

    samp_data = pd.read_csv(samp_file)
    site_data = pd.read_csv(coord_file)

    # 1-deciduous, 0-evergreen
    specie_class_mack = {'AL': 1,  # Alder
                         'BP': 1,  # Alaskan paper birch
                         'LL': 1,  # Larix
                         'PB': 1,  # Balsam poplar
                         'PG': 0,  # white spruce
                         'PM': 0,  # Black spruce
                         'PT': 1,  # Aspen
                         'SA': 1}  # Willow

    # define lists for column names
    site_headers = ['Site', 'Transect_mark', 'Latitude', 'Longitude', 'Elevation']
    site_id = ['Site', 'Transect']
    specie_headers = ['Spp']
    ba_headers = ['Mean(BA)']

    # define lists for output data
    out_header = ['site', 'year', 'decid_frac', 'length_mts', 'age']

    samp_list = list(dict(row_obj.items()) for _, row_obj in samp_data.iterrows())
    site_list = list(dict(row_obj.items()) for _, row_obj in site_data.iterrows())

    sites = sorted(list(set(list(elem['Site'] for elem in site_list))))

    for i, site in enumerate(sites):
        transect_list = list(site_entry for site_entry in site_list
                             if site_entry['Site'] == site)

        elevation = np.mean(list(entry['Elevation (ft)'] for entry in transect_list))
        indexed_coords = list((elem['Transect_mark'], ('-' + elem['Longitude'][1:], elem['Latitude'][1:]))
                              for elem in transect_list)

        indexed_coords.sort(key=lambda x: x[0])
        sorted_coords = list(elem[1] for elem in indexed_coords)

        first_pt = sorted_coords[0]
        last_pt = sorted_coords[-1]

        length = dist.vincenty(reversed(first_pt), reversed(last_pt)).m

        geom_wkt = Vector.wkt_from_coords(sorted_coords, geom_type='linestring')
        geom = ogr.CreateGeometryFromWkt(geom_wkt)

        specie_frac = dict(list((samp_entry[specie_headers[0]], samp_entry[ba_headers[0]])
                                for samp_entry in samp_list
                                if str(samp_entry['Site']) + str(convert_usable(samp_entry['Transect'])) == site))

        if len(specie_frac) == 0:
            log.lprint('Site {}: {} of {}: No samples found'.format(str(site),
                                                                    str(i + 1),
                                                                    str(len(sites))))
            continue

        decid_ba = sum(list(specie_class_mack[specie]*ba_frac for specie, ba_frac in specie_frac.items()))
        total_ba = sum(list(ba_frac for _, ba_frac in specie_frac.items()))

        decid_frac = decid_ba/total_ba

        if site in age_dict:
            age = age_dict[site]
        else:
            age = 0

        attr = {'site': site,
                'year': year,
                'decid_frac': decid_frac,
                'length_mts': length,
                'age': age}

        mack_vec.add_feat(geom,
                          attr=attr)

        log.lprint('Site {}: {} of {}: Basal area deciduous fraction {}'.format(str(site),
                                                                                str(i + 1),
                                                                                str(len(sites)),
                                                                                str(decid_frac)))

    log.lprint('Total number of sites: {}'.format(len(sites)))
    log.lprint('Total number of samples: {}'.format(str(mack_vec.nfeat)))
    log.lprint('Years: {}'.format(year))

    log.lprint('Vector: {}'.format(mack_vec))

    # write vector to shapefile
    mack_vec.write_vector(outfile=out_file)

    log.lprint('Written file: {}'.format(out_file))
    
    '''
    infile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects_ba_with_age.shp"

    outfile = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/BNZ_LTER/" + \
        "mack_data_transects_ba_with_age_pts.shp"

    vec = Vector(infile)

    print(vec)

    geoms = list(Vector.get_geom_str(Vector.get_osgeo_geom(wkt).Centroid()) for wkt in vec.wktlist)

    vec.wktlist = geoms

    vec.type = OGR_TYPE_DEF['point']

    vec.write_vector(outfile)
    '''
