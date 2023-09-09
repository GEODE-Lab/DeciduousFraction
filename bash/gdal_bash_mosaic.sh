#!/bin/bash
#SBATCH --job-name=gdal_tif
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=54000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_mosaic_tif_%j.out
module purge
module load gdal/2.2.1

# bash script to make mosaics

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/alaska_data/uncert_uncomp/'

# list of input files
files=(${datadir}*.tif)
echo ${files[*]}

mosaic=$datadir'uncert_mosaic.tif'
compmosaic=$datadir'uncert_mosaic_vis.tif'

echo '********************************************************************************************'

echo 'Data folder: '$datadir
echo 'Mosaic: '$mosaic
echo 'Compressed mosaic: '$compmosaic

echo '********************************************************************************************'

# make mosaic
# spatial resolution: 30m
# data type: Byte
# background value: 0
# file format: Geotiff
gdal_merge.py -init 0 -o $mosaic -of GTiff -ps 30 30 -ot Byte ${files[*]}

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $mosaic $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

echo '********************************************************************************************'
echo 'Done!~~~~~~~~~~'
date
