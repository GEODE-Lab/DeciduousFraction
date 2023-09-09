from geosoup import *
import numpy as np
import pandas as pd
import math
import copy


samp_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/excel/Yukon_PSP.csv"
out_file = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/excel/Yukon_PSP.shp"

samp_data = pd.read_csv(samp_file)

projection = 'UTM'

headers = list(samp_data)
# for header in headers:
#    print(header)

# 1-deciduous, 0-evergreen
specie_id_yukon = {'Balsam_Poplar': 1,
                   'Black_Spruce': 0,
                   'Hardwood': 1,
                   'Lodgepole_Pine': 0,
                   'Paper_Birch': 1,
                   'Subalpine_Fir': 0,
                   'Trembling_Aspen': 1,
                   'White_Spruce': 0}

meta_headers = ['PSP Number', 'UTM Easting', 'UTM Northing', 'UTM Zone', 'Datum']

time_headers = ['t0', 't1', 't2', 't3', 't4', 't5']

specie_headers = ['sp1_ID_BA_t0', 'sp2_ID_BA_t0', 'sp3_ID_BA_t0', 'sp4_ID_BA_t0',
                  'sp1_ID_BA_t1', 'sp2_ID_BA_t1', 'sp3_ID_BA_t1', 'sp4_ID_BA_t1',
                  'sp1_ID_BA_t2', 'sp2_ID_BA_t2', 'sp3_ID_BA_t2', 'sp4_ID_BA_t2',
                  'sp1_ID_BA_t3', 'sp2_ID_BA_t3', 'sp3_ID_BA_t3', 'sp4_ID_BA_t3',
                  'sp1_ID_BA_t4', 'sp2_ID_BA_t4', 'sp3_ID_BA_t4', 'sp4_ID_BA_t4',
                  'sp1_ID_BA_t5', 'sp2_ID_BA_t5', 'sp3_ID_BA_t5', 'sp4_ID_BA_t5']

ba_headers = ['sp1_FracBA_t0', 'sp2_FracBA_t0', 'sp3_FracBA_t0', 'sp4_FracBA_t0',
              'sp1_FracBA_t1', 'sp2_FracBA_t1', 'sp3_FracBA_t1', 'sp4_FracBA_t1',
              'sp1_FracBA_t2', 'sp2_FracBA_t2', 'sp3_FracBA_t2', 'sp4_FracBA_t2',
              'sp1_FracBA_t3', 'sp2_FracBA_t3', 'sp3_FracBA_t3', 'sp4_FracBA_t3',
              'sp1_FracBA_t4', 'sp2_FracBA_t4', 'sp3_FracBA_t4', 'sp4_FracBA_t4',
              'sp1_FracBA_t5', 'sp2_FracBA_t5',
              'sp3_FracBA_t5',
              'sp4_FracBA_t5']

cols = meta_headers + time_headers + specie_headers + ba_headers

samp_data = samp_data[cols]

specie_mini_headers = ['sp1', 'sp2', 'sp3', 'sp4']
specie_ba_mini_headers = ['sp1_ba', 'sp2_ba', 'sp3_ba', 'sp4_ba']

temp_list = list()

specie_list = list()

for index, row in samp_data.iterrows():

    meta_dict = dict()
    for elem in meta_headers:
            meta_dict[elem] = row[elem]

    for time_stamp in time_headers:
        val_dict = dict()
        frac = 0.0
        if not math.isnan(row[time_stamp]):
            specie_header_list = list(elem for elem in specie_headers if time_stamp in elem)
            specie_ba_header_list = list(elem for elem in ba_headers if time_stamp in elem)

            val_dict['year'] = row[time_stamp]

            for i, specie_header in enumerate(specie_header_list):
                if type(row[specie_header]).__name__ == 'str':

                    #  val_dict[specie_mini_headers[i]] = row[specie_id]
                    #  specie_list.append(row[specie_id])
                    #  val_dict[specie_ba_mini_headers[i]] = row[specie_ba_header_list[i]]
                    frac = frac + float(row[specie_ba_header_list[i]])*float(specie_id_yukon[row[specie_header]])
                else:
                    #  val_dict[specie_mini_headers[i]] = None
                    #  val_dict[specie_ba_mini_headers[i]] = None
                    pass

                val_dict['decid_frac'] = frac

            for key, value in meta_dict.items():
                val_dict[key] = value

            temp_list.append(val_dict)

sort_var = 'decid_frac'
val_list = list(temp[sort_var] for temp in temp_list)
index_list = list(val_tuple[0] for val_tuple in sorted(enumerate(val_list),
                                                       key=lambda x: x[1],
                                                       reverse=True))

# remove nan
data_list = list(temp_list[i] for i in index_list if not np.isnan(temp_list[i]['decid_frac']))

# count zeroes
count_zeros = sum(list(1 for data in data_list if data['decid_frac'] == 0))
count_data = len(data_list)
count_non_zeroes = count_data - count_zeros

percent_zero = 100.0*(float(count_zeros)/float(count_data))
percent_nonzero = 100.0 - percent_zero

print('Percent of list as zero decid fraction: {0:.2f}'.format(percent_zero))
print('Percent of list as non-zero decid fraction: {0:.2f}'.format(percent_nonzero))

retain_zero_percent = 25

if retain_zero_percent <= 0 or retain_zero_percent > percent_zero:
    retain_zero_percent = percent_zero

num_retain = int(np.floor(float(retain_zero_percent*count_non_zeroes)/float(100.0-retain_zero_percent)))
percent_zero_retain = 100.0*(float(num_retain)/float(count_zeros))

data_list0 = list(data for data in data_list if data['decid_frac'] == 0.0)
data_list1 = list(data for data in data_list if data['decid_frac'] != 0.0)

reduced_data_list0 = Sublist(data_list0).remove_by_percent(100-percent_zero_retain)

data_list = None
for data in reduced_data_list0:
    data_list1.append(data)
data_list = copy.deepcopy(data_list1)

# count zeroes
count_zeros = sum(list(1 for data in data_list if data['decid_frac'] == 0.0))
count_data = len(data_list)

print('Percent of list as zero decid fraction: {0:.2f}'.format(100.0*(float(count_zeros)/float(count_data))))

samp_data2 = pd.DataFrame(data_list)

wkt_list = list()
attribute_list = list()
attribute_types = {'decid_frac': 'float',
                   'year':       'int',
                   'PSP Number': 'int'}

for data in data_list:

    if projection == 'UTM':
        spref_str = '+proj=utm +zone={z} +datum={d}'.format(z=data['UTM Zone'],
                                                            d=data['Datum'])

        wkt = Vector.wkt_from_coords((data['UTM Easting'], data['UTM Northing']),
                                     geom_type='point')
    elif projection == 'geographic':
        spref_str = '+proj=longlat +datum={d}'.format(d=data['Datum'])

        wkt = Vector.wkt_from_coords((data['Longitude'], data['Latitude']),
                                     geom_type='point')
    else:
        raise ValueError("No projection type specified")

    vector = Vector.vector_from_string(wkt,
                                       spref_string=spref_str,
                                       spref_string_type='proj4',
                                       vector_type=OGR_TYPE_DEF['point'])
    vector.reproject(epsg=4326)

    wkt_list.append(vector.wktlist[0])

    attribute_list.append({'decid_frac': data['decid_frac'],
                           'year': data['year'],
                           'PSP Number': data['PSP Number']})


vector = Vector.vector_from_string(wkt_list,
                                   out_epsg=4326,
                                   attributes=attribute_list,
                                   attribute_types=attribute_types)

print(vector)

vector.write_to_file(outfile=out_file)
