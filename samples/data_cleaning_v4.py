from geosoup import Vector, Handler, Sublist
from geosoupML import Euclidean
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable


plt.rcParams.update({'font.size': 18, 'font.family': 'Times New Roman'})
plt.rcParams['axes.labelweight'] = 'bold'
font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')

'''
This data cleaning code uses the histogram only of deciduous fraction 
bins to clean samples. The samples have not been used to extract Landsat data yet. 
Once the samples are cleaned they are then be used to extract 
Landsat data from GEE in subsequent codes.
'''


if __name__ == '__main__':

    # static vars--------------------------------------------------------------------------------------------
    version = 9  # version number
    nbins = 100  # number of bins

    cutoff = 66  # percentile at which to cutoff the samples in each bin

    east_west_bounds = "/home/richard/Dropbox/projects/NAU/landsat_deciduous/data/STUDY_AREA/" \
                       "CAN_AK_east_west_boreal.shp"

    boreal_bounds = "/home/richard/Dropbox/projects/NAU/landsat_deciduous/data/STUDY_AREA/boreal/" \
                    "NABoreal_simple_10km_buffer_geo.shp"

    # sample file dirsctory
    samp_dir = "/home/richard/Dropbox/projects/NAU/landsat_deciduous/data/samples/"

    # input files
    infile = samp_dir + "all_samp_pre_v1.csv"
    infile_shp = samp_dir + "all_samp_pre_v1.shp"

    # output files
    outfile = samp_dir + "all_samp_post_v{}.csv".format(version)
    outshpfile = samp_dir + "all_samp_post_v{}.shp".format(version)

    # plot files
    pre_qq_file = samp_dir + 'pre_qq_file_v{}.png'.format(version)
    post_qq_file = samp_dir + 'post_qq_file_v{}.png'.format(version)
    plot_file = samp_dir + 'sample_distribution_plot_v{}.png'.format(version)

    # years bins for samples, based on Landsat data temporal ranges
    year_bins = [(1984, 1997), (1998, 2002), (2003, 2007), (2008, 2012), (2013, 2018)]

    # year samp calculation -----------------------------------------------------------------------------------------
    # read bounds
    boreal_vec = Vector(boreal_bounds)
    boreal_geom = Vector.get_osgeo_geom(boreal_vec.wktlist[0])

    sep_vec = Vector(east_west_bounds)

    # geometries of east and west boreal regions
    sep_geom_west = Vector.get_osgeo_geom(sep_vec.wktlist[0])
    sep_geom_east = Vector.get_osgeo_geom(sep_vec.wktlist[1])

    # area of east and west regions
    area_west = sep_vec.attributes[0]['area']
    area_east = sep_vec.attributes[1]['area']

    # ratio of east and west areas
    area_ratio = area_east/area_west

    # make list of year bins
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

                # add samples to a year-wise list of samples
                year_samp[i].append(elem)

    for year_samp_ in year_samp:
        print(len(year_samp_))

    # iterate thru year list of samples
    for i, samp_list in enumerate(year_samp):
        print('year: {}'.format(str(year_bins[i])))
        samp_count = 0

        # gather all site IDs
        site_ids = list(set(list(attr_dict['site'] for attr_dict in samp_list)))

        # iterate thru sites
        for site_id in site_ids:

            # choose the sites that have the same ID
            same_site_samp_list = list(samp for samp in samp_list if samp['site'] == site_id)

            lat = same_site_samp_list[0]['Latitude']
            lon = same_site_samp_list[0]['Longitude']

            samp_wkt = Vector.wkt_from_coords([lon, lat])
            samp_geom = Vector.get_osgeo_geom(samp_wkt)

            if boreal_geom.Intersects(samp_geom):

                # take mean of decid fraction and year of all samples
                # at the same site that fall in the same year bin
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

    attribute_types = {'site': 'str',
                       'year': 'int',
                       'decid_frac': 'float'}

    wkt_list = list()
    attr_list = list()

    # loop thru decid fraction samples and add to
    # WKT geometry and attributes list
    for i, row in enumerate(decid_frac_samp):
        elem = dict()
        for header in list(attribute_types):
            elem[header] = row[header]

        wkt = Vector.wkt_from_coords([row['longitude'], row['latitude']],
                                     geom_type='point')

        wkt_list.append(wkt)
        attr_list.append(elem)

    # create a Vector object from wktlist
    vector = Vector.vector_from_string(wkt_list,
                                       out_epsg=4326,
                                       vector_type='point',
                                       attributes=attr_list,
                                       attribute_types=attribute_types)

    print(vector)
    vector.write_vector(infile_shp)

    # sample histogram calculation -----------------------------------------------------------------------------

    # extract all decid frac values for calculating histogram
    decid_frac_list = list(samp['decid_frac'] for samp in decid_frac_samp)

    # histogram calculation
    step = 1.0 / float(nbins)
    hist, bin_edges = np.histogram(decid_frac_list, bins=nbins)
    print(hist)

    # calculate the cutoff number per bin
    med = np.ceil(np.percentile(hist, cutoff)).astype(int)
    print('Max bin size: {}'.format(str(med)))

    # calculate number of elements to keep and number to eliminate in each bin
    # calculate histogram bin edges
    hist_diff = list()
    hist_count = list(0 for _ in hist)
    hist_edges = list()
    for i, hist_val in enumerate(hist):
        if hist_val > med:
            hist_diff.append(hist_val - med)
            hist_count[i] = med
        else:
            hist_diff.append(0)
            hist_count[i] = hist_val
        hist_edges.append((bin_edges[i], bin_edges[i + 1]))

    # initialize list of lists for each bin
    binned_decid_dicts = list(list() for _ in hist_edges)
    out_binned_decid_dicts = list(list() for _ in hist_edges)

    # place all samples in their respective bins
    for decid_samp in decid_frac_samp:
        for i, hist_edge in enumerate(hist_edges):
            if i != (len(hist_edges)-1):
                if hist_edge[0] <= decid_samp['decid_frac'] < hist_edge[1]:
                    binned_decid_dicts[i].append(decid_samp)
            else:
                if hist_edge[0] <= decid_samp['decid_frac'] <= hist_edge[1]:
                    binned_decid_dicts[i].append(decid_samp)

    # random selection of samples in bins where count exceeds the bin threshold
    for i, decid_dicts in enumerate(binned_decid_dicts):

        if len(decid_dicts) > hist_count[i]:
            out_binned_decid_dicts[i] = Sublist(decid_dicts).random_selection(hist_count[i])
        else:
            out_binned_decid_dicts[i] = decid_dicts

    print('Samples after bin thresholding: {}'.format(str(sum(hist_count))))

    # flatten the 'by bin' list of lists
    out_decid_frac_samp = list()
    for sublist in out_binned_decid_dicts:
        for elem in sublist:
            lat = elem['latitude']
            lon = elem['longitude']

            wkt = Vector.wkt_from_coords([float(lon), float(lat)], geom_type='point')
            elem['wkt'] = wkt

            out_decid_frac_samp.append(elem)

    # This portion of code calculates the number of samples on each side
    # divider_lon longitude. The aim is to make the samples on the east side
    # equal in number to the samples on the west. The east side samples are
    # vastly large in number and need to be reduced.
    west_count = 0
    east_count = 0
    west_index = list()
    east_index = list()

    # place the samples in appropriate lists based on where they lie
    for i, elem in enumerate(out_decid_frac_samp):
        geom = Vector.get_osgeo_geom(elem['wkt'])

        if geom.Intersects(sep_geom_west):
            west_count += 1
            west_index.append(i)
        elif geom.Intersect(sep_geom_east):
            east_count += 1
            east_index.append(i)
        else:
            print('No intersection with boreal domain for {}'.format(elem['site']))
    
    print('West count:  {}'.format(west_count))
    print('East count:  {}'.format(east_count))

    # if more samples in the east, randomly select same number or a fraction of samples as west
    if east_count > west_count:
        east_index = Sublist(east_index).random_selection(int(west_count * area_ratio))

        print('East count after random selection: {}'.format(str(len(east_index))))

    '''
    # get east samples from the selected random indices
    east_samp = list(out_decid_frac_samp[i] for i in east_index)

    # Remove the east samples that are closer to each other
    # than thresh (default: median value)
    # this is done only for east samples due to
    # proximity/spatial auto-correlation issues
    east_euc = Euclidean(samples=east_samp,
                         names=['longitude', 'latitude'])
    east_euc.calc_dist_matrix()
    east_euc.proximity_filter(thresh=thresh)

    east_samp = east_euc.samples
    east_index = list(range(len(east_samp)))

    print('East count after processing: {}'.format(len(east_index)))
    '''

    indices = east_index + west_index

    wkt_list = list(wkt_list[i] for i in indices)
    attr_list = list(attr_list[i] for i in indices)

    out_decid_frac_samp = list(out_decid_frac_samp[i] for i in indices)

    print('Total count after processing: {}'.format(len(out_decid_frac_samp)))

    out_decid_frac_list = list(samp['decid_frac'] for samp in out_decid_frac_samp)
    # ----------------------

    # find uniform distribution for the given distribution
    resp, fit_stats = stats.probplot(np.array(decid_frac_list),
                                     dist='uniform')

    # calculate quantiles for QQ plot
    theo_quantiles = list(np.quantile(resp[0], q) for q in Sublist.frange(0.0, 1.0, step))
    actual_quantiles = list(np.quantile(resp[1], q) for q in Sublist.frange(0.0, 1.0, step))

    print('R-sq before removal: {}'.format(str(fit_stats[2] ** 2 * 100.0)))
    resp2, fit_stats2 = stats.probplot(np.array(out_decid_frac_list),
                                       dist='uniform')
    theo_quantiles2 = list(np.quantile(resp2[0], q) for q in Sublist.frange(0.0, 1.0, step))
    actual_quantiles2 = list(np.quantile(resp2[1], q) for q in Sublist.frange(0.0, 1.0, step))

    print('R-sq after removal: {}'.format(str(fit_stats2[2] ** 2 * 100.0)))

    # sample distribution plot --------------------------------------------------------------------------------
    fig1, ax1 = plt.subplots()

    ax1.plot(theo_quantiles, actual_quantiles, '.', markersize=15, markerfacecolor='none', markeredgecolor='#0C92CA')
    ax1.plot((0.0, 1.0), (0.0, 1.0), '-', color='red')
    fig1.savefig(samp_dir + '/unitary_pre_qq_plot_v{}.png'.format(version), bbox_inches='tight')

    fig2, ax1 = plt.subplots()

    ax1.plot(theo_quantiles2, actual_quantiles2, '.', markersize=15, markerfacecolor='none', markeredgecolor='#0C92CA')
    ax1.plot((0.0, 1.0), (0.0, 1.0), '-', color='red')
    fig2.savefig(samp_dir + '/unitary_post_qq_plot_v{}.png'.format(version), bbox_inches='tight')

    perc_out = 100.0 * (float(len(decid_frac_list) - len(out_decid_frac_list)) / float(len(decid_frac_list)))

    print('Percentage of samples removed: {} %'.format(str(perc_out)))
    print('Final number of samples: {}'.format(str(len(out_decid_frac_list))))

    fig3, axes = plt.subplots(nrows=1, figsize=(7, 15))

    ax1 = axes
    divider = make_axes_locatable(ax1)
    ax2 = divider.new_vertical(size='25%', pad=0.4)
    fig3.add_axes(ax2)

    # matplotlib histogram
    res1 = ax1.hist(decid_frac_list,
                    color='#0C92CA',
                    edgecolor='black',
                    bins=int(nbins))

    ax1.set_ylim(0, 5000)
    # ax1.tick_params(axis='y', pad=0.2)
    ax1.spines['top'].set_visible(False)

    ax1.axhline(med,
                color='Red',
                linestyle='dashed',
                linewidth=2)

    res2 = ax2.hist(decid_frac_list,
                    color='#0C92CA',
                    edgecolor='black',
                    bins=int(nbins))

    ax2.set_ylim(20000, 21000)
    ax2.tick_params(bottom="off", labelbottom='off')
    ax2.spines['bottom'].set_visible(False)

    # From https://matplotlib.org/examples/pylab_examples/broken_axis.html
    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
    ax2.plot((-d, +d), (-4.0 * d, +4.0 * d), **kwargs)  # top-left diagonal
    ax2.plot((1 - d, 1 + d), (-4.0 * d, +4.0 * d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax1.transAxes)  # switch to the bottom axes
    ax1.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    res3 = ax1.hist(out_decid_frac_list,
                    color='#FFA500',
                    edgecolor='black',
                    bins=int(nbins))

    # save plot
    fig3.savefig(plot_file, bbox_inches='tight')

    out_samp_index = list(range(len(out_decid_frac_samp)))
    np.random.shuffle(out_samp_index)

    out_decid_frac_samp = list(out_decid_frac_samp[i] for i in out_samp_index)

    # write csv file
    Handler.write_to_csv(out_decid_frac_samp,
                         outfile)

    # write shp file ---------------------------------------------------------------------------------
    vector = Vector.vector_from_string(wkt_list,
                                       out_epsg=4326,
                                       vector_type='point',
                                       attributes=attr_list,
                                       attribute_types=attribute_types)

    print(vector)
    vector.write_vector(outshpfile)

    # write shp file: end---------

    print('Done!')
