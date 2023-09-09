#!/bin/bash
#SBATCH --job-name=tc_calc
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=50000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_mosaic_tif_%j.out
module purge
module load gdal/2.2.1

# bash script to make mosaics

date

file='/scratch/rm885/hansen_tc_2010/treecover2010/useful_tc2010/hansen_tc_2010_mosaic_vis.tif'
mask='/scratch/rm885/hansen_tc_2010/treecover2010/useful_tc2010/hansen_tc_2010_mosaic_vis_mask0.tif'


gdal_calc.py -A $file --outfile=$mask --calc="A<1" --NoDataValue=0 --type='Byte' --co="COMPRESS=LZW" --co="BIGTIFF=YES" 

gdaladdo -ro $mask 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES


