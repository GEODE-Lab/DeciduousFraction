#!/bin/bash
#SBATCH --job-name=gdal_tile
#SBATCH --time=23:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=15000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/gdal_tile_extent_slurm_%j.out

#This is a bash script to make tiles extents from a folder of tif files

module purge
module load anaconda

#input folder that contains tif files, dont forget the '/' at the end
tiffilesfolder='/scratch/rm885/gdrive/sync/decid/alaska_data/uncomp/'

#boundary file
boundaryfile='/scratch/rm885/gdrive/sync/decid/bounds/alaska_main.shp'

#tile directory
tiledir='/scratch/rm885/gdrive/sync/decid/alaska_data/tiles_bound/'

#output folder, dont forget the '/' at the end
outshpfile='/scratch/rm885/gdrive/sync/decid/alaska_data/tiles_extentV2.shp'

date

#make tiles
python '/home/rm885/projects/decid/get_tile_extents.py' $tiffilesfolder $boundaryfile $tiledir $outshpfile

date
