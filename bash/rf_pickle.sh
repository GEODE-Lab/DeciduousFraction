#!/bin/bash
#SBATCH --job-name=pckl_mpi
#SBATCH --time=23:59:59
#SBATCH --ntasks=96
#SBATCH --mem=96000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/gdrive/sync/decid/excel/pypickle_mpi_%j.out
module load anaconda
module load intel
date
mpirun -n 96 python "/home/rm885/projects/decid/src/prepare_rf_model_mpi.py" "/scratch/rm885/gdrive/sync/decid/RF_model_pickles/ABoVE_test_V8_L7_all_2010_samp.csv" "/scratch/rm885/gdrive/sync/decid/RF_model_pickles/rf_pickle_v8" "v8"
date
