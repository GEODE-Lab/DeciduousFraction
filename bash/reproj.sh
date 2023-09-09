#!/bin/bash
#SBATCH --job-name=reproj
#SBATCH --time=23:59:59
#SBATCH --cpus-per-task=8
#SBATCH --mem=54000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/py_reproj_%j.out

# This is a bash script to reproject tif files
export GDAL_DATA=/home/rm885/path/gdal
# File to reproject
infile='/scratch/rm885/gdrive/sync/decid/NLCD/ak_nlcd_2011_forest_mask_.tif'
outfile='/scratch/rm885/gdrive/sync/decid/NLCD/ak_nlcd_2011_forest_mask_reprojV2.tif'
# Reproject
date

gdalwarp -overwrite -multi $infile $outfile -ot Byte -tr 0.00027 0.00027 -t_srs 'EPSG:4326' -r bilinear -co COMPRESS=LZW -co BIGTIFF=YES -wo WRITE_FLUSH=YES -wo NUM_THREADS=8 -te -179.0 48.5 -128.0 71.0 

gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

date
