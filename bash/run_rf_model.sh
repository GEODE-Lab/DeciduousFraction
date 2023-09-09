#!/bin/bash
#SBATCH --job-name=rfm_2010
#SBATCH --time=15:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=64000
#SBATCH --array=1-840
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/rf_2010_model_slurm_%A_%a.out

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_output/'

#if output folder doesn't exist
# mkdir $outfolder
echo $datadir

FILELIST=(${datadir}*_2005*.tif)
echo ${#FILELIST[*]}

#for this element in job array, pick filename based on task ID
f=${FILELIST[$[SLURM_ARRAY_TASK_ID - 1]]}

echo $f
echo $outfolder

#make tiles
python '/home/rm885/projects/decid/src/run_saved_rf_model.py' $f $outfolder '/scratch/rm885/gdrive/sync/decid/RF_model_pickles/gee_data_cleaning_v28_median2_RF_214_full.pickle'


