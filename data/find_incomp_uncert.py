from modules import *


if __name__ == '__main__':

    chk_dir = '/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_LS8_corr_tc1/'
    source_dir = '/scratch/rm885/gdrive/sync/decid/ABoVE_data_boreal_LS8_corr/'

    dir_handler = Handler(dirname=chk_dir)

    prediction_files = dir_handler.find_all('prediction')
    uncertainty_files = dir_handler.find_all('uncertainty')

    prediction_list = list(elem.split('_prediction.tif') for elem in prediction_files)
    uncertainty_list = list(elem.split('_uncertainty.tif') for elem in uncertainty_files)

    print(prediction_list)
    print(uncertainty_list)

    incomplete_list = list()
    for prediction_file in prediction_list:
        if prediction_file not in uncertainty_list:
            incomplete_list.append(source_dir + Handler(prediction_file).basename + '.tif')

    for elem in incomplete_list:
        print(elem)
