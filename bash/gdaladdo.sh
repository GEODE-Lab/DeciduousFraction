#!/bin/bash
#SBATCH --job-name=addo
#SBATCH --time=15:59:59
#SBATCH --cpus-per-task=1
#SBATCH --mem=54000
#SBATCH --output=/scratch/rm885/support/out/slurm-jobs/gdal_add_o_slurm_%A.out

gdaladdo -ro "/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal/ABoVE_median_SR_NDVI_boreal_2015-0000031744-0000142848.tif" 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES

