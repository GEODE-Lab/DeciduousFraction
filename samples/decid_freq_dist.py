from geosoup import *
import pandas as pd
import ast
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pylab
import scipy.stats as stats
from osgeo import ogr, osr

plt.rcParams.update({'font.size': 22, 'font.family': 'Times New Roman'})
plt.rcParams['axes.labelweight'] = 'bold'

# print(plt.rcParams.keys())

font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')

# boundary of the region
above_coords = [[-168.83884, 66.60503], [-168.66305, 64.72256], [-166.11423, 63.29787], [-168.83884, 60.31062],
                [-166.02634, 56.92698], [-166.64157, 54.70557], [-164.84625, 54.05535], [-157.94684, 54.69525],
                [-153.64020, 56.21509], [-151.17926, 57.48851], [-149.64118, 58.87838], [-147.67361, 61.37118],
                [-142.04861, 59.70736], [-135.67654, 58.69490], [-130.48731, 55.73262], [-124.82205, 50.42354],
                [-113.70389, 51.06312], [-112.07791, 53.29901], [-109.00174, 53.03557], [-105.16527, 52.53873],
                [-101.13553, 50.36751], [-98.007415, 49.77869], [-96.880859, 48.80976], [-94.983189, 48.94521],
                [-94.851353, 52.79709], [-88.238500, 56.92737], [-91.862463, 57.81702], [-93.775610, 59.60700],
                [-92.984594, 61.25472], [-87.315649, 64.30688], [-80.504125, 66.77919], [-79.976781, 68.59675],
                [-81.426977, 69.84364], [-84.547094, 70.00956], [-87.447485, 69.93430], [-91.094946, 70.77629],
                [-91.798071, 72.17192], [-89.688696, 73.86475], [-89.600805, 74.33426], [-92.940649, 74.61654],
                [-93.380102, 75.58784], [-94.874242, 75.69681], [-95.137914, 75.86949], [-96.719946, 76.56045],
                [-97.598852, 76.81343], [-97.618407, 77.32284], [-99.552001, 78.91297], [-103.94653, 79.75829],
                [-113.79028, 78.81110], [-124.33715, 76.52777], [-128.02856, 71.03224], [-136.99340, 69.67342],
                [-149.64965, 71.03224], [-158.08715, 71.65080],
                [-167.93090, 69.24910]]

above_geom = ogr.CreateGeometryFromWkt('POLYGON((' + ', '.join(list(' '.join(str(coord) for
                                                                             coord in coords)
                                                                    for coords in above_coords)) + '))')
above_geom.CloseRings()
print(above_geom)

folder = "C:/users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/"

file1 = folder + "SAMPLES/BNZ_LTER/mack_data_transects_ba.shp"
file2 = folder + "SAMPLES/CAFI/CAFI_PSP.shp"
file3 = folder + "SAMPLES/" + \
        "CAN_NFI/Canada_NFI/From_Jackie_11_17_17/Originial_Canada_data/data/NFI_plots_sample_site_data_July_26_2013.shp"
file4 = folder + "SAMPLES/CAN_PSP/PSP_data/CAN_PSP_all_v3_above.shp"
file5 = folder + "SAMPLES/NWT/Chronosequence_BA_data_JB.shp"
file6 = folder + "SAMPLES/NWT/NWT_site_tree_data.shp"
file7 = folder + "SAMPLES/CAN_PSP/CAN_PSP_V2.shp"
file8 = folder + "SAMPLES/CAN_PSP/Yukon_PSP.shp"
file9 = folder + "SAMPLES/NWT/NWT_PSP.shp"

year_bins = [(1984, 1997), (1998, 2002), (2003, 2007), (2008, 2012), (2013, 2018)]
year_samp = list(list() for _ in range(len(year_bins)))

year_samp_reduced = list(list() for _ in range(len(year_bins)))

nbins = 100
cutoff = 55  # percentile at which to cutoff the samples in each bin

# filelist = [file5, file6, file9 ]
# filelist = [file1, file2, file3, file5, file6, file7, file8, file9]
filelist = [file1, file3, file4, file5, file6]

vectors = list()
all_attr_list = list()
for filename in filelist:
    vec = Vector(filename=filename)
    vectors.append(vec)
    print(vec)
    for feat in vec.features:
        geom = feat.GetGeometryRef()
        if geom.Intersects(above_geom):
            all_attr_list.append(feat.items())
            print(feat.items())

    # all_attr_list += list(vec_dict for vec_dict in vec.attributes)

sites = list(set(list(attr_dict['site'] for attr_dict in all_attr_list)))

print(len(sites))



print('Total samples: {}'.format(str(len(all_attr_list))))

for attr in all_attr_list:
    for i, years in enumerate(year_bins):
        if years[0] <= attr['year'] <= years[1]:
            year_samp[i].append(attr)

for i, samp_list in enumerate(year_samp):
    site_ids = list(set(list(attr_dict['site'] for attr_dict in samp_list)))
    for site_id in site_ids:
        same_site_samp_list = list(samp for samp in samp_list if samp['site'] == site_id)
        decid_frac = np.median(list(site_samp['decid_frac'] for site_samp in same_site_samp_list))
        year = int(np.median(list(site_samp['year'] for site_samp in same_site_samp_list)))

        year_samp_reduced[i].append({'site': site_id,
                                     'year': year,
                                     'decid_frac': decid_frac})

decid_frac_samp = list()
for sublist in year_samp_reduced:
    for attr in sublist:
        decid_frac_samp.append(attr)

print('Reduced samples: {}'.format(str(len(decid_frac_samp))))

decid_frac_list = list(samp['decid_frac'] for samp in decid_frac_samp)

step = 1.0/float(nbins)
hist, bin_edges = np.histogram(decid_frac_list, bins=nbins)
print(hist)
med = np.ceil(np.percentile(hist, cutoff))

hist_diff = list()
hist_count = list(0 for _ in range(len(hist)))
hist_edges = list()
for i, hist_val in enumerate(hist):
    if hist_val > med:
        hist_diff.append(hist_val-med)
        hist_count[i] = med
    else:
        hist_diff.append(0)
        hist_count[i] = hist_val
    hist_edges.append((bin_edges[i], bin_edges[i+1]))

print('Max bin size: {}'.format(str(med)))

out_decid = list()
decid_count = list(0 for _ in range(len(hist)))
for decid_val in decid_frac_list:
    for i, hist_edge in enumerate(hist_edges):
        if hist_edge[0] <= decid_val <= hist_edge[1]:
            if hist_count[i] >= decid_count[i]:
                out_decid.append(decid_val)
            decid_count[i] += 1

print('Samples after removal: {}'.format(str(len(out_decid))))

resp, fit_stats = stats.probplot(np.array(decid_frac_list),
                                 dist='uniform')

theo_quantiles = list(np.quantile(resp[0], q) for q in Sublist.frange(0.0, 1.0, step))
actual_quantiles = list(np.quantile(resp[1], q) for q in Sublist.frange(0.0, 1.0, step))

print('R-sq before removal: {}'.format(str(fit_stats[2]**2 * 100.0)))

plt.plot(theo_quantiles, actual_quantiles, '.', markersize=15,  markerfacecolor='none', markeredgecolor='#0C92CA')
plt.plot((0.0, 1.0), (0.0, 1.0), '-', color='red')
plt.show()

resp2, fit_stats2 = stats.probplot(np.array(out_decid),
                                   dist='uniform')
theo_quantiles = list(np.quantile(resp2[0], q) for q in Sublist.frange(0.0, 1.0, step))
actual_quantiles = list(np.quantile(resp2[1], q) for q in Sublist.frange(0.0, 1.0, step))

print('R-sq after removal: {}'.format(str(fit_stats2[2]**2 * 100.0)))

plt.plot(theo_quantiles, actual_quantiles, '.', markersize=15,  markerfacecolor='none', markeredgecolor='#0C92CA')
plt.plot((0.0, 1.0), (0.0, 1.0), '-', color='red')
plt.show()


perc_out = 100.0*float(sum(hist_diff))/float(sum(hist))

print('Percentage of samples removed: {} %'.format(str(perc_out)))

# matplotlib histogram
res = plt.hist(decid_frac_list,
               color='#0C92CA',
               edgecolor='black',
               bins=int(nbins))

plt.axhline(med,
            color='black',
            linestyle='dashed',
            linewidth=1)
# Add labels
plt.show()

# matplotlib histogram
res = plt.hist(out_decid,
               color='#0C92CA',
               edgecolor='black',
               bins=int(nbins))
plt.show()
