#!/bin/bash
#SBATCH --job-name=RFP
#SBATCH --time=1:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1024
#SBATCH --partition=all
#SBATCH --array=1-2000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/iter_%A_%a.out
date
python "/home/rm885/projects/decid/src/prepare_rf_models.py" "/scratch/rm885/gdrive/sync/decid/excel/pred_uncert_temp/temp_data_iter_"$SLURM_ARRAY_TASK_ID".csv" "/scratch/rm885/gdrive/sync/decid/excel/pred_uncert_temp/temp_Cdata_iter_"$SLURM_ARRAY_TASK_ID".csv" "/scratch/rm885/gdrive/sync/decid/excel/pred_uncert_out/RF_pred_y_data_"$SLURM_ARRAY_TASK_ID".csv" "/scratch/rm885/gdrive/sync/decid/pypickle"
date
