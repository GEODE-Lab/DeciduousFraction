#!/bin/bash
#SBATCH --job-name=albedo_
#SBATCH --time=11:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=48000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/albedo_data_mosaic_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/albedo_data/'
files=(${datadir}*.tif)
echo ${files[*]}

gdal_merge.py -o /scratch/rm885/gdrive/sync/decid/albedo_data/albedo_data_mosaic.tif -of GTiff -ps 0.0021 0.0021 -ot Int16 -co 'COMPRESS=LZW' -co 'BIGTIFF=YES' ${files[*]}

date
