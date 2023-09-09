#!/bin/bash
#SBATCH --job-name=count_
#SBATCH --time=11:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=148000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/albedo_data_mosaic_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_count/'
files=(${datadir}*.tif)
echo ${files[*]}

gdal_merge.py -o /scratch/rm885/gdrive/sync/decid/ABoVE_count/count_data_mosaic.tif -of GTiff -ps 0.00027 0.00027 -ot Int16 -co 'COMPRESS=LZW' -co 'BIGTIFF=YES' ${files[*]}
gdaladdo -ro /scratch/rm885/gdrive/sync/decid/ABoVE_count/count_data_mosaic.tif 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW
date
