from geosoup import *
import pandas as pd
import math
from osgeo import ogr
import datetime


def remove_nan(elem):
    if not math.isnan(elem):
        return elem


if __name__ == '__main__':

    samp_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/NWT/Chronosequence_BA_data_JB.csv"
    out_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/NWT/Chronosequence_BA_data_JB.shp"
    log_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/NWT/Chronosequence_BA_data_JB.log"

    samp_data = pd.read_csv(samp_file)

    projection = 'geographic'

    headers = list(samp_data)
    for header in headers:
        print(header)

    out_vec = Vector(in_memory=True,
                     primary_key=None,
                     epsg=4326,  # geographic projection
                     geom_type=Vector.ogr_geom_type('point'))

    out_vec.name = 'alaska_lakes'

    site_attr = ogr.FieldDefn('site', ogr.OFTString)
    site_attr.SetWidth(32)

    year_attr = ogr.FieldDefn('year', ogr.OFTInteger)
    year_attr.SetWidth(8)

    age_attr = ogr.FieldDefn('age', ogr.OFTInteger)
    age_attr.SetWidth(8)

    decid_attr = ogr.FieldDefn('decid_frac', ogr.OFTReal)
    decid_attr.SetPrecision(5)
    decid_attr.SetWidth(8)

    out_vec.layer.CreateField(site_attr)
    out_vec.layer.CreateField(year_attr)

    out_vec.layer.CreateField(decid_attr)
    out_vec.layer.CreateField(age_attr)

    out_vec.fields = out_vec.fields + [site_attr, year_attr, decid_attr,
                                       age_attr]

    log = Logger('SAMP',
                 filename=log_file)

    log.lprint('Sample file: {}'.format(Handler(samp_file).basename))
    log.lprint('Output file: {}'.format(Handler(out_file).basename))

    samp_data = pd.read_csv(samp_file)

    # 1-deciduous, 0-evergreen
    specie_id_nwt = {
                        'ba.Alcr': 1,	 # Alnus crispa (alder, shrub)
                        'ba.Bene': 1,    # Betula neoalaskana (alaskan paper birch)
                        'ba.Betsp': 1,	 # Betula (birch)
                        'ba.Lala': 1,	 # Larix laricina (tamarack)
                        'ba.Piba': 0,	 # Pinus banksiana (jack pine)
                        'ba.Picea': 0,	 # Picea (spruce)
                        'ba.Pigl': 0,	 # Picea glauca (white spruce)
                        'ba.Pima': 0,	 # Picea mariana (black spruce)
                        'ba.Poba': 1,	 # Populus balsamifera (cottonwood)
                        'ba.Potr': 1,	 # Populus tremuloides (aspen)
                        'ba.Salix': 1,	 # Salix (willow)
                        'ba.Decid': 1,	 # deciduous tree
                        'ba.Unknown': 2  # trees that could not be determined
                    }

    # define lists for column names
    geom_headers = ['Lat_start', 'Long_start']
    time_headers = ['date', 'age']

    # define lists for output data
    out_header = ['site', 'year', 'decid_frac', 'age']

    samp_list = list()
    site_samp_count = 0

    for index, row_obj in samp_data.iterrows():

        # extract each site as dictionary
        row = dict(row_obj.items())

        # get site name
        site_name = row['plot']

        age = int(row[time_headers[1]]) if not math.isnan(row[time_headers[1]]) else 75

        site_meas_date = datetime.datetime.strptime(row[time_headers[0]], '%m/%d/%Y')
        site_meas_year = site_meas_date.date().year

        total_ba_list = list()
        decid_ba_list = list()

        for key, val in row.items():
            if key in specie_id_nwt:
                sp_class = specie_id_nwt[key]

                if not math.isnan(row[key]):
                    total_ba_list.append(row[key])
                    if sp_class == 1:
                        decid_ba_list.append(row[key])

        decid_ba = sum(decid_ba_list)
        total_ba = sum(total_ba_list)

        decid_frac = decid_ba/total_ba if total_ba != 0.0 else -99.0

        if decid_frac == -99.0:
            log.lprint('Site {}: {} of {}: Failed sample for {}'.format(str(site_name),
                                                                        str(index + 1),
                                                                        str(len(samp_data)),
                                                                        str(site_meas_year)))
            continue

        lat, lon = (row[geom_header] for geom_header in geom_headers)

        geom_wkt = Vector.wkt_from_coords((lon, lat), geom_type='point')
        geom = ogr.CreateGeometryFromWkt(geom_wkt)

        samp_dict = dict(zip(out_header, [site_name, site_meas_year, decid_frac, age]))

        # update vector
        out_vec.add_feat(geom=geom,
                         attr=samp_dict)

        samp_dict.update({'geom': geom_wkt})

        samp_list.append(samp_dict)

        site_samp_count += 1

        log.lprint('Site {}: {} of {}: Extracted sample for {}'.format(str(site_name),
                                                                       str(index+1),
                                                                       str(len(samp_data)),
                                                                       str(site_meas_year)))

    log.lprint('Total number of sites: {}'.format(len(samp_data)))
    log.lprint('Total number of samples: {}'.format(len(samp_list)))

    log.lprint('Vector: {}'.format(out_vec))

    # write vector to shapefile
    out_vec.write_vector(outfile=out_file)

    log.lprint('Written file: {}'.format(out_file))
