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
plt.rcParams.update({'font.size': 22, 'font.family': 'Times New Roman'})
plt.rcParams['axes.labelweight'] = 'bold'

print(plt.rcParams.keys())

font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')

file1 = "C:/Users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/TEST_RUNS/samp_runs_100k_jsons.txt"
with open(file1, 'r') as f:
    lines = list(ast.literal_eval(line)
                 for line in f.readlines())

rsq_list = list()
for line in lines:
    rsq_list.append(1.25 * line['rsq'])


# matplotlib histogram
res = plt.hist(rsq_list, color = '#0C92CA', edgecolor = 'black',
         bins = int(30))



# Add labels
plt.show()


