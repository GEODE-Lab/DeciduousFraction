#!/bin/bash
#SBATCH --job-name=hrf_tc
#SBATCH --time=1-05:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=24000
#SBATCH --array=1-785
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/hrf_tc_model_slurm_%A_%a.out

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_LS8_corr/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_LS8_corr_tc1/'

#if output folder doesn't exist
mkdir $outfolder
echo $datadir
# list of input filess

FILELIST=(${datadir}*.tif)
echo ${#FILELIST[*]}
echo ${FILELIST[*]}
#for this element in job array, pick filename based on task ID
f=${FILELIST[$[SLURM_ARRAY_TASK_ID - 1]]}

echo $f
echo $outfolder

#make tiles
python '/home/rm885/projects/decid/src/run_saved_hrf_model_tc.py' $f $outfolder '/scratch/rm885/gdrive/sync/decid/RF_model_pickles/working/out_tc_2010_samp_v1_RF_59.pickle' '/scratch/rm885/gdrive/sync/decid/RF_model_pickles/working/out_tc_2010_samp_v1_summer_RF_772.pickle'



