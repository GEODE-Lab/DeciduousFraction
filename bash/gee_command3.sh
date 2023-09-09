#!/bin/bash
#SBATCH --job-name=gee1
#SBATCH --time=23:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=4000
#SBATCH --partition=all
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/rclone_gee_%j.out

rclone copy "/scratch/rm885/gdrive/sync/decid/RF_decid_frac_output_tiles/ABoVE_decid_2010_mosaic_vis.tif" masseyr44_gcs:masseyr44_store1/
earthengine upload image --asset_id=users/masseyr44/decid/ABoVE_decid_2010_mosaic_vf gs://masseyr44_store1/ABoVE_decid_2010_mosaic_vis.tif
earthengine acl set public users/masseyr44/decid/ABoVE_decid_2010_mosaic_vf
