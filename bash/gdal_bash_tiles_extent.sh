#!/bin/bash
#SBATCH --job-name=gdal_tile
#SBATCH --time=5:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=25000
#SBATCH --output=/home/rm885/slurm-jobs/gdal_tile_extent_slurm_%j.out

#This is a bash script to make tiles extents from a folder of tif files

module purge
module load anaconda

#input folder 
tiffilesfolder='/scratch/rm885/hansen_tc_2010/treecover2010/treecover2010_v3'

#boundary file
boundaryfile='/scratch/rm885/gdrive/sync/decid/bounds/above_domain/domain_simple.shp'

#tile directory
tiledir='/scratch/rm885/hansen_tc_2010/treecover2010/useful_tc2010'

#output folder, dont forget the '/' at the end
outshpfile='/scratch/rm885/gdrive/sync/decid/bounds/above_domain/hansen_tc_2010_tiles.shp'

date

#make tiles
python '/home/rm885/projects/decid/src/get_tile_extents.py' $tiffilesfolder $boundaryfile $tiledir $outshpfile

date
