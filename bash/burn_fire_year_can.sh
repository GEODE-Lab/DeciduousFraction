#!/bin/bash
#SBATCH --job-name=can_f2
#SBATCH --time=2-23:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=26000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/burn_fire_year_can_2_%A_%a.out

infile="/scratch/rm885/gdrive/sync/decid/shapefiles/boreal/NFDB_poly_20171106_gt500ha_geo_v2.shp"
outfile="/scratch/rm885/gdrive/sync/decid/shapefiles/boreal/NFDB_poly_20171106_gt500ha_geo_v2.tif"

fire_year_col='YEAR'
fire_id_col='FIRE_ID'

python '/home/rm885/projects/decid/src/burn_top_vector.py' $infile $outfile $fire_year_col $fire_id_col

gdaladdo -ro $outfile 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW

date
