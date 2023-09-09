#!/bin/bash
#SBATCH --job-name=fall_15u
#SBATCH --time=18:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=64000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/fall_alb_mosaic_2015_uncert_tif_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'

datadir='/scratch/rm885/gdrive/sync/decid/decid_tc_albedo_predict_fall_uncert/'


# list of input filess
files=(${datadir}decid_tc_2015_layerstack*.tif)
echo 'Found '${#files[*]}' files'

mosaic=$datadir'decid_tc_2015_fall_albedo_uncert.tif'
temp=$datadir'decid_tc_2015_fall_albedo_temp_uncert.tif'
compmosaic=$datadir'decid_tc_2015_fall_albedo_vis_uncert.tif'

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
#gdal_merge.py -init 0 -n 0 -o $mosaic -of GTiff -ps 0.00027 0.00027 -ot Float32 ${files[*]}
gdal_calc.py -A $mosaic --outfile=$temp --calc="(A*100)*(A>=0) + (A*0)*(A<0)" --type=Byte --NoDataValue=0
# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $temp $compmosaic 

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

outfile_=${compmosaic##*/}

outfile=$datadir${outfile_%.tif}'_250m_uncert.tif'
gdalwarp -ot Byte -tr 0.002083333 0.002083333 -t_srs 'EPSG:4326' -r bilinear -co COMPRESS=LZW -co BIGTIFF=YES  $compmosaic $outfile
gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

rm $mosaic
rm $temp


