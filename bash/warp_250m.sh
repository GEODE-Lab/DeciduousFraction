#!/bin/bash
#SBATCH --job-name=warp_250
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=128000
#SBATCH --partition=all
#SBATCH --array=1-5
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_warp_%A_%a.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'

datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_output_h/'


FILELIST=(${datadir}*_prediction_vis.tif)
echo ${#FILELIST[*]}

#for this element in job array, pick filename based on task ID
f=${FILELIST[$[SLURM_ARRAY_TASK_ID - 1]]}

echo $f

outfile_=${f##*/}

echo $outfile_

outfile=$datadir${outfile_%.tif}'_modis250.tif'

echo $outfile

gdalwarp -ot Float32 -tr 0.002083333 0.002083333 -t_srs 'EPSG:4326' -r bilinear -srcnodata -9999.0 -dstnodata -9999.0 -co COMPRESS=LZW -co BIGTIFF=YES $f $outfile 

gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW
