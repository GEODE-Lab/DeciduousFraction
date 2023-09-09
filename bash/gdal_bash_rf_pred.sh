#!/bin/bash
#SBATCH --job-name=rf_tile
#SBATCH --time=23:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=18000
#SBATCH --array=1-36767
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/rf_pred_ras_tile_%A_%a.out

#This is a bash script to make tiles from uncompressed tif files
date
echo 'Begin!~~~~~~~~~~'
#input folder that contains tif files, dont forget the '/' at the end
raster_tiles='/scratch/rm885/gdrive/sync/decid/alaska_data/tiles_boundV2/'

#dir containing RF models, 
rdatadir='/scratch/rm885/gdrive/sync/decid/rdata'

#output prediction directory,
outdir='/scratch/rm885/gdrive/sync/decid/alaska_data/pred_out'

#make filelist array
declare -a FILELIST
for f in $raster_tiles*; do
    FILELIST[${#FILELIST[@]}+1]=$(echo "$f");
done

#what this statement does: for this element in job array, pick filename based on task ID
inraster=${FILELIST[$SLURM_ARRAY_TASK_ID]}

#print input file
echo 'input raster'
echo ${inraster}
echo 'rdata directory'
echo ${rdatadir}
echo 'out data directory'
echo ${outdir}

#run saved rf models
Rscript --vanilla '/home/rm885/projects/decid/run_saved_rf_model.R' ${inraster} ${rdatadir} ${outdir}

echo 'Done!~~~~~~~~~~'
date
