#!/usr/bin/env bash
array_job_uncert=$(sbatch /scratch/rm885/support/sh/prepare_rf_models_job_array.sh | awk '{ print $4 }')
sbatch --dependency=afterany:$array_job_uncert/scratch/rm885/support/sh/compile_rf_model_outputs.sh
