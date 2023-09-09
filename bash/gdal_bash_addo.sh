#!/bin/bash
#SBATCH --job-name=gdal_tif
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=100000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_addo_%j.out
module purge
module load gdal/2.2.1

# bash script to make mosaics

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/rf_tiles_2010_V2/'

file=$datadir'decid_2010_V3_out_mosaic.tif'

echo '********************************************************************************************'
echo 'file : '$file

echo '********************************************************************************************'

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $file 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

echo '********************************************************************************************'
echo 'Done!~~~~~~~~~~'
date

