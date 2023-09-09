#!/bin/bash
#SBATCH --job-name=c2015psu
#SBATCH --time=23:59:59
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem=48000


module purge
module load anaconda
module load gdal/2.2.1
date
python /home/rm885/projects/decid/src/composite_albedo_1proc.py /scratch/rm885/gdrive/albedo/geographic /scratch/rm885/gdrive/albedo/composites3 2013 2018 180 240 pctl_90 2
date


