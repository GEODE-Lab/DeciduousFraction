#!/bin/bash
#SBATCH --job-name=rf_v30f
#SBATCH --time=1-23:59:59
#SBATCH --ntasks=24
#SBATCH --nodes=1
#SBATCH --mem=96000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/rf_v30f_md_pypickle_mp_%A.out

date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
pickle_dir='/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v30_md/'
samp_file='/scratch/rm885/gdrive/sync/decid/SAMPLES/gee_samp_extract_postbin_v30_all_md.csv'
code='v30_all_md'
n_iter=10000
cpus=24
#if output folder doesn't exist
mkdir $pickle_dir

#make model runs
python "/home/rm885/projects/decid/src/prepare_rf_model_cv.py" $samp_file $pickle_dir $code $n_iter $cpus
echo '-------------------------------------------'
date
