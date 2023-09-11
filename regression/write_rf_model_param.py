import json


"""
This script is used to write a text file containing a list of ictionaries containing
parameters for a random forest model. Ths parameters include:
1) trees : number of trees
2) samp_split : minimum number of samples required to split an internal node
3) samp_leaf : minimum number of samples required to be at a leaf node
4) max_feat :  number of features to consider when looking for the best split
"""

if __name__ == '__main__':

    ntrees_list = [10, 20, 50, 100, 200, 500, 1000]
    samp_leaf_list = [1, 2, 5, 10, 20, 50, 100]
    samp_split_list = list(range(2, 21))
    max_feat_list = list(range(1, 34))

    out_file = 'C:/users/rm885/Dropbox/projects/NAU/landsat_deciduous/data/SAMPLES/rf_param_v7.csv'

    param_list = list()
    header_list = ['trees',
                   'samp_split',
                   'samp_leaf',
                   'max_feat']

    for i in ntrees_list:
        for j in samp_split_list:
            for k in samp_leaf_list:
                for l in max_feat_list:
                    temp_dict = [str(i),
                                 str(j),
                                 str(k),
                                 str(l)]

                    print(', '.join(temp_dict))
                    param_list.append(temp_dict)

    print('Length of dict: {}'.format(str(len(param_list))))

    with open(out_file, 'w') as f:
        f.write(', '.join(header_list) + '\n')

    with open(out_file, 'a') as f:
        for param in param_list:
            f.write(', '.join(param) + '\n')

    print('File Written: {}'.format(out_file))
