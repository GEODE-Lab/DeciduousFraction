#!/bin/bash
#SBATCH --job-name=chk_pckl
#SBATCH --time=3:59:59
#SBATCH --ntasks=1
#SBATCH --mem=4000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/chk_pickle_%A.out

date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
pickledir='/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v13h_pickle/'
outfile='/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v13h_3.csv'
cutoff=66.0
compfile=$pickledir'results_summary_v13h.csv'

#make tiles
python "/home/rm885/projects/decid/src/check_model_pickles.py" $pickledir $compfile $outfile $cutoff
echo '-------------------------------------------'
date
