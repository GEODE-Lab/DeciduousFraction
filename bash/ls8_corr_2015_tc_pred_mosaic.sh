#!/bin/bash
#SBATCH --job-name=ls8_p_tc
#SBATCH --time=18:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=64000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/ls8_corr_tc_pred_mosaic_2015_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'

datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_LS8_corr_tc1/'

# list of input filess
files=(${datadir}ABoVE_median_SR_NDVI_1_2015*prediction.tif ${datadir}ABoVE_median_SR_NDVI_2_2015*prediction.tif ${datadir}ABoVE_median_SR_NDVI_3_2015*prediction.tif ${datadir}ABoVE_median_SR_NDVI_4_2015*prediction.tif ${datadir}ABoVE_median_SR_NDVI_5_2015*prediction.tif ${datadir}ABoVE_median_SR_NDVI_6_2015*prediction.tif)
echo 'Found '${#files[*]}' files'
mosaicsmall=$datadir'ls8_corr_tc_pred_mosaic_small_2015.tif'
mosaic=$datadir'ls8_corr_tc_pred_mosaic_2015.tif'
temp=$datadir'ls8_corr_tc_pred_mosaic_2015_temp.tif'
compmosaic=$datadir'ls8_corr_tc_pred_mosaic_2015_vis.tif'

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
gdal_merge.py -init 0 -n 0 -o $mosaicsmall -co BIGTIFF=YES -of GTiff -ps 0.0084 0.0084 -ot Float32 ${files[*]}
gdal_merge.py -init 0 -n 0 -o $mosaic -co BIGTIFF=YES -of GTiff -ps 0.00027 0.00027 -ot Float32 ${files[*]}
gdal_calc.py -A $mosaic --outfile=$temp --calc="(A*1)*(A>=0) + (A*0)*(A<0)"  --co='BIGTIFF=YES' --type=Byte --NoDataValue=0
# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $temp $compmosaic 

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

outfile_=${compmosaic##*/}

outfile=$datadir${outfile_%.tif}'_250m.tif'
gdalwarp -ot Byte -tr 0.002083333 0.002083333 -t_srs 'EPSG:4326' -r bilinear -co COMPRESS=LZW -co BIGTIFF=YES  $compmosaic $outfile
gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

rm $mosaic
rm $temp
