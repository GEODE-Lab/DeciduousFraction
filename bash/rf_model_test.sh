#!/bin/bash
#SBATCH --job-name=RF_test
#SBATCH --time=1-23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=8000
#SBATCH --partition=all
#SBATCH --array=1-2000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/rf_test_%A_%a.out
date
python "/home/rm885/projects/decid/src/rf_model_test.py" "/scratch/rm885/gdrive/sync/decid/excel/pred_uncert_temp/temp_data_iter_"$SLURM_ARRAY_TASK_ID".csv" "/scratch/rm885/gdrive/sync/decid/excel/pred_uncert_temp/temp_Cdata_iter_"$SLURM_ARRAY_TASK_ID".csv" "rf_test_"$SLURM_ARRAY_TASK_ID "/scratch/rm885/gdrive/sync/decid/rf_test"
date
