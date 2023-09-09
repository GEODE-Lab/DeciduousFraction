#!/bin/bash
#SBATCH --job-name=rfm_v13c
#SBATCH --time=1-23:59:59
#SBATCH --ntasks=24
#SBATCH --mem=72000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/pypickle_mp_%A.out

date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
pickle_dir='/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v13c_pickle/'
samp_file='/scratch/rm885/gdrive/sync/decid/SAMPLES/decid_samp_clean_data_v13_corr.csv'
code='v13c'
n_iter=1000
cpus=24
#if output folder doesn't exist
mkdir $pickle_dir

#make model runs
python "/home/rm885/projects/decid/src/prepare_rf_model.py" $samp_file $pickle_dir $code $n_iter $cpus
echo '-------------------------------------------'
date
