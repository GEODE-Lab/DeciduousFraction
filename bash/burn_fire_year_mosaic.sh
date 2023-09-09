#!/bin/bash
#SBATCH --job-name=burn_mos
#SBATCH --time=18:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=64000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/burn_top_layer_mosaic_tif_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'


gdal_merge.py -init 0 -n 0 -ot Int16 -co 'COMPRESS=LZW' -co 'BIGTIFF=YES' -o /scratch/rm885/gdrive/sync/decid/shapefiles/boreal/NA_fire_top_layer_year.tif /scratch/rm885/gdrive/sync/decid/shapefiles/boreal/NFDB_poly_20171106_gt500ha_geo_v2.tif /scratch/rm885/gdrive/sync/decid/shapefiles/boreal/FireAreaHistory_1940_2018_v2.tif 

gdaladdo -ro /scratch/rm885/gdrive/sync/decid/shapefiles/boreal/NA_fire_top_layer_year.tif 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES


date
echo 'End -------'
