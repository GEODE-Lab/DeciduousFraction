#!/bin/bash
#SBATCH --job-name=gdal_tif
#SBATCH --time=1:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=54000
#SBATCH --array=1-9
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/gdal_tif_slurm_%A_%a.out

#This is a bash script to uncompress GEE output tif files
#Manually substitute number of array jobs in #SBATCH array=1-X  above^
#where X = number of tif files in folder

module load gdal/2.2.1

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/alaska_data/uncert/'
files=(${datadir}*.tif)

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/alaska_data/uncert_uncomp/'

#if output folder doesn't exist
mkdir $outfolder

#what this statement does: for this element in job array, pick filename based on task ID
f=${files[$SLURM_ARRAY_TASK_ID - 1]}
echo $f
#get basename and extension from picked filename
bname=$(basename $f)
extension="${bname##*.}"
filename="${bname%.*}"

#output filename
outf=$outfolder""$filename"_uncomp."$extension
echo $outf

# if output file exists then remove
if [ -f $outf ] ; then
    rm -f $outf
fi

#gdal to uncompress specified filename with given options
gdal_translate -of GTiff -ot BYTE -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co INTERLEAVE=PIXEL -co COMPRESS=NONE $f $outf

