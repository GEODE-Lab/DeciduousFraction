#!/bin/bash
#SBATCH --job-name=albedo_r
#SBATCH --time=3:30:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=12000
#SBATCH --array=1-12221
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/albedo_reproj_%A_%a.out

date
echo 'Begin!~~~~~~~~~~'
inp_dir='/scratch/rm885/gdrive/albedo/sinusoidal/'
out_dir='/scratch/rm885/gdrive/albedo/geographic/'
end_str='.tif'

#get list of files from teh folder
FILELIST=(${inp_dir}bluesky_albedo_*${end_str})

#what this statement does: for this element in job array, pick filename based on task ID
f=${FILELIST[$SLURM_ARRAY_TASK_ID-1]}

#get basename and extension from picked filename
bname=$(basename $f)

#name of output file
outf=$out_dir''$bname

# spatial reference strings
# MODIS sinusoidal
#print files
echo $f
echo $outf

# reproject to geographic
gdalwarp -dstnodata -9999 -ot Int16 -tr 0.0042 0.0042 -r bilinear -t_srs 'EPSG:4326' -co COMPRESS=LZW $f $outf

echo 'Done!~~~~~~~~~~'
date
