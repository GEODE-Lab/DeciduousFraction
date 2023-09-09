#!/bin/bash
date
source /home/richard/env/nau/bin/activate
in_file="/scratch/data/tc/samples/hansen_tc_mosaic_2010_coll1_samp_v1_corrected_useful.csv"
out_file="/scratch/data/tc/samples/hansen_tc_mosaic_2010_coll1_samp_v1_corrected_useful_cv_grid_v1.csv"

/home/richard/env/nau/bin/python3 /home/richard/code/decid/prepare_rf_model_cv_grid_tc.py $in_file $out_file tree_cover 44


deactivate
date
