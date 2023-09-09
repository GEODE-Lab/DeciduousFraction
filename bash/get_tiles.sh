#!/bin/bash
#SBATCH --job-name=rclone
#SBATCH --time=2:59:59
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=2000
#SBATCH --begin=now+2hours

date

downloaddir='/scratch/rm885/gdrive/sync/decid/ABoVE_tiles/'

if [ ! -d $downloaddir ]; then
	mkdir $downloaddir;
fi

module load rclone
rclone --include "ABoVE_img_am_2010_z5*.tif" copy masseyr44:/ABoVE_data_Can/ /scratch/rm885/gdrive/sync/decid/ABoVE_tiles/
