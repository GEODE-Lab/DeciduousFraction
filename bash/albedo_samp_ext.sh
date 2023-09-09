#!/bin/bash
#SBATCH --job-name=alb_samp
#SBATCH --time=3:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=32000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/albedo_samp_extract_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'
python projects/decid/src/extract_ran_samp_albedo.py


date
