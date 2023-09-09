#!/bin/bash
#SBATCH --job-name=sum_alb_
#SBATCH --time=3:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=24000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/sum_alb_mosaic_2015_modis_res_tif_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'

datadir='/scratch/rm885/gdrive/sync/decid/decid_tc_albedo_predict_sum/'

# list of input filess
files=(${datadir}decid_tc_2000_layerstack*.tif)
echo 'Found '${#files[*]}' files'

mosaic=$datadir'decid_tc_2000_sum_albedo_modis_res.tif'
compmosaic=$datadir'decid_tc_2000_sum_albedo_modis_res_vis.tif'

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
gdal_merge.py -init 0 -n 0 -o $mosaic -of GTiff -ps 0.0021 0.0021 -ot Float32 ${files[*]}

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $mosaic $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

rm $mosaic

# list of input filess
files=(${datadir}decid_tc_2015_layerstack*.tif)
echo 'Found '${#files[*]}' files'

mosaic=$datadir'decid_tc_2015_sum_albedo_modis_res.tif'
compmosaic=$datadir'decid_tc_2015_sum_albedo_modis_res_vis.tif'

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
gdal_merge.py -init 0 -n 0 -o $mosaic -of GTiff -ps 0.0021 0.0021 -ot Float32 ${files[*]}

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $mosaic $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

rm $mosaic