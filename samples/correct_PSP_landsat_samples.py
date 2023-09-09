from geosoup import Handler, Opt
import datetime
import numpy as np


main_attr = ['latitude', 'longitude', 'decid_frac', 'site', 'site_year']
composite_attr = ['img_jday', 'img_year', 'sensor']
topo_attr = ['elevation', 'slope', 'aspect']
band_attr = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'ndvi', 'evi', 'savi']


def normalized_difference(b1,
                          b2,
                          adj=0.0,
                          adj_index=1.0,
                          additive=0.0):
    """
    Normalized difference between two bands (based on NDVI formula)
    :param b1: First band
    :param b2: Second band
    :param adj: Adjustment (useful for indices such as SAVI, as canopy cover adjustment)
    :param adj_index: Adjustment index
    :param additive: Additive
    :return: Float
    """

    if float(b1) + float(b2) + adj != 0.0:
        return ((1 + adj ** adj_index) * (float(b1) - float(b2))) / (float(b1) + float(b2) + adj) + additive
    else:
        return 0.0


def enhanced_normalized_difference(b1,
                                   b2,
                                   b3,
                                   adj=0.0,
                                   c1=1.0,
                                   c2=1.0,
                                   c3=1.0,
                                   gain=0.0):
    """
    Method to calculate enhanced normalized difference between two bands using a third band
    This is equivalent to:
                        GAIN * [(BAND1  -  BAND2)/(BAND1 * COEFF1  +  BAND2 * COEFF1  +  BAND3 * COEFF3 + ADJSTMNT)]

    :param b1: First band
    :param b2: Second Band
    :param b3: Third Band
    :param adj: Adjustment factor
    :param c1: First Coefficient
    :param c2: Second Coefficient
    :param c3: Third Coefficient
    :param gain: Gain value for the index
    :return: Float
    """
    if (c1 * float(b1) + c2 * float(b2) + c3 * float(b3) + adj) != 0.0:
        return gain * ((float(b1) - float(b2)) / (c1 * float(b1) + c2 * float(b2) + c3 * float(b3) + adj))
    else:
        return 0.0


def correct_landsat_sr(bands_dict,
                       sensor,
                       scale=1.0):
    """
    Function to correct reflectance values in the bands_dict to match Landsat 7 output
    Landsat 8 coefficients based on roy et al 2016 DOI: 10.1016/j.rse.2015.12.024
    Landsat 5 coefficients based on sulla-menashe et al 2016 DOI: 10.1016/j.rse.2016.02.041
    :param sensor: Options- LT05, LE07, LC08
    :param bands_dict: Dictionary of band values
    :param scale: Number to scale bands with
    :return: dictionary with keys - 'blue', 'green', 'red', 'nir', 'swir1', 'swir2'
    """

    in_bands = {
        'LT05': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'],
        'LE07': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'],
        'LC08': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'],
    }

    if sensor not in in_bands:
        raise ValueError('Invalid sensor name. Valid names are: landsat_5, landsat_7, landsat_8')

    out_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']

    multi_coeff = {
        'LT05': [0.91996, 0.92764, 0.88810, 0.95057, 0.96525, 0.99601],
        'LE07': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        'LC08': [0.8850, 0.9317, 0.9372, 0.8339, 0.8639, 0.9165]
    }

    add_coeff = {
        'LT05': [0.0037, 0.0084, 0.0098, 0.0038, 0.0029, 0.0020],
        'LE07': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'LC08': [0.0183, 0.0123, 0.0123, 0.0448, 0.0306, 0.0116]
    }

    out_dict = {}
    for ib, in_band in enumerate(in_bands[sensor]):
        out_dict[out_bands[ib]] = (float(bands_dict[in_band]) * scale) * multi_coeff[sensor][ib] + \
                                  add_coeff[sensor][ib]

    for band_name in ('slope', 'aspect', 'elevation'):
        if band_name in bands_dict:
            out_dict[band_name] = bands_dict[band_name]

    return out_dict


def extract_date(string):
    """
    Method to extract dates from a Landsat file name
    :param string: Landsat file name
    :return: Dictionary
    """
    # LT05_L1TP_035020_19960605_20170104_01_T1
    list_str = string.split('_')
    return {
        'sensor': list_str[0],
        'level': list_str[1],
        'pathrow': (int(list_str[2][0:3]), int(list_str[2][3:6])),
        'date': datetime.datetime.strptime(list_str[3], '%Y%m%d')
    }


def unclear_value(x,
                  length=16,
                  only_clear=True,
                  verbose=False):
    """
    Clear value using pixel_qa band
        fill_bit = (0,)
        clear_bit = (1,)
        water_bit = (2,)
        cloud_shadow_bit = (3,)
        snow_bit = (4,)
        cloud_bit = (5,)
        cloud_conf_bit = (6, 7)
        cirrus_conf_bit = (8, 9)
        terrain_occlusion = (10,)

    :param x: pixel_qa band value
    :param length: length of bit string
    :param verbose: if the qa inference should be printed
    :param only_clear: If only pixels with clear tag should be selected
    :return: True if not clear OR False if clear
    """
    try:
        val = int(x)
    except ValueError:
        return True

    bit_str = ''.join(reversed(np.binary_repr(val, length)))
    fill = bit_str[0] == '1'
    clear = bit_str[1] == '1'
    water = bit_str[2] == '1'
    cloud_shadow = bit_str[3] == '1'
    snow = bit_str[4] == '1'
    cloud = bit_str[5] == '1'
    cloud_conf = bit_str[6:8] in ('11', '01')
    cirrus_conf = bit_str[8:10] in ('11', '01')
    terrain_occ = bit_str[10] == '1'
    low_cloud_conf = bit_str[6:8] == '10'
    low_cirrus_conf = bit_str[8:10] == '10'

    clear_condition = [clear, water]
    clear_result = ['clear', 'water']

    unclear_condition = [fill, cloud_shadow, snow, cloud,
                         cloud_conf, cirrus_conf, terrain_occ]
    unclear_result = ['fill', 'cloud_shadow', 'snow', 'cloud',
                      'cloud_conf', 'cirrus_conf', 'terrain_occlusion']

    if only_clear:
        unclear_condition += [low_cloud_conf, low_cirrus_conf]
        unclear_result += ['low_cloud_conf', 'low_cirrus_conf']
    else:
        clear_condition += [low_cloud_conf, low_cirrus_conf]
        clear_result += ['low_cloud_conf', 'low_cirrus_conf']

    if any(clear_condition):
        if verbose:
            print(', '.join(out_result for ii, out_result in
                            enumerate(clear_result) if clear_condition[ii]))
            print(np.binary_repr(int(x), length))
        return False

    elif any(unclear_condition):
        if verbose:
            print(', '.join(out_result for ii, out_result in
                            enumerate(unclear_result) if unclear_condition[ii]))
            print(np.binary_repr(int(x), length))
        return True

    else:
        if verbose:
            print('Out of range')
            print(np.binary_repr(int(x), length))
        return True


def saturated_bands(x, length=16):
    """
    Radiometric saturation
    :param x: pixel value
    :param length: bit length
    :return: 0 if saturated or 1 if clear
    """
    try:
        val = int(x)
    except ValueError:
        return True

    bit_str = ''.join(reversed(np.binary_repr(val, length)))

    if bit_str[0] == '1':
        return True
    else:
        return False


def read_gee_extract_data(filename):
    """
    Method to read sample data in the form of a site dictionary with samples dicts by year
    :param filename: Input data file name
    :return: dict of list of dicts by year
    """

    lines = Handler(filename).read_from_csv(return_dicts=True)

    print(len(lines))

    samp_list = []
    line_counter = 0
    error_counter = 0
    for j, line in enumerate(lines):
        include = True

        try:
            for key, val in line.items():
                if type(val) == str:
                    if val == 'None':
                        include = False

            if saturated_bands(line['radsat_qa']) \
                    or line['GEOMETRIC_RMSE_MODEL'] > 15.0 \
                    or unclear_value(line['pixel_qa']):
                include = False

            if include:
                line_counter += 1

                temp_dict = {'latitude': line['latitude'],
                             'longitude': line['longitude'],
                             'decid_frac': line['decid_frac'],
                             'site_year': line['year'],
                             'site': line['site']}

                sensor_dict = extract_date(line['LANDSAT_ID'])

                temp_dict['img_jday'] = sensor_dict['date'].timetuple().tm_yday
                temp_dict['img_year'] = sensor_dict['date'].timetuple().tm_year
                temp_dict['sensor'] = sensor_dict['sensor']

                bands = list('B' + str(ii + 1) for ii in range(7))

                band_dict = dict()
                for band in bands:
                    if band in line:
                        band_dict[band] = line[band]

                temp2_dict = correct_landsat_sr(band_dict,
                                                sensor_dict['sensor'],
                                                scale=0.0001)

                temp_dict.update(temp2_dict)

                topo_dict = dict(zip(['slope', 'elevation', 'aspect'],
                                     list(line[topo_elem] for topo_elem in ['slope', 'elevation', 'aspect'])))

                temp_dict.update(topo_dict)

                temp_dict.update({'ndvi': normalized_difference(temp_dict['nir'],
                                                                temp_dict['red'])})
                temp_dict.update({'evi': enhanced_normalized_difference(temp_dict['nir'],
                                                                        temp_dict['red'],
                                                                        temp_dict['blue'],
                                                                        gain=2.5,
                                                                        adj=1.0,
                                                                        c2=6.0,
                                                                        c3=-7.5)})
                temp_dict.update({'savi': normalized_difference(temp_dict['nir'],
                                                                temp_dict['red'],
                                                                adj=0.5)})
                samp_list.append(temp_dict)

        except Exception as e:
            print('Error number {} : {}'.format(error_counter, str(e)))
            print(line)
            error_counter += 1
            continue

    print('Total errors in data extraction: {}'.format(str(error_counter)))
    # print(line_counter)

    return samp_list


if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------
    version = 1

    folder = "D:/Shared" \
             "/Dropbox/projects/NAU/landsat_deciduous/data/samples/gee_extract/"

    # datafile = folder + "gee_samp_extract_v2019_01_29T08_06_32.csv"
    # datafile = folder + "gee_samp_extract_postbin_v8_east_2019_08_29T_all.csv"
    datafile = folder + "gee_extract_6_17_2020.csv"

    outfile = folder + "gee_extract_6_17_2020_formatted_ndvi_samples.csv"
    # ----------------------------------------------------------------------------------------------------

    gee_data = read_gee_extract_data(datafile)
    Handler.write_to_csv(gee_data, outfile)
    Opt.cprint('Done!')



