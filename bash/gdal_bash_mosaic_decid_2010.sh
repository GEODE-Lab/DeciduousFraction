#!/bin/bash
#SBATCH --job-name=gdal_tif
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=400000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_mosaic_tif_%j.out
module purge
module load gdal/2.2.1

# bash script to make mosaics

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/RF_decid_frac_output_tiles/'

files=(${datadir}*ABoVE_img_am_2010*.tif)

mosaic=$datadir'ABoVE_decid_2010_mosaic.tif'
compmosaic=$datadir'ABoVE_decid_2010_mosaic_vis.tif'
compmosaic_byte=$datadir'ABoVE_decid_2010_mosaic_vis_byte.tif'

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
gdal_merge.py -init 0 -o $mosaic -of GTiff -ps 0.000269 0.000269 -n 0.384285 -ot Float32 ${files[*]}

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_calc.py -A $mosaic --outfile=$compmosaic --calc="A*100.0" --NoDataValue=0 --type='Byte' --co='BIGTIFF=YES' --co='COMPRESS=LZW' 

# gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $mosaic $compmosaic
# gdal_translate -of GTiff -co COMPRESS=LZW -a_nodata 0.330400 -co BIGTIFF=YES $mosaic $compmosaic
# gdal_calc.py -A $compmosaic --outfile=$compmosaic_byte --calc="A*100.0" --NoDataValue=0 --type='Byte' --co="COMPRESS=LZW" --co="BIGTIFF=YES" 

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

echo '********************************************************************************************'
echo 'Done!~~~~~~~~~~'
date

