# from geosoup import Handler
import sys


if __name__ == '__main__':

    script, job_id, arr_min, arr_max = sys.argv

    chk_str = 'DUE TO TIME LIMIT'
    chk_str2= 'CANCELLED'
    raster_name_marker = 'raster :'

    stdout_folder = '/scratch/rm885/support/out/slurm-jobs/'
    stdout_file_prefix = 'hrf_model_slurm_low_mem_all_tc'
    
    print('Looking into folder : {}\n'.format(stdout_folder))

    terminated_list_file = '/home/rm885/terminated_files_for_{}.txt'.format(job_id)

    stdout_files = [(stdout_folder + stdout_file_prefix + '_{}_{}.out'.format(job_id, ii)) for ii in range(int(arr_min), int(arr_max)+1)]

    counter = 0
    terminated_list = []
    for ii, filename in enumerate(stdout_files):
        with open(filename, 'r') as f:
            filelines = f.readlines()
        
        for fileline in filelines[-5:]:
            if chk_str in fileline or chk_str2 in fileline:
                for fileline2 in filelines[65:85]:
                    if raster_name_marker in fileline2:
                        temp_str = fileline2.split('<raster')[1]
                        raster_name = temp_str.split('of size')[0].strip()
                        
                        terminated_list.append(raster_name)
                        counter +=1 

                        print('{} at {}) Found terminated file: {}'.format(counter, ii+1, raster_name))
                        break

    print('Looked into {} files...'.format(ii))
        
    terminated_list = [filename + '\n' for filename in list(set(terminated_list))]

    with open(terminated_list_file,'w') as tf:
        tf.writelines(terminated_list)

    print('Written file: {}'.format(terminated_list_file))
    
    print('Done~!')
