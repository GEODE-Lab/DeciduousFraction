from modules import *
import pandas as pd
import math
from osgeo import ogr, osr
import json


def remove_nan(elem):
    if not math.isnan(elem):
        return elem


if __name__ == '__main__':

    folder = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/CAN_NFI/Canada_NFI/" + \
            "From_Jackie_11_17_17/Originial_Canada_data/data/"

    domain = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/STUDY_AREA/ABoVE_Study_Domain_original.shp"

    large_tree_file = folder + "Large_trees_sample_Oct_21_2013_new.csv"
    small_tree_file = folder + "Small_trees_sample_Oct_21_2013.csv"
    site_metadata_file = folder + "NFI_plots_sample_site_data_July_26_2013_meta.csv"
    site_bio_file = folder + "Site_biometrics_sample_Oct_21_2013_new.csv"

    out_file = folder + "NFI_plots_sample_site_data_July_26_2013.shp"
    log_file = folder + "NFI_plots_sample_site_data_July_26_2013.log"

    log = Logger('SAMP',
                 filename=log_file)

    log.lprint('Tree sample file 1: {}'.format(Handler(large_tree_file).basename))
    log.lprint('Tree sample file 2: {}'.format(Handler(small_tree_file).basename))
    log.lprint('Site metadata file: {}'.format(Handler(site_metadata_file).basename))
    log.lprint('Site biometrics file: {}'.format(Handler(site_bio_file).basename))
    log.lprint('Output file: {}'.format(Handler(out_file).basename))

    site_data = list(dict(row_obj.items()) for _, row_obj in pd.read_csv(site_metadata_file).iterrows())
    large_tree_data = list(dict(row_obj.items()) for _, row_obj in pd.read_csv(large_tree_file).iterrows())

    small_tree_data = list(dict(row_obj.items()) for _, row_obj in pd.read_csv(small_tree_file).iterrows())
    site_bio_data = list(dict(row_obj.items()) for _, row_obj in pd.read_csv(site_bio_file).iterrows())

    genus_list = sorted(list(set(list(elem['smtree_genus'] for elem in small_tree_data) +
                                 list(elem['lgtree_genus'] for
                                      elem in large_tree_data))))

    species_dict = dict()

    for genus in genus_list:
        specie_list = list()

        for large_tree in large_tree_data:
            if large_tree['lgtree_genus'] == genus:
                specie_list.append(large_tree['lgtree_species'])

        for small_tree in small_tree_data:

            if small_tree['smtree_genus'] == genus:
                specie_list.append(small_tree['smtree_species'])

        if type(genus).__name__ == 'str':
            species_dict[genus] = sorted(list(set(specie_list)))

    genus_list = list()
    for genus, species in species_dict.items():
        genus_list.append((genus, species))

    sorted_genus_list = sorted(genus_list, key=lambda x: x[0])

    genus_class = {  # 1: deciduous, 0: evergreen
                    'ABIE': 0,  # Abies
                    'ACER': 1,  # Acer
                    'ALNU': 1,  # Alnus
                    'AMEL': 1,  # Amelanchier
                    'BETU': 1,  # Betula
                    'CORN': 1,  # Cornus
                    'FRAX': 1,  # Fraxinus
                    'GENC': 0,  # Unknown conifer
                    'GENH': 1,  # Unknown hardwood
                    'JUNI': 0,  # Juniper
                    'LARI': 1,  # Larix
                    'NEMO': 1,  # Nemopanthus
                    'PICE': 0,  # Picea
                    'PINU': 0,  # Pinus
                    'POPU': 1,  # Populus
                    'PRUN': 1,  # Prunus
                    'QUER': 1,  # Quercus
                    'SALI': 1,  # Salix
                    'SHEP': 1,  # Shepherdia
                    'SORB': 1,  # Sorbus
                    'THUJ': 0,  # Thuja
                    'TILI': 1,  # Tilia
                    'TSUG': 0,  # Tsuga
                    'VIBU': 1,  # Viburnum
                 }

    genus_name = {
                    'ABIE': 'Abies',
                    'ACER': 'Acer',
                    'ALNU': 'Alnus',
                    'AMEL': 'Amelanchier',
                    'BETU': 'Betula',
                    'CORN': 'Cornus',
                    'FRAX': 'Fraxinus',
                    'GENC': 'Unknown conifer',
                    'GENH': 'Unknown hardwood',
                    'JUNI': 'Juniper',
                    'LARI': 'Larix',
                    'NEMO': 'Nemopanthus',
                    'PICE': 'Picea',
                    'PINU': 'Pinus',
                    'POPU': 'Populus',
                    'PRUN': 'Prunus',
                    'QUER': 'Quercus',
                    'SALI': 'Salix',
                    'SHEP': 'Shepherdia',
                    'SORB': 'Sorbus',
                    'THUJ': 'Thuja',
                    'TILI': 'Tilia',
                    'TSUG': 'Tsuga',
                    'VIBU': 'Viburnum',
                 }

    genus_types = ['Evergreen', 'Deciduous']

    for sorted_genus in sorted_genus_list:
        if sorted_genus[0] in genus_class:
            log.lprint('Genus: {}, Type: {}'.format(genus_name[sorted_genus[0]],
                                                    genus_types[genus_class[sorted_genus[0]]]))

    projection = 'geographic'

    out_epsg = 4326  # geographic projection

    domain_vec = Vector(filename=domain)

    domain_spref_str = domain_vec.spref_str
    domain_geom = domain_vec.features[0].GetGeometryRef()

    out_spref = osr.SpatialReference()
    res = out_spref.ImportFromEPSG(out_epsg)
    out_spref_str = out_spref.ExportToWkt()

    Vector.reproj_geom(domain_geom,
                       domain_spref_str,
                       out_spref_str)

    nfi_vec = Vector(in_memory=True,
                     primary_key=None,
                     epsg=out_epsg,
                     geom_type=Vector.ogr_geom_type('point'))

    nfi_vec.name = 'nfi_plot_data'

    site_attr = ogr.FieldDefn('site', ogr.OFTString)
    site_attr.SetWidth(32)

    year_attr = ogr.FieldDefn('year', ogr.OFTInteger)
    year_attr.SetWidth(8)

    age_attr = ogr.FieldDefn('age', ogr.OFTInteger)
    age_attr.SetWidth(8)

    decid_attr = ogr.FieldDefn('decid_frac', ogr.OFTReal)
    decid_attr.SetPrecision(5)
    decid_attr.SetWidth(8)

    nfi_vec.layer.CreateField(site_attr)
    nfi_vec.layer.CreateField(year_attr)
    nfi_vec.layer.CreateField(decid_attr)

    nfi_vec.fields = nfi_vec.fields + [site_attr, year_attr, decid_attr, age_attr]

    samp_list = list()
    site_samp_count = 0

    log.lprint('Large tree sample: {}'.format(json.dumps(large_tree_data[0])))
    log.lprint('Small tree sample: {}'.format(json.dumps(small_tree_data[0])))
    log.lprint('Site sample: {}'.format(json.dumps(site_data[0])))
    log.lprint('Site bio sample: {}'.format(json.dumps(site_bio_data[0])))

    for j, site in enumerate(site_data):
        site_id = int(site['Plot'])
        year = int(site['year'])
        coords = (site['Longitude'], site['Latitude'])
        age = int(list(site['site_age'] for site in site_bio_data if int(site['Plot']) == site_id)[0])

        site_tree_list = list()
        for i, tree in enumerate(large_tree_data):
            if int(tree['Plot']) == site_id and tree['lgtree_status'] == 'LS':
                genus = tree['lgtree_genus']

                if genus in genus_class:
                    dbh = tree['dbh']
                    ba = (3.14159/4.0) * (dbh**2)

                    site_tree_list.append({'genus': genus, 'ba': ba})

        nlarge = len(site_tree_list)

        for i, tree in enumerate(small_tree_data):
            if int(tree['Plot']) == site_id and tree['smtree_status'] == 'LS':
                genus = tree['smtree_genus']

                if genus in genus_class:
                    dbh = tree['smtree_dbh']
                    ba = (3.14159 / 4.0) * (dbh ** 2)

                    site_tree_list.append({'genus': genus, 'ba': ba})

        nsmall = len(site_tree_list) - nlarge

        if nlarge < 5:
            if nsmall < 20:
                status = 'Discarded (too few trees)'
            else:
                status = 'Included'
        elif 5 <= nlarge <= 15:
            if nsmall < 10:
                status = 'Discarded (too few trees)'
            else:
                status = 'Included'
        else:
            status = 'Included'

        total_ba = sum(list(tree['ba'] for tree in site_tree_list))
        decid_ba = sum(list(tree['ba'] for tree in site_tree_list if genus_class[tree['genus']] == 1))

        if total_ba > 0.0:
            if status == 'Included':
                decid_frac = decid_ba / total_ba

                geom_wkt = Vector.wkt_from_coords(coords, geom_type='point')
                geom = ogr.CreateGeometryFromWkt(geom_wkt)

                if domain_geom.Intersects(geom):
                    nfi_vec.add_feat(geom,
                                     attr={'site': site_id,
                                           'age': age,
                                           'year': year,
                                           'decid_frac': decid_frac})
                else:
                    status = 'Discarded (outside domain)'

            log.lprint('{} Site {}: {} of {}: Extracted {} large and {} small trees for {}'.format(status,
                                                                                                   str(site_id),
                                                                                                   str(j + 1),
                                                                                                   str(len(site_data)),
                                                                                                   str(nlarge),
                                                                                                   str(nsmall),
                                                                                                   str(year)))

        else:
            log.lprint('Site {}: {} of {}: No trees!'.format(str(site_id),
                                                             str(j + 1),
                                                             str(len(site_data))))

    log.lprint('Total number of sites: {}'.format(str(len(site_data))))
    log.lprint('Total number of included sites: {}'.format(str(nfi_vec.nfeat)))

    log.lprint('Vector: {}'.format(nfi_vec))

    # write vector to shapefile
    nfi_vec.write_vector(outfile=out_file)

    log.lprint('Written file: {}'.format(out_file))
