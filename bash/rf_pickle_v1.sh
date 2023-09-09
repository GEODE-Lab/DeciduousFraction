#!/bin/bash
#SBATCH --job-name=pickle1
#SBATCH --time=23:59:59
#SBATCH --cpus-per-task=28
#SBATCH --mem=48000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/gdrive/sync/decid/excel/pypickle_%j.out
module load anaconda
date
python "/home/rm885/projects/decid/src/prepare_rf_model.py" "/scratch/rm885/gdrive/sync/decid/RF_model_pickles/ABoVE_test_V1_all_samp.csv" "/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_test_v1" "v1"
date
