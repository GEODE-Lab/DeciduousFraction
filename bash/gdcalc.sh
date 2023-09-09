#!/bin/bash
#SBATCH --job-name=gdcalc
#SBATCH --time=3:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=16000
#SBATCH --array=1-1567
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdcalc_hrf_all_model_east_2015_ls8_uncorr_slurm_%A_%a.out

#input folder that contains tif files, dont forget the '/' at the end
datadir='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_output_h2_2015_ls8_uncorr/'

#output folder, dont forget the '/' at the end
outfolder='/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_output_h2_2015_ls8_uncorr_calc/'

#if output folder doesn't exist
mkdir $outfolder
echo $datadir

FILELIST=(${datadir}*.tif)
echo 'Found '${#FILELIST[*]}' output files'

#for this element in job array, pick filename based on task ID
f=${FILELIST[$[SLURM_ARRAY_TASK_ID - 1]]}

f_=${f##*/}
outfile=$outfolder${f_%.tif}'_corr1.tif'

echo $f
echo $outfolder


gdal_calc.py -A $f --outfile=$outfile --calc="(A*100)*(A>=0) + (A*0)*(A<0)" --type=Int16 

date
