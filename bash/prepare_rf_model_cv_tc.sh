#!/bin/bash
#SBATCH --job-name=rf_v1_tc
#SBATCH --time=23:59:59
#SBATCH --ntasks=24
#SBATCH --nodes=1
#SBATCH --mem=96000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/pypickle_mp_tc_%A.out

date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
pickle_dir='/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_tc_pickle_test_v1_2/'
samp_file='/scratch/rm885/gdrive/sync/decid/SAMPLES/out_tc_2010_samp_v1.csv'
code='v1_2'
n_iter=100
cpus=24
#if output folder doesn't exist
mkdir $pickle_dir

#make model runs
python "/home/rm885/projects/decid/src/prepare_rf_model_cv_tc.py" $samp_file $pickle_dir $code $n_iter $cpus
echo '-------------------------------------------'
date
