#!/bin/bash
#SBATCH --job-name=RF_comp3
#SBATCH --time=10-13:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=128000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/rf_compilation_%A.out

date
python /home/rm885/projects/decid/src/compile_rf_test_by_param.py 
date
