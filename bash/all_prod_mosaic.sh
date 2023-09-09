#!/bin/bash
#SBATCH --job-name=allprod_
#SBATCH --time=21:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=96000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/all_prod_mosaic_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/all_product_stack/'
files=(${datadir}*.tif)
echo ${files[*]}

gdal_merge.py -o /scratch/rm885/gdrive/sync/decid/all_product_stack/all_prod_mosaic.tif -of GTiff -ps 0.0021 0.0021 -ot Int16 -co 'COMPRESS=LZW' -co 'BIGTIFF=YES' ${files[*]}
gdaladdo -ro /scratch/rm885/gdrive/sync/decid/all_product_stack/all_prod_mosaic.tif 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW
date
