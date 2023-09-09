#!/bin/bash
#SBATCH --job-name=alb_ovr
#SBATCH --time=1:59:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=16000
#SBATCH --partition=all
#SBATCH --output=/home/rm885/slurm-jobs/albedo_data_overview_%j.out

module load gdal/2.2.1

date
echo 'Begin!~~~~~~~~~~'
datadir='/scratch/rm885/gdrive/sync/decid/albedo_data/'
files=(${datadir}albedo_data_2000_2010*.tif)

nn=${#files[@]}

for (( n=0; n<nn; n++ ))
do
    echo ${files[n]}
    gdaladdo -ro ${files[n]} 2 4 8 16 32 64 128 256 --config COMPRESS_OVERVIEW LZW --config BIGTIFF_OVERVIEW YES
    
done


date
