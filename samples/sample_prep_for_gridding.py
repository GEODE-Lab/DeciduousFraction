import numpy as np
import os
import sys
from geosoup import *


if __name__ == '__main__':
   

    # output file dirsctory
    outdir = "/home/richard/data/"

    # input file directory
    infile = outdir + "all_samp_pre_v1.csv"
    ini_outfile = outdir + "all_samp_pre_v1.shp"

    boreal_bounds = outdir + "NABoreal_simple_10km_buffer_geo.shp"

    year_bins = [(1984, 1997), (1998, 2002), (2003, 2007), (2008, 2012), (
        2013, 2018)]

    # script-----------------------------------------------------------------------------------------------

    boreal_vec = Vector(boreal_bounds)

    boreal_geom = Vector.get_osgeo_geom(boreal_vec.wktlist[0])

    year_samp = list(list() for _ in range(len(year_bins)))

    year_samp_reduced = list(list() for _ in range(len(year_bins)))

    # get data and names
    file_data = Handler(infile).read_from_csv(return_dicts=True)
    header = list(file_data[0])

    print('\nTotal samples: {}'.format(str(len(file_data))))

    boreal_samp_count = 0

    # bin all samples based on sample years using year_bins
    for elem in file_data:
        for i, years in enumerate(year_bins):
            if years[0] <= elem['year'] <= years[1]:
                year_samp[i].append(elem)

    # take mean of all samples of the same site that fall in the same year bin
    for i, samp_list in enumerate(year_samp):
        print('year: {}'.format(str(year_bins[i])))
        samp_count = 0
        site_ids = list(set(list(attr_dict['site'] for attr_dict in samp_list)))

        for site_id in site_ids:
            same_site_samp_list = list(samp for samp in samp_list if samp['site'] == site_id)

            lat = same_site_samp_list[0]['Latitude']
            lon = same_site_samp_list[0]['Longitude']

            samp_wkt = Vector.wkt_from_coords([lon, lat])
            samp_geom = Vector.get_osgeo_geom(samp_wkt)

            if boreal_geom.Intersects(samp_geom):

                decid_frac = np.mean(list(site_samp['decid_frac'] for site_samp in same_site_samp_list))
                year = int(np.mean(list(site_samp['year'] for site_samp in same_site_samp_list)))

                # remove spaces in site names,
                # and add year to site name eg: 'site1' + '2007' = 'site1_2007'
                year_samp_reduced[i].append({'site': str(site_id).replace(' ', '') + '_' + str(year),
                                             'year': year,
                                             'decid_frac': decid_frac,
                                             'latitude': lat,
                                             'longitude': lon})
                boreal_samp_count += 1
                samp_count += 1
        print('samp_count: {}'.format(str(samp_count)))

    # flatten the 'by year' list of lists
    decid_frac_samp = list()
    for sublist in year_samp_reduced:
        for elem in sublist:
            decid_frac_samp.append(elem)

    print('Reduced samples: {}'.format(str(len(decid_frac_samp))))

    print(decid_frac_samp[0])

    attribute_types = {'site': 'str',
                       'year': 'int',
                       'decid_frac': 'float'}

    wkt_list = list()
    attr_list = list()

    for i, row in enumerate(decid_frac_samp):
        elem = dict()
        for header in list(attribute_types):
            elem[header] = row[header]

        wkt = Vector.wkt_from_coords([row['longitude'], row['latitude']],
                                     geom_type='point')

        wkt_list.append(wkt)
        attr_list.append(elem)

    vector = Vector.vector_from_string(wkt_list,
                                       out_epsg=4326,
                                       vector_type='point',
                                       attributes=attr_list,
                                       attribute_types=attribute_types,
                                       verbose=True)

    print(vector)
    vector.write_vector(ini_outfile)
    print(ini_outfile)
    
 