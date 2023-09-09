#!/bin/bash
#SBATCH --job-name=tcf
#SBATCH --time=3-23:59:59
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=204800

date

year=2010
echo 'Begin Download!~~~~~~~~~~'

downloaddir='/scratch/rm885/gdrive/sync/decid/tc_files/gz'$year
extractdir='/scratch/rm885/gdrive/sync/decid/tc_files/tif'$year

if [ ! -d $downloaddir ] ; then
	mkdir $downloaddir;
fi

if [ ! -d $extractdir ] ; then
	mkdir $extractdir;
fi
regionfile='/scratch/rm885/gdrive/sync/decid/bounds/above_domain/domain_simple.shp'
wrsfile='/scratch/rm885/gdrive/sync/decid/bounds/wrs2/wrs2_descending.shp'


python '/home/rm885/projects/decid/src/get_tc_tiles.py' $year downloaddir $extractdir $regionfile $wrsfile

echo 'End Download!~~~~~~~~~~'

echo '********************************************************************************************'
echo 'Begin Reprojection!~~~~~~~~~~'

datadir='/scratch/rm885/gdrive/sync/decid/tc_files/tif'$year'/'
outdir='/scratch/rm885/gdrive/sync/decid/tc_files/tif_geo'$year'/'

if [ ! -d $datadir ] ; then
	mkdir $datadir;
fi

if [ ! -d $outdir ] ; then
	mkdir $outdir;
fi

export GDAL_DATA='/home/rm885/path/gdal'

# list of input files
files=(${datadir}*.tif)
echo ${files[*]}

echo '********************************************************************************************'

for f in ${files[*]}; do
   bname=$(basename $f);
   extension="${bname##*.}";
   filename="${bname%.*}";
   outf=$outdir""$filename"_geo."$extension;
   if [ -f $outf ] ; then
      rm -f $outf;
   fi;
   echo 'Reprojecting '$f' to '$outf;
   gdalwarp -overwrite -multi $f $outf -et 0.05 -ot Byte -tr 0.00027 0.00027 -t_srs 'EPSG:4326' -wo WRITE_FLUSH=YES -wo NUM_THREADS=4 ;
done

echo '********************************************************************************************'
echo 'Begin Mosaic!~~~~~~~~~~'


datadir='/scratch/rm885/gdrive/sync/decid/tc_files/tif_geo'$year'/'
outdir='/scratch/rm885/gdrive/sync/decid/tc_files/mosaic'$year'/'

if [ ! -d $datadir ] ; then
	mkdir $datadir;
fi

if [ ! -d $outdir ] ; then
	mkdir $outdir;
fi

mosaic=$outdir'tc_mosaic.tif'
compmosaic=$outdir'tc_mosaic_vis.tif'

files=(${datadir}*.tif)
echo ${files[*]}

echo 'Data folder: '$datadir
echo 'Mosaic: '$mosaic
echo 'Compressed mosaic: '$compmosaic

echo '********************************************************************************************'

# make mosaic
# spatial resolution: 30m
# data type: Byte
# background value: 0
# file format: Geotiff
gdal_merge.py -init 0 -o $mosaic -of GTiff -ps 0.00027 0.00027 -ot Byte ${files[*]}

# compress large tif file using LZW compression
# use BIGTIFF=YES for large files
gdal_translate -of GTiff -co COMPRESS=LZW -co BIGTIFF=YES $mosaic $compmosaic

# make overview (pyramid) file: gdaladdo -> gdal add overview
# this is useful if at any point ArcGIS is going to be used with this data
# this makes pyramids and will save that step with ArcGIS
gdaladdo -ro $compmosaic 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW
echo '********************************************************************************************'
date
