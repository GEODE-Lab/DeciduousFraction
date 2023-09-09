from geosoup import *
import pandas as pd
import math
import time
from osgeo import ogr, osr


def convert_usable(elem):
    if not math.isnan(elem):
        try:
            return float(elem)
        except ValueError:
            try:
                return int(elem)
            except ValueError:
                try:
                    return str(elem)
                except:
                    return None
    else:
        return None


if __name__ == '__main__':

    data_folder = "C:/shared/projects/NAU/landsat_deciduous/data/SAMPLES/CAN_PSP/PSP_data/"

    domain = "C:/shared/projects/NAU/landsat_deciduous/data/STUDY_AREA/ABoVE_Study_Domain_original.shp"

    location_file = data_folder + "All_sites_101218.csv"
    ba_fraction_file = data_folder + "PSP_BA_dec_ever_v1.csv"
    survey_dates_file = data_folder + "survey_dates_v1.csv"

    log_file = data_folder + "CAN_PSP_all_v3_above.log"
    out_csv = data_folder + "CAN_PSP_all_v3_above.csv"
    out_shp = data_folder + "CAN_PSP_all_v3_above.shp"

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

    psp_vec = Vector(in_memory=True,
                     primary_key=None,
                     epsg=out_epsg,
                     geom_type=Vector.ogr_geom_type('point'))

    psp_vec.name = 'can_ak_psp'

    site_attr = ogr.FieldDefn('site', ogr.OFTString)
    site_attr.SetWidth(32)

    year_attr = ogr.FieldDefn('year', ogr.OFTInteger)
    year_attr.SetWidth(8)

    decid_attr = ogr.FieldDefn('decid_frac', ogr.OFTReal)
    decid_attr.SetPrecision(5)
    decid_attr.SetWidth(8)

    psp_vec.layer.CreateField(site_attr)
    psp_vec.layer.CreateField(year_attr)

    psp_vec.layer.CreateField(decid_attr)

    psp_vec.fields = psp_vec.fields + [site_attr,
                                       year_attr, decid_attr]

    log = Logger('SAMP',
                 filename=log_file)

    log.lprint('Location file: {}'.format(location_file))
    log.lprint('BA fraction file: {}'.format(ba_fraction_file))
    log.lprint('Dates file: {}'.format(survey_dates_file))
    log.lprint('Output file: {}'.format(out_shp))

    location_data = pd.read_csv(location_file)
    ba_fraction_data = pd.read_csv(ba_fraction_file)
    survey_date_data = pd.read_csv(survey_dates_file)

    location_headers = list(location_data)
    fraction_headers = list(ba_fraction_data)
    survey_headers = list(survey_date_data)

    time_headers = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13']
    decid_headers = ['deciduous_BA', 'evergreen_BA']
    meta_headers = ['site', 'Latitude', 'Longitude']

    site_list = list(dict(row_obj.items()) for _, row_obj in location_data.iterrows())
    samp_list = list(dict(row_obj.items()) for _, row_obj in ba_fraction_data.iterrows())
    date_list = list(dict(row_obj.items()) for _, row_obj in survey_date_data.iterrows())

    nsites = len(site_list)
    results = list()

    log.lprint('Processing {} sites...'.format(str(nsites)))
    print('\nProcessing {} sites...\n'.format(str(nsites)))

    t0 = time.time()

    for i, site_dict in enumerate(site_list):

        meas_count = 0

        samp_loc = list(j for j, samp_dict in enumerate(samp_list) if samp_dict['site'] == site_dict['site'])
        date_loc = list(j for j, date_dict in enumerate(date_list) if date_dict['site'] == site_dict['site'])

        geom = ogr.CreateGeometryFromWkt(Vector.wkt_from_coords((site_dict['Longitude'], site_dict['Latitude']),
                                                                geom_type='point'))

        if geom.Intersects(domain_geom):

            if len(samp_loc) == 1 and len(date_loc) == 1:

                samp_dict = dict(list((k, convert_usable(v)) for k, v in samp_list[samp_loc[0]].items() if k != 'site'))
                date_dict = dict(list((k, convert_usable(v)) for k, v in date_list[date_loc[0]].items() if k != 'site'))

                for time_header in time_headers:
                    site_samp_dict = dict()
                    year = date_dict[time_header]

                    if year is not None:

                        evrgn_ba = samp_dict['evergreen_BA_' + time_header]
                        decid_ba = samp_dict['deciduous_BA_' + time_header]

                        if None not in (evrgn_ba, decid_ba):
                            site_samp_dict['site'] = site_dict['site']
                            site_samp_dict['year'] = int(year)

                            total_ba = (decid_ba+evrgn_ba)

                            if total_ba > 0.0:
                                df = float(decid_ba)/float(total_ba)

                                site_samp_dict['decid_frac'] = df

                                results.append({'attr': site_samp_dict,
                                                'geom': geom})

                                psp_vec.add_feat(geom,
                                                 attr=site_samp_dict)
                                meas_count += 1

        if meas_count > 0:
            log.lprint('{} of {}: Processed : {} with {} data points'.format(str(i + 1),
                                                                             str(nsites),
                                                                             site_dict['site'],
                                                                             str(meas_count)))
        else:
            log.lprint('{} of {}: Failed : {} '.format(str(i + 1),
                                                       str(nsites),
                                                       site_dict['site']))

    t1 = time.time()

    log.lprint('Time taken: {}'.format(Timer.display_time(t1 - t0, precision=0)))
    log.lprint('Final list items: {}'.format(str(len(results))))
    log.lprint(psp_vec)

    print('Time taken: {}'.format(Timer.display_time(t1 - t0, precision=0)))
    print('Final list items: {}'.format(str(len(results))))
    print(psp_vec)

    psp_vec.write_vector(outfile=out_shp)
    log.close()
