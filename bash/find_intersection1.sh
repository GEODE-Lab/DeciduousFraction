#!/bin/bash
#SBATCH --job-name=int1
#SBATCH --time=15:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=18000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/intersection1_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'
infile='/scratch/rm885/gdrive/sync/decid/SAMPLES/fire/can_fire/NFDB_poly_20171106_gt500ha_ABoVE_geo_boreal_s1.shp'
outfile='/scratch/rm885/gdrive/sync/decid/SAMPLES/fire/can_fire/NFDB_poly_20171106_gt500ha_s1_multi.shp'

python /home/rm885/projects/decid/src/find_intersecting_geoms.py $infile $outfile

date
