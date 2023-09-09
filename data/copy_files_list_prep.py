import os
from geosoup import Handler

if __name__ == '__main__':

    data_folder = ''
    out_folder = ''

    data_files = Handler(dirname=data_folder).find_all('*.tif')

    

    file_uncert = "C:/Users/masse/Downloads/tc_uncert_list.txt"
    file_avail = "C:/Users/masse/Downloads/avail_list.txt"
    out_file = "C:/Users/masse/Downloads/copy_list.txt"

    with open(file_uncert, 'r') as fu:
        filelines_u = fu.readlines()

    with open(file_avail, 'r') as fa:
        filelines_a = fa.readlines()

    filenames_u = [os.path.basename(elem.split(' ')[-1].replace('_uncert', '').strip()) for elem in filelines_u]
    filenames_a = [os.path.basename(elem.split(' ')[-1].strip()) for elem in filelines_a]

    print(filenames_u[:5])
    print(len(filelines_u))
    print('--------')
    print(filenames_a[:5])
    print(len(filenames_a))
    print('--------')

    outnames = [filename+'\n' for filename in filenames_a if filename not in filenames_u]

    print(len(outnames))
    print(outnames[:5])

    with open(out_file, 'w') as fc:
        fc.writelines(outnames)
