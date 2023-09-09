#!/bin/bash
#SBATCH --job-name=gdal_tif
#SBATCH --time=1:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=12000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/gdal_tif_slurm_%j.out

#This is a bash script to uncompress GEE output tif files
#Manually substitute number of array jobs in #SBATCH array=1-X  above^
#where X = number of tif files in folder

module load gdal/2.2.1

#input folder that contains tif files, dont forget the '/' at the end
files='/scratch/rm885/gdrive/gdrive/sync/decid/alaska_data/uncert/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/alaska_data/uncert_uncomp/'

#if output folder doesn't exist
mkdir $outfolder

#make filelist array
declare -a FILELIST
for f in $files*; do
   f=$(echo "$f");
   echo $f;
   bname=$(basename $f);
   extension="${bname##*.}";
   filename="${bname%.*}";
   outf=$outfolder""$filename"_uncomp."$extension;
   if [ -f $outf ] ; then
      rm -f $outf;
   fi;
   gdal_translate -of GTiff -ot BYTE -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co INTERLEAVE=PIXEL -co COMPRESS=NONE $f $outf;
done

date
