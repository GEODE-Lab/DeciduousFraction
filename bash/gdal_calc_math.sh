#!/bin/bash
#SBATCH --job-name=gdal_calc
#SBATCH --time=8:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=6000
#SBATCH --array=1-566
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/rf_model_run_V2_slurm_%A_%a.out

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/rf_tiles_2010_V2/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/rf_tiles_2010_V2_calc/'

#if output folder doesn't exist
mkdir $outfolder

FILELIST=(${datadir}*.tif)

#what this statement does: for this element in job array, pick filename based on task ID
f=${FILELIST[$SLURM_ARRAY_TASK_ID]}

bname=$(basename $f);
extension="${bname##*.}";
filename="${bname%.*}";
tempf=$outfolder""$filename"_temp."$extension;
outf=$outfolder""$filename"_byte."$extension;
if [ -f $outf ] ; then
   rm -f $outf;
fi;

echo $f
echo $outf

gdal_translate -of GTiff -ot Float32 -a_nodata 0.330400 $f $tempf;
gdal_calc.py -A $tempf --outfile=$outf --calc="A*100.0" --NoDataValue=0 --type='Byte'

rm -f tempf

exit 0
