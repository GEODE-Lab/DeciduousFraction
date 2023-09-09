from geosoup import *
import pandas as pd
import math
from osgeo import ogr


def remove_nan(elem):
    if not math.isnan(elem):
        return elem


if __name__ == '__main__':

    samp_file = "c:/users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/CAFI/CAFI_PSP.csv"
    out_file = "c:/users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/CAFI/CAFI_PSP.shp"
    log_file = "c:/users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/CAFI/CAFI_PSP.log"


    cafi_vec = Vector(in_memory=True,
                      primary_key=None,
                      epsg=4326,  # geographic projection
                      geom_type=Vector.ogr_geom_type('point'))

    cafi_vec.name = 'alaska_lakes'

    site_attr = ogr.FieldDefn('site', ogr.OFTString)
    site_attr.SetWidth(32)

    year_attr = ogr.FieldDefn('year', ogr.OFTInteger)
    year_attr.SetWidth(8)

    decid_attr = ogr.FieldDefn('decid_frac', ogr.OFTReal)
    decid_attr.SetPrecision(5)
    decid_attr.SetWidth(8)

    cafi_vec.layer.CreateField(site_attr)
    cafi_vec.layer.CreateField(year_attr)
    cafi_vec.layer.CreateField(decid_attr)

    cafi_vec.fields = cafi_vec.fields + [site_attr, year_attr, decid_attr]

    log = Logger('SAMP',
                 filename=log_file)

    log.lprint('Sample file: {}'.format(Handler(samp_file).basename))
    log.lprint('Output file: {}'.format(Handler(out_file).basename))

    samp_data = pd.read_csv(samp_file)

    # 1-deciduous, 0-evergreen
    specie_id_cafi = {1: 1,  # Alaskan birch
                      2: 1,  # unknown deciduous
                      3: 1,  # Balsam poplar
                      4: 1,  # Quaking aspen
                      5: 0,  # White spruce
                      6: 0,  # Black spruce
                      7: 1,  # Tamarack
                      8: 1,  # Kenai birch
                      9: 0,  # Lodgepole pine
                      10: 0,  # Mountain hemlock
                      12: 0,  # Lutz spruce
                      13: 0,  # Sitka spruce
                      14: 0}  # Western hemlock

    # define lists for column names
    geom_headers = ['Longitude', 'Latitude']
    site_id = ['PSP Number']
    time_headers = ['t0', 't1', 't2', 't3', 't4']
    specie_headers = ['sp1_ID_BA', 'sp2_ID_BA', 'sp3_ID_BA', 'sp4_ID_BA']
    ba_headers = ['sp1_FracBA', 'sp2_FracBA', 'sp3_FracBA', 'sp4_FracBA']

    # define lists for output data
    out_header = ['site', 'year', 'decid_frac']

    samp_list = list()
    year_list = list()

    for index, row_obj in samp_data.iterrows():

        # extract each site as dictionary
        row = dict(row_obj.items())

        # get site name
        site_name = row[site_id[0]]

        site_meas_year = list()
        site_samp_count = 0

        # iterate through each time header
        for time_id in time_headers:

            # get year if available
            year = int(remove_nan(row[time_id])) if remove_nan(row[time_id]) is not None else None

            if year is not None:
                year_list.append(str(year))
                site_meas_year.append(str(year))

                # get all specie IDs measured in that year
                specie_IDs = list(remove_nan(row[col_name + '_{}'.format(time_id)])
                                  for col_name in
                                  specie_headers)

                # classify the IDs
                specie_classes = list(specie_id_cafi[int(specie_ID)] if specie_ID is not None else 0
                                      for specie_ID in specie_IDs)

                # get basal area fractions
                specie_BA_fractions = list(remove_nan(row[col_name + '_{}'.format(time_id)])
                                           for col_name in ba_headers)

                # compute deciduous fraction
                decid_frac = sum(list(specie_BA_fractions[i] if specie_BA_fractions[i] is not None else 0.0
                                      for i, specie_class in enumerate(specie_classes)
                                      if specie_class == 1))

                # create geometry
                geom_str = Vector.wkt_from_coords(row[elem] for elem in geom_headers)

                geom = ogr.CreateGeometryFromWkt(geom_str)

                samp_dict = dict(zip(out_header, [site_name, year, decid_frac]))

                # update vector
                cafi_vec.add_feat(geom=geom,
                                  attr=samp_dict)

                samp_dict.update({'geom': geom_str})

                samp_list.append(samp_dict)

                site_samp_count += 1

        log.lprint('Site {}: {} of {}: Extracted {} samples for {}'.format(str(site_name),
                                                                           str(index+1),
                                                                           str(len(samp_data)),
                                                                           str(site_samp_count),
                                                                           ','.join(site_meas_year)))

    log.lprint('Total number of sites: {}'.format(len(samp_data)))
    log.lprint('Total number of samples: {}'.format(len(samp_list)))
    log.lprint('Years: {}'.format(', '.join(sorted(list(set(year_list))))))

    log.lprint('Vector: {}'.format(cafi_vec))

    # write vector to shapefile
    cafi_vec.write_vector(outfile=out_file)

    log.lprint('Written file: {}'.format(out_file))
