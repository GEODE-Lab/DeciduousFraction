#!/bin/bash
#SBATCH --job-name=rfm_v13i
#SBATCH --time=5-23:59:59
#SBATCH --ntasks=72
#SBATCH --mem=192000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/pypickle_mpi_%A.out
module load intel
date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
pickle_dir='/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v13i_pickle/'
samp_file='/scratch/rm885/gdrive/sync/decid/SAMPLES/decid_samp_clean_data_v13_corr.csv'
code='v13i'
n_iter=50000
#if output folder doesn't exist
mkdir $pickle_dir

#make tiles
mpirun -n 72 python "/home/rm885/projects/decid/src/prepare_rf_model_mpi.py" $samp_file $pickle_dir $code $n_iter
echo '-------------------------------------------'
date
