#!/bin/bash
#SBATCH --job-name=gdal_tile
#SBATCH --time=23:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=12000
#SBATCH --array=1-132
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/gdal_tile_slurm_%A_%a.out

#This is a bash script to make tiles from uncompressed tif files

module purge
module load python

#input folder that contains tif files, dont forget the '/' at the end
tiffiles='/scratch/rm885/gdrive/sync/decid/alaska_data/uncomp/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/alaska_data/tiles/'

#if output folder doesn't exist
mkdir $outfolder

FILELIST=(${datadir}*.tif)

#what this statement does: for this element in job array, pick filename based on task ID
f=${FILELIST[$SLURM_ARRAY_TASK_ID]}

#get basename and extension from picked filename
bname=$(basename $f)
extension="${bname##*.}"
filename="${bname%.*}"

#print input file
echo $f

# if output file exists then remove
if [ -f $outf ] ; then
    rm -f $outf
fi

#make tiles
python make_tiles.py $f $outfolder 256 256

