#!/bin/bash
#SBATCH --job-name=tce_5k
#SBATCH --time=5-23:59:59
#SBATCH --cpus-per-task=32
#SBATCH --mem=160000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/tc_extract_%A_%a.out

date

nprocs=32
nsamp=1000
datadir="/scratch/rm885/gdrive/sync/decid/tree_cover_hansen_2010/treecover2010/useful_tc2010/"
infile=$datadir"hansen_tc_2010_mosaic_vis.tif"
outfile=$datadir"hansen_tc_2010_mosaic_vis_"$nsamp"_v1.shp"

echo $infile
echo $outfile
echo $nsamp
echo $nprocs

echo '-----------------------------'

#make tiles
python '/home/rm885/projects/decid/src/extract_tc_geom.py' $infile $outfile $nsamp $nprocs

date
