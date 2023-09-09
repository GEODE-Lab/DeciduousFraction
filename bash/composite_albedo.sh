#!/bin/bash
#SBATCH --job-name=compalb3
#SBATCH --time=5-23:59:59
#SBATCH --ntasks=16
#SBATCH --nodes=1
#SBATCH --mem=300000


module purge
module load anaconda
module load gdal/2.2.1
date
python /home/rm885/projects/decid/src/composite_albedo.py /scratch/rm885/gdrive/albedo/geographic /scratch/rm885/gdrive/albedo/composites__ 16
date


