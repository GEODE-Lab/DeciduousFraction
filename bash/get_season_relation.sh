#!/bin/bash
#SBATCH --job-name=bor_chk
#SBATCH --time=23:59:59
#SBATCH --ntasks=1
#SBATCH --mem=16000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/boreal_chk_%A.out

date
echo '-------------------------------------------'
#output folder, dont forget the '/' at the end
inp_dir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_check/data/'
out_dir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_check/bands/'

#if output folder doesn't exist
mkdir $out_dir

#make model runs
python "/home/rm885/projects/decid/src/get_season_relation.py" $inp_dir $out_dir
echo '-------------------------------------------'
date
