import pandas as pd

"""
This script is used to identify quality flag for compositing Blue-sky albedo
"""

if __name__ == '__main__':

    bluesky_qa_file_flags = "D:/Shared/Dropbox/projects/NAU/landsat_deciduous/data/albedo_Data/" + \
                            "bluesky_quality_flag_key.csv"

    df = pd.read_csv(bluesky_qa_file_flags)

    vals = df['meta_flag_value'].loc[(df['sza_above_70'] == 0.0) &
                                     ((df['mcd43a2_qflag'] == 0.0) |
                                      (df['mcd43a2_qflag'] == 1.0))]

    print(vals.to_numpy().tolist())

    # [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23]
