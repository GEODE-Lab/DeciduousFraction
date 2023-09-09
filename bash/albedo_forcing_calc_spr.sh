#!/bin/bash
#SBATCH --job-name=spr00_15
#SBATCH --time=15:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=64000
#SBATCH --array=1-180
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/albedo_calc_spring_2000_2015_%A_%a.out

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/decid_tc_layerstack/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/decid_tc_albedo_predict_spr/'

#if output folder doesn't exist
mkdir $outfolder
echo $datadir

files=(${datadir}*.tif)
echo 'Found '${#files[*]}' files'

#for this element in job array, pick filename based on task ID
f=${files[$[SLURM_ARRAY_TASK_ID - 1]]}

echo $f
echo $outfolder


python '/home/rm885/projects/decid/src/albedo_forcing_calc.py' $f $outfolder '/scratch/rm885/gdrive/sync/decid/excel/RFalbedo_deciduous_fraction_treecover_50000_cutoff_5_deg1_20191115T184820_spring.pickle' 'spr_albedo'

date
