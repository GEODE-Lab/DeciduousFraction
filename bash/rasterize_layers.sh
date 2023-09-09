#!/bin/bash
#SBATCH --job-name=rast_all
#SBATCH --time=23:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=144000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/rasterize_extent_%A_%a.out

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/shapefiles/above_domain/'

echo $datadir

file1=$datadir'gadm36_CAN_0.shp'
file2=$datadir'gadm36_USA_0.shp'

date
echo $file1
python '/home/rm885/projects/decid/src/rasterize_extent.py' $file1

date
echo $file2
python '/home/rm885/projects/decid/src/rasterize_extent.py' $file2

date