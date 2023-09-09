#!/bin/bash
#SBATCH --job-name=rf_class
#SBATCH --time=1-23:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=64000
#SBATCH --array=1-20
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/run_saved_rf_model_%A_%a.out

#This is a bash script to make tiles from uncompressed tif files
date
echo 'Begin!~~~~~~~~~~'
#input folder that contains tif files, dont forget the '/' at the end
rf_picklefile="/scratch/rm885/gdrive/sync/decid/pypickle/temp_data_iter_335.pickle"

#dir containing rasters, 
datadir="/scratch/rm885/gdrive/sync/decid/alaska_data/uncomp_ph/"

#output prediction directory,
outdir="/scratch/rm885/gdrive/sync/decid/alaska_data/classifV1_ph"

#make filelist array
files=(${datadir}*.tif)

#what this statement does: for this element in job array, pick filename based on task ID
inraster=${files[$SLURM_ARRAY_TASK_ID - 1]}

echo '********************************************************************************************'

echo 'Random Forest file: '$rf_picklefile
echo 'Inraster: '$inraster
echo 'Output folder: '$outdir

echo '********************************************************************************************'

#run saved rf models
python "/home/rm885/projects/decid/src/run_saved_rf_model.py" $rf_picklefile $inraster $outdir


echo '********************************************************************************************'
echo 'Done!~~~~~~~~~~'
date
