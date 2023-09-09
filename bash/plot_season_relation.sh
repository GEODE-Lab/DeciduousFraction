#!/bin/bash
#SBATCH --job-name=plot_chk
#SBATCH --time=9:59:59
#SBATCH --ntasks=1
#SBATCH --mem=120000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/plot_boreal_chk_%A.out

date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
inp_dir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_check/bands/'

#make model runs
python "/home/rm885/projects/decid/src/plot_season_relation.py" $inp_dir
echo '-------------------------------------------'
date
