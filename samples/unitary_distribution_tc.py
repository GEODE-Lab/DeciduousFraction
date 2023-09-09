from geosoup import *
from geosoupML import *
import datetime
import random
import numpy as np
import scipy.stats as stats
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import copy
import math


def md_clean(sample_dicts,
             bandnames,
             md_cutoff=95):
    """
    Method to remove outlier samples based on the percentage cutoff provided
    :param sample_dicts: List of sample dictionaries
    :param bandnames: Names of the band to be used as the axes for calculating distance
    :param md_cutoff: Cutoff of the Mahalanobis distance
    :return: List of samples
    """

    if len(sample_dicts) > len(bandnames):

        # initialize mahalanobis class
        md_data = Mahalanobis(samples=sample_dicts,
                              names=bandnames)

        md_data.sample_matrix()
        md_data.cluster_center(method='median')
        md_vec = md_data.calc_distance()

        # eliminate NaNs in Mahalanobis dist vector
        num_list = list(ii for ii, x in enumerate(list(np.isnan(md_vec))) if not x)
        if len(num_list) < 1:
            return sample_dicts

        md_vec = [md_vec[x] for x in num_list]

        # find all MD values that as less than cutoff percentile
        loc = list(ii for ii, x in
                   enumerate(md_vec) if (x <= np.percentile(md_vec, md_cutoff)
                                         and x != np.nan))

        out_samples = list(sample_dicts[ii] for ii in loc)

    else:
        print('Too few samples for cleaning')

        out_samples = sample_dicts

    return out_samples


def reformat_samples(site_dicts):
    """
    Method to reformat samples for use in Mahalanobis distance algo
    :param site_dicts: list of sample dictionaries
                example of a site dict:

    {'1_70066 G000005_1994': {'tc_value': 0.24758,
                              'geom': 'POINT(-121.298569584 55.7763510752)',
                              'site_year': 1994,
                              'data':  {
                                       '262_1993': {'sensor': 'LT05', 'img_year': 1993, 'img_jday': 262,
                                                    'bands': {'blue': 0.0266, 'swir1': 0.0756, 'swir2': 0.0244,
                                                              'green': 0.0481, 'nir': 0.1523, 'red': 0.0344
                                                              }
                                                   },
                                       '263_1984': {'sensor': 'LT05', 'img_year': 1984, 'img_jday': 263,
                                                    'bands': {'blue': 0.0205, 'swir1': 0.0801, 'swir2': 0.0352,
                                                              'green': 0.0516, 'nir': 0.1649, 'red': 0.0491
                                                             }
                                                    }
                                       '264_1984': {'sensor': 'LT05', 'img_year': 1984, 'img_jday': 263,
                                                    'bands': {'blue': 0.0205, 'swir1': 0.0801, 'swir2': 0.0352,
                                                              'green': 0.0516, 'nir': 0.1649, 'red': 0.0491
                                                             }}}}}

    :return: list of dicts
    """

    out_dicts = list()
    for site_elem in site_dicts:
        out_dict = copy.deepcopy(site_elem)
        data = copy.deepcopy(out_dict['data'])
        out_dict.pop('data')

        count = 0
        for samp_dict in data:
            if len(samp_dict) != 0:
                count += 1
                jday_year, samp_data = samp_dict.items()[0]
                temp_elem = dict()
                temp_elem.update(samp_data)
                temp_elem.pop('bands')
                temp_elem.update(samp_data['bands'])

                for key, val in temp_elem.items():
                    key = key + '_' + str(count)
                    out_dict.update({key: val})

        if count == 3:
            out_dicts.append(out_dict)

    return out_dicts


def percentile(inp_list, pctl):
    """
    Find the percentile of a list of values.
    """
    if not inp_list:
        return None

    sorted_arr = sorted(inp_list)
    k = (len(sorted_arr) - 1) * (float(pctl) / 100.0)
    f = int(math.ceil(k))

    return sorted_arr[f]


def mean(inp_list):
    """
    compute mean of list
    :param inp_list: input list
    :return: float
    """
    return np.mean(inp_list)


def ndvi_pctl_composite(site_samp_dict,
                        pctl=75,
                        jday_start=0,
                        jday_end=365):
    """
    Calculate the percentile composite from a list of values in a site dictionary
    :param site_samp_dict: Dictionary of Extracted Landsat values for a site
    :param pctl: Percentile to use for compositing
    :param jday_start: Start julian day for compositing
    :param jday_end: End julian day for compositing
    :return: Dictionary
    """

    ndvi_list = list()
    for ii, data_dict in site_samp_dict.items():
        ndvi = int(normalized_difference(data_dict['bands']['nir'],
                                         data_dict['bands']['red'],
                                         canopy_adj=0.0) * 10000.0)

        if jday_start <= data_dict['img_jday'] <= jday_end:
            ndvi_list.append((data_dict['img_jday'],
                              data_dict['img_year'],
                              ii,
                              ndvi))

    if len(ndvi_list) > 0:
        pctl_th_ndvi = percentile(list(elem[3] for elem in ndvi_list), pctl)
        ii = list(elem[2] for elem in ndvi_list if elem[3] == pctl_th_ndvi)[0]

        out_dict = copy.deepcopy(site_samp_dict[ii])

        out_dict['bands'].update({'ndvi': normalized_difference(out_dict['bands']['nir'],
                                                                out_dict['bands']['red'],
                                                                canopy_adj=0.0)})

        out_dict['bands'].update({'ndwi': normalized_difference(out_dict['bands']['nir'],
                                                                out_dict['bands']['swir2'],
                                                                canopy_adj=0.0)})

        out_dict['bands'].update({'nbr': normalized_difference(out_dict['bands']['nir'],
                                                               out_dict['bands']['swir1'],
                                                               canopy_adj=0.0)})

        out_dict['bands'].update({'savi': normalized_difference(out_dict['bands']['nir'],
                                                                out_dict['bands']['red'],
                                                                canopy_adj=0.5)})

        out_dict['bands'].update({'vari': enhanced_normalized_difference(out_dict['bands']['red'],
                                                                         out_dict['bands']['green'],
                                                                         out_dict['bands']['blue'],
                                                                         canopy_adj=0.0,
                                                                         gain=1.0)})
        return {ii: out_dict}

    else:
        return {}


def normalized_difference(b1,
                          b2,
                          canopy_adj=0.5,
                          adj_index=1.0,
                          additive=0.0):
    """
    Normalized difference between two bands (based on NDVI formula)
    :param b1: First band
    :param b2: Second band
    :param canopy_adj: Adjustment for canopy cover (useful for indices such as SAVi)
    :param adj_index: Adjustment index
    :param additive: Additive
    :return: Float
    """

    if float(b1) + float(b2) + canopy_adj != 0.0:
        return ((1 + canopy_adj ** adj_index) * (float(b1) - float(b2))) / (
                    float(b1) + float(b2) + canopy_adj) + additive
    else:
        return 0.0


def enhanced_normalized_difference(b1,
                                   b2,
                                   b3,
                                   canopy_adj=0.5,
                                   c1=1.0,
                                   c2=1.0,
                                   gain=2.5):
    if (float(b1) + c1 * float(b2) - c2 * float(b3) + canopy_adj) != 0.0:
        return gain * ((float(b1) - float(b2)) / (float(b1) + c1 * float(b2) - c2 * float(b3) + canopy_adj))
    else:
        return 0.0


def correct_landsat_sr(bands_dict,
                       sensor):
    out_dict = dict()
    out_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']

    if sensor == 'LT05' or sensor == 'LE07':

        out_dict['blue'] = float(bands_dict['B1']) / 10000.0
        out_dict['green'] = float(bands_dict['B2']) / 10000.0
        out_dict['red'] = float(bands_dict['B3']) / 10000.0
        out_dict['nir'] = float(bands_dict['B4']) / 10000.0
        out_dict['swir1'] = float(bands_dict['B5']) / 10000.0
        out_dict['swir2'] = float(bands_dict['B7']) / 10000.0

        for band_name in ('slope', 'aspect', 'elevation'):
            if band_name in bands_dict:
                out_dict[band_name] = bands_dict[band_name]

    elif sensor == 'LC08':

        out_dict['blue'] = 0.8850 * (float(bands_dict['B2']) / 10000.0) + 0.0183
        out_dict['green'] = 0.9317 * (float(bands_dict['B3']) / 10000.0) + 0.0123
        out_dict['red'] = 0.9372 * (float(bands_dict['B4']) / 10000.0) + 0.0123
        out_dict['nir'] = 0.8339 * (float(bands_dict['B5']) / 10000.0) + 0.0448
        out_dict['swir1'] = 0.8639 * (float(bands_dict['B6']) / 10000.0) + 0.0306
        out_dict['swir2'] = 0.9165 * (float(bands_dict['B7']) / 10000.0) + 0.0116

        for band_name in ('slope', 'aspect', 'elevation'):
            if band_name in bands_dict:
                out_dict[band_name] = bands_dict[band_name]

    else:
        raise ValueError('Invalid sensor specified')

    return out_dict


def extract_date(string):
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

    '''
    fill_bit = (0,)
    clear_bit = (1,)
    water_bit = (2,)
    cloud_shadow_bit = (3,)
    snow_bit = (4,)
    cloud_bit = (5,)
    cloud_conf_bit = (6, 7)
    cirrus_conf_bit = (8, 9)
    terrain_occlusion = (10,)
    '''

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


def saturated_bands(x, length=8):
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
    lines = Handler(filename).read_from_csv(return_dicts=True)

    # sites = list(set(list(str(line['site']) for line in lines)))
    # print(len(sites))

    site_dict = dict()
    line_counter = 0
    for j, line in enumerate(lines):

        include = True
        for key, val in line.items():
            if type(val).__name__ == 'str':
                if val == 'None':
                    include = False

        if saturated_bands(line['radsat_qa']) \
                or line['GEOMETRIC_RMSE_MODEL'] > 15.0 \
                or unclear_value(line['pixel_qa']):
            include = False

        if include:
            if 'site' not in line:
                line['site'] = '_'.join([str(line['longitude']), str(line['latitude'])])
            if 'year' not in line:
                line['year'] = '2010'

            line_counter += 1
            site_year = str(line['site']) + '_' + str(line['year'])

            if site_year not in site_dict:
                geom_wkt = Vector.wkt_from_coords((line['longitude'], line['latitude']))
                site_dict[site_year] = {'geom': geom_wkt,
                                        'tc_value': line['tc_value'],
                                        'data': dict(),
                                        'site_year': line['year'],
                                        'site': line['site']}

            temp_dict = dict()

            sensor_dict = extract_date(line['LANDSAT_ID'])

            temp_dict['img_jday'] = sensor_dict['date'].timetuple().tm_yday
            temp_dict['img_year'] = sensor_dict['date'].timetuple().tm_year
            temp_dict['sensor'] = sensor_dict['sensor']

            bands = list('B' + str(ii + 1) for ii in range(7)) + ['slope', 'elevation', 'aspect']

            band_dict = dict()
            for band in bands:
                if band in line:
                    band_dict[band] = line[band]

            temp_dict['bands'] = correct_landsat_sr(band_dict,
                                                    sensor_dict['sensor'])

            site_dict[site_year]['data'].update({'{}_{}'.format(str(temp_dict['img_jday']),
                                                                str(temp_dict['img_year'])): temp_dict})

    # print(line_counter)

    return site_dict


if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------

    version = 1

    canopy_adj = 0.5
    additive = 0.25
    adj_idx = 1.0

    # number of bins to divide the 0 - 365 date range into
    year_div = 52

    composite_pctl = 75

    nbins = 50
    cutoff = 60  # percentile per bin at which to cutoff the samples

    # ----------------------------------------------------------------------------------------------------

    s1_jday1 = 90
    s1_jday2 = 165

    s2_jday1 = 180
    s2_jday2 = 240

    s3_jday1 = 255
    s3_jday2 = 330

    md_bandnames = ['savi_1', 'savi_2', 'savi_3']

    plt.rcParams.update({'font.size': 22, 'font.family': 'Times New Roman'})
    plt.rcParams['axes.labelweight'] = 'bold'
    # print(plt.rcParams.keys())

    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')

    # ----------------------------------------------------------------------------------------------------

    # folder = "D:/shared" \
    #         "/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/gee_extract/"

    # datafile = folder + "gee_samp_extract_v2019_01_29T08_06_32.csv"
    # datafile = folder + "gee_samp_extract_short_v2019_03_11T00_35_27.csv"

    # outfile = folder + "gee_data_cleaning_v{}_75pctl.csv".format(str(version))

    tc_dir = 'D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/tree_cover/'
    folder = tc_dir
    outfile = tc_dir + 'out_tc_2010_samp_v{}.csv'.format(version)

    tc_files = ['tree_cover_gee_extract_gee_samp_extract_instance-1_v2019_03_19T08_45_38.csv',
                'tree_cover_gee_extract_gee_samp_extract_instance-2_v2019_03_19T08_42_20.csv',
                'tree_cover_gee_extract_gee_samp_extract_instance-3_v2019_03_19T08_46_46.csv',
                'tree_cover_gee_extract_gee_samp_extract_instance-4_v2019_03_19T08_50_16.csv',
                'tree_cover_gee_extract_gee_samp_extract_instance-5_v2019_03_19T09_04_28.csv']

    all_samp = list()
    for tc_file in tc_files:

        datafile = tc_dir + tc_file

        print(datafile)

        # ----------------------------------------------------------------------------------------------------

        gee_data_dict = read_gee_extract_data(datafile)

        for elem in gee_data_dict.items()[0:10]:
            Opt.cprint(elem)

        '''
        example of a site dict: 

        {'1_70066 G000005_1994': {'tc_value': 24, 
                                  'geom': 'POINT(-121.298569584 55.7763510752)', 
                                  'site_year': 1994,
                                  'data':  {                                       
                                           '262_1993': {'sensor': 'LT05', 'img_year': 1993, 'img_jday': 262,
                                                        'bands': {'blue': 0.0266, 'swir1': 0.0756, 'swir2': 0.0244,
                                                                  'green': 0.0481, 'nir': 0.1523, 'red': 0.0344
                                                                  }
                                                       },
                                           '263_1984': {'sensor': 'LT05', 'img_year': 1984, 'img_jday': 263,
                                                        'bands': {'blue': 0.0205, 'swir1': 0.0801, 'swir2': 0.0352,
                                                                  'green': 0.0516, 'nir': 0.1649, 'red': 0.0491
                                                                 }
                                                        }
                                           '264_1984': {'sensor': 'LT05', 'img_year': 1984, 'img_jday': 263,
                                                        'bands': {'blue': 0.0205, 'swir1': 0.0801, 'swir2': 0.0352,
                                                                  'green': 0.0516, 'nir': 0.1649, 'red': 0.0491
                                                                 }
                                                        }
                                           }
                                 }
        }
        '''

        # ----------------------------------------------------------------------------------------------------
        Opt.cprint('Total number of data points before cleaning : {}'.format(len(gee_data_dict)))

        composite_data_dict = dict()
        total_sites = 0
        for site_index, site_dict in gee_data_dict.items():

            temp_dict = copy.deepcopy(site_dict)
            temp_dict.pop('data')

            temp_dict['data'] = list()

            temp_dict['data'].append(ndvi_pctl_composite(site_dict['data'],
                                                         pctl=composite_pctl,
                                                         jday_start=s1_jday1,
                                                         jday_end=s1_jday2))

            temp_dict['data'].append(ndvi_pctl_composite(site_dict['data'],
                                                         pctl=composite_pctl,
                                                         jday_start=s2_jday1,
                                                         jday_end=s2_jday2))

            temp_dict['data'].append(ndvi_pctl_composite(site_dict['data'],
                                                         pctl=composite_pctl,
                                                         jday_start=s3_jday1,
                                                         jday_end=s3_jday2))

            if len(temp_dict['data']) == 3:
                composite_data_dict.update({site_index: temp_dict})
            total_sites += 1

        Opt.cprint('\n')
        Opt.cprint(
            'After removing samples with less than 3 temporal data points: {}'.format(str(len(composite_data_dict))))

        for elem in composite_data_dict.items()[0:10]:
            Opt.cprint(elem)

        # ----------------------------------------------------------------------------------------------------
        print('Total samples: {}'.format(str(len(composite_data_dict))))

        # append all the samples to one list
        for site_id_year, site_dict in composite_data_dict.items():
            all_samp.append(site_dict)

    print('Total samples before cleaning: {}'.format(str(len(all_samp))))

    # list of deciduous fraction values
    tc_value_list = list(samp['tc_value'] for samp in all_samp)

    # construct a histogram of deciduous fraction values
    step = 1.0 / float(nbins)
    hist, bin_edges = np.histogram(tc_value_list, bins=nbins)
    print(hist)
    med = int(np.ceil(np.percentile(hist, cutoff)))

    # identify lists of number of values above t-he limit,
    # number of allowed values in each bin, and edges of each bin
    hist_diff = list()
    hist_count = list(0 for _ in range(len(hist)))
    hist_edges = list()
    for i, hist_val in enumerate(hist):

        if hist_val > med:
            hist_diff.append(hist_val - med)
            hist_count[i] = med
        else:
            hist_diff.append(0)
            hist_count[i] = int(hist_val)
        hist_edges.append((bin_edges[i], bin_edges[i + 1]))

    print('Max bin size: {}'.format(str(med)))
    print('Total samples after bin cutoff: {}'.format(sum(hist_count)))

    print(hist_count)

    # binning all samples
    decid_samp_list = list(list() for _ in range(len(hist)))  # binned list

    # assign each sample to its bin
    for samp in all_samp:
        for i, hist_edge in enumerate(hist_edges):
            if hist_edge[0] <= samp['tc_value'] < hist_edge[1]:
                decid_samp_list[i].append(samp)
        if samp['tc_value'] == 100:
            decid_samp_list[-1].append(samp)

    print(list(len(elem) for elem in decid_samp_list))

    # randomly select samples in each bin if number of samples in the bin is larger than count
    decid_samp_cut_list = list(random.sample(decid_samp_list[i], count)
                               if count < len(decid_samp_list[i]) else decid_samp_list[i]
                               for i, count in enumerate(hist_count))

    # print number of samples in each bin
    print(list(len(elem) for elem in decid_samp_cut_list))

    # clean all samples using Mahalanobis distance
    # and append all the samples to one list
    all_cut_samp = list()
    samp_id = 1
    for sublist in decid_samp_cut_list:
        formatted_samp = reformat_samples(sublist)

        cleaned_samp_list = md_clean(formatted_samp,
                                     md_bandnames)
        for elem in cleaned_samp_list:
            elem['id'] = samp_id
            all_cut_samp.append(elem)
            samp_id += 1

    out_decid = list(site_samp['tc_value'] for site_samp in all_cut_samp)

    # fint uniform distribution for the given distribution
    resp, fit_stats = stats.probplot(np.array(tc_value_list),
                                     dist='uniform')

    # calculate quantiles for QQ plot
    theo_quantiles = list(np.quantile(resp[0], q) for q in Sublist.frange(0.0, 1.0, step))
    actual_quantiles = list(np.quantile(resp[1], q) for q in Sublist.frange(0.0, 1.0, step))

    print('R-sq before removal: {}'.format(str(fit_stats[2] ** 2 * 100.0)))

    fig1, ax1 = plt.subplots()

    ax1.plot(theo_quantiles, actual_quantiles, '.', markersize=15, markerfacecolor='none', markeredgecolor='#0C92CA')
    ax1.plot((0.0, 1.0), (0.0, 1.0), '-', color='red')
    fig1.savefig(folder + '/unitary_pre_qq_plot_v{}.png'.format(version), bbox_inches='tight')

    resp2, fit_stats2 = stats.probplot(np.array(out_decid),
                                       dist='uniform')
    theo_quantiles = list(np.quantile(resp2[0], q) for q in Sublist.frange(0.0, 1.0, step))
    actual_quantiles = list(np.quantile(resp2[1], q) for q in Sublist.frange(0.0, 1.0, step))

    print('R-sq after removal: {}'.format(str(fit_stats2[2] ** 2 * 100.0)))

    fig2, ax1 = plt.subplots()

    ax1.plot(theo_quantiles, actual_quantiles, '.', markersize=15, markerfacecolor='none', markeredgecolor='#0C92CA')
    ax1.plot((0.0, 1.0), (0.0, 1.0), '-', color='red')
    fig2.savefig(folder + '/unitary_post_qq_plot_v{}.png'.format(version), bbox_inches='tight')

    perc_out = 100.0 * (float(len(tc_value_list) - len(out_decid)) / float(len(tc_value_list)))
    print('Percentage of samples removed: {} %'.format(str(perc_out)))
    print('Final number of samples: {}'.format(str(len(out_decid))))

    fig3, axes = plt.subplots(nrows=1, figsize=(10, 10))

    ax1 = axes
    divider = make_axes_locatable(ax1)
    ax2 = divider.new_vertical(size='50%', pad=0.2)
    fig3.add_axes(ax2)

    # matplotlib histogram
    res1 = ax1.hist(tc_value_list,
                    color='#0C92CA',
                    edgecolor='black',
                    bins=int(nbins))

    ax1.set_ylim(0, 900)
    # ax1.tick_params(axis='y', pad=0.2)
    ax1.spines['top'].set_visible(False)

    ax1.axhline(med,
                color='Red',
                linestyle='dashed',
                linewidth=2)

    res2 = ax2.hist(tc_value_list,
                    color='#0C92CA',
                    edgecolor='black',
                    bins=int(nbins))

    ax2.set_ylim(4195, 4500)
    ax2.tick_params(bottom="off", labelbottom='off')
    ax2.spines['bottom'].set_visible(False)

    # From https://matplotlib.org/examples/pylab_examples/broken_axis.html
    d = .01  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
    ax2.plot((-d, +d), (-2.0 * d, +2.0 * d), **kwargs)  # top-left diagonal
    ax2.plot((1 - d, 1 + d), (-2.0 * d, +2.0 * d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax1.transAxes)  # switch to the bottom axes
    ax1.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    res3 = ax1.hist(out_decid,
                    color='#FFA500',
                    edgecolor='black',
                    bins=int(nbins))

    # save plot
    fig3.savefig(folder + '/sample_distribution_plot_pre_v{}.png'.format(version), bbox_inches='tight')

    '''
    fig4, ax1 = plt.subplots()

    # matplotlib histogram
    res3 = ax1.hist(out_decid,
                    color='#FFA500',
                    edgecolor='black',
                    bins=int(nbins))
    fig4.savefig(folder + '/sample_distribution_plot_post_v{}.png'.format(version), bbox_inches='tight')
    '''

    for samp in all_cut_samp[:10]:
        print(samp)

    Handler.write_to_csv(all_cut_samp,
                         outfile=outfile)
    print('Data written to file: {}'.format(outfile))
