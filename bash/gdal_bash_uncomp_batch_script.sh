#!/bin/bash
#SBATCH --job-name=uncomp
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=12000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_uncomp_tif_%j.out

# this script is not suitable for large number of files; use job array instead

module load gdal/2.2.1

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/alaska_data/uncert/'

files=(${datadir}*.tif)

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/alaska_data/uncert_uncomp/'

#if output folder doesn't exist
mkdir $outfolder

#make filelist array
for f in ${files[*]}; do
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
