#!/bin/bash
#SBATCH --job-name=mos2015
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=128000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/gdal_mosaic_2015_tif_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'

datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_output_h2/'

# list of input filess
files=(${datadir}*_2015-*prediction.tif)
echo 'Found '${#files[*]}' prediction files'

mosaic=$datadir'ABoVE_median_SR_NDVI_boreal_2015_prediction.tif'
temp=$datadir'ABoVE_median_SR_NDVI_boreal_2015_prediction_temp_2.tif'
compmosaic=$datadir'ABoVE_median_SR_NDVI_boreal_2015_prediction_vis_nd_2.tif'

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
gdal_merge.py -init -9999.0 -o $mosaic -of GTiff -ps 0.00027 0.00027 -ot Float32 ${files[*]}

gdal_calc.py -A $mosaic --outfile=$temp --calc="(A*100)*(A>=0) + (A*0 + 255)*(A<0)" --type=Byte --NoDataValue=255

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $temp $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

outfile_=${compmosaic##*/}

outfile=$datadir${outfile_%.tif}'_250m.tif'
gdalwarp -ot Byte -tr 0.002083333 0.002083333 -t_srs 'EPSG:4326' -r bilinear -srcnodata 255 -dstnodata 255 -co COMPRESS=LZW -co BIGTIFF=YES 
gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

#rm $mosaic
rm $temp

# list of input filess
files=(${datadir}*_2015-*uncertainty.tif)
echo 'Found '${#files[*]}' uncertainty files'

mosaic=$datadir'ABoVE_median_SR_NDVI_boreal_2015_uncertainty.tif'
temp=$datadir'ABoVE_median_SR_NDVI_boreal_2015_uncertainty_temp_2.tif'
compmosaic=$datadir'ABoVE_median_SR_NDVI_boreal_2015_uncertainty_vis_nd_2.tif'

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
# gdal_merge.py -init -9999.0 -o $mosaic -of GTiff -ps 0.00027 0.00027 -ot Float32 ${files[*]}

gdal_calc.py -A $mosaic --outfile=$temp --calc="(A*100)*(A>=0) + (A*0 + 255)*(A<0)" --type=Byte --NoDataValue=255

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $temp $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

outfile_=${compmosaic##*/}

outfile=$datadir${outfile_%.tif}'_250m.tif'
gdalwarp -ot Byte -tr 0.002083333 0.002083333 -t_srs 'EPSG:4326' -r bilinear -srcnodata 255 -dstnodata 255 -co COMPRESS=LZW -co BIGTIFF=YES 
gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

#rm $mosaic
rm $temp