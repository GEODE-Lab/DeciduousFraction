#!/bin/bash
#SBATCH --job-name=probav
#SBATCH --time=9:30:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=48000
#SBATCH --array=1-20
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/probaV_reproj_%A_%a.out

date
echo 'Begin!~~~~~~~~~~'
inp_dir='/scratch/rm885/gdrive/arctic_greening/probav/orig/'
out_dir='/scratch/rm885/gdrive/arctic_greening/probav/reproj/'
cutfile='/scratch/rm885/gdrive/arctic_greening/arctic_oroarctic_laea.shp'
end_str='.tif'

#get list of files from teh folder
FILELIST=(${inp_dir}ProbaV_LC100_epoch2015_global_v2.0.2_*${end_str})

#what this statement does: for this element in job array, pick filename based on task ID
f=${FILELIST[$SLURM_ARRAY_TASK_ID-1]}

#get basename and extension from picked filename
basename=$(basename $f)
bbasename="${basename%_EPSG-4326.*}"

cutfilebasename=$(basename $cutfile)
cutfileextension="${cutfilebasename##*.}"
cutfilelayername="${cutfilebasename%.*}"

#name of output file
outf=$out_dir''$bbasename'_EPSG-3571.tif'

# spatial reference strings
# MODIS sinusoidal
#print files
echo $f
echo $outf
echo $cutfile
echo $cutfilelayername

# reproject to geographic

# gdalwarp -dstnodata 255 -ot Byte -tr 100 100 -r bilinear -t_srs EPSG:3571 \
# -crop_to_cutline -cutline $cutfile -cl $cutfilelayername \
# -co COMPRESS=LZW -co BIGTIFF=YES \
# $f $outf

python /home/rm885/projects/decid/data/reproj_to_laea_clip.py $f $cutfile $out_dir

echo "Done!"
date
