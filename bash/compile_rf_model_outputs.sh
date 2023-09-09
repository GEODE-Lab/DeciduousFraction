#!/bin/bash
#SBATCH --job-name=tau
#SBATCH --time=3:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2048
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/slurm_%j.out
date
echo

python /home/rm885/projects/decid/src/compile_y_param_files.py /scratch/rm885/gdrive/sync/decid/excel/pred_uncert_out/trn /scratch/rm885/gdrive/sync/decid/excel/pred_uncert_out/tau.csv

echo
date
