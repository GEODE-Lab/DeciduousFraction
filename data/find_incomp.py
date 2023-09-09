from modules import *


if __name__ == '__main__':

    chk_file = '/home/rm885/tc_jobstats.txt'
    job_dir = '/scratch/rm885/support/out/slurm-jobs/'
    out_dir = '/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_tc_incomp/'

    file_lines = Handler(chk_file).read_text_by_line()



    job_dict = dict()
    incomp_jobs = list()
    for line in file_lines:
        k, v = line.split(',')
        job_dict[k.strip()] = v.strip()

        if v.strip() == 'TIMEOUT':
            incomp_jobs.append(k.strip())


    print(len(incomp_jobs))

    job_files = Handler(dirname=job_dir).find_all('.out')

    file_list = list()
    for job_file in job_files:
        for incomp_job in incomp_jobs:
            if incomp_job in job_file:
                file_list.append(job_file)

    print('')

    ras_files = list()
    for job_file in file_list:
        file_lines = Handler(job_file).read_text_by_line()
        ras_files.append(file_lines[3].strip())

    print('')
    print(len(ras_files))
    for ras_file in ras_files:
        print(ras_file)





