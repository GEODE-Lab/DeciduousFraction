from geosoup import *
from geosoupML import *
import sys
import os
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


"""
This script is used to compile RF model r-squared and RMSE values
for 3d plotting surfaces. Axes: Rmse/Rsq, Trees, Split
"""

if __name__ == '__main__':

    # import file names from commandline args
    # script, param_type, file_dir, summary_file, plot_file = argv

    param_type = 'rsq'
    file_dir = 'D:\\Shared\\Dropbox\\projects\\NAU\\landsat_deciduous\\data\\rf_test'
    summary_file = 'D:\\Shared\\Dropbox\\projects\\NAU\\landsat_deciduous\\data\\summary_{}.csv'.format(param_type)
    plot_file = 'D:\\Shared\\Dropbox\\projects\\NAU\\landsat_deciduous\\data\\plot_summary_{}.png'.format(param_type)

    print('Searching in {} ...'.format(file_dir))
    print('')

    # find all y value files
    filenames = Handler(dirname=file_dir).find_all(param_type + '.csv')

    # number of files
    n = Sublist.list_size(filenames)

    print('{} Files found'.format(n))
    print('')

    row_names = None
    col_names = None
    temp_matrix = None
    # read data
    for i in range(0, n):
        print('Processing file ' + str(i+1) + ': ' + filenames[i])

        temp_data = Samples(csv_file=filenames[i])

        if i == 0:
            row_names = temp_data.extract_column(column_id=0)
            col_names = temp_data.x_name
            temp_data.delete_column(column_id=0)
            temp_matrix = np.array(temp_data.x)

        else:
            temp_data.delete_column(column_id=0)
            temp_matrix = temp_matrix + np.array(temp_data.x)

    temp_matrix = temp_matrix/float(n)

    out_matrix = Samples(x=temp_matrix, x_name=col_names)

    Handler(summary_file).write_numpy_array_to_file(np_array=out_matrix.x,
                                                    rownames=[str(int(name)) for name in row_names['value']],
                                                    colnames=out_matrix.x_name[1:])

    X = [int(x) for x in out_matrix.x_name[1:]]
    Y = [int(name) for name in row_names['value']]
    X, Y = np.meshgrid(X, Y)
    Z = out_matrix.x
    minz = np.matrix(Z).min()
    maxz = np.matrix(Z).max()

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(maxz*1.1, minz*0.9)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.view_init(-135, 40)
    ax.set_xlabel('Split')
    ax.set_ylabel('Trees')
    plt.savefig(plot_file)
