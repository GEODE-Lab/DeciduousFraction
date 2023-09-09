#!/bin/bash
#SBATCH --job-name=mos2015
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=150000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_mosaic_tif_%j.out
module purge
module load gdal/2.2.1

# bash script to make mosaics

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_count/'


files=(${datadir}*_2015_181_225_18129*.tif)

mosaic=$datadir'ABoVE_count_2015_181_225_18129_mosaic.tif'
compmosaic=$datadir'ABoVE_count_2015_181_225_18129_mosaic_vis.tif'

echo '********************************************************************************************'
echo 'Data folder: '$datadir
echo 'Mosaic: '$mosaic
echo '********************************************************************************************'

# make mosaic
# spatial resolution: 30m
# data type: Byte
# background value: 0
# file format: Geotiff
gdal_merge.py -init 0 -o $mosaic -of GTiff -ps 0.000269 0.000269 -ot Int16 ${files[*]}

# compress large tif file using LZW compression
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $mosaic $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES


echo '********************************************************************************************'
echo 'Done!~~~~~~~~~~'
date

