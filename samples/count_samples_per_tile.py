from geosoup import Handler
import numpy as np
import json


if __name__ == '__main__':

    infile = "C:/Users/Richard/Desktop/extracted_samples.txt"

    filelines = Handler(infile).read_text_by_line()

    sample_count = np.zeros(len(filelines), dtype=np.int16)

    for i, fileline in enumerate(filelines):
        file_dict = json.loads(fileline.replace("'", '"'))

        _, samp_list = list(file_dict.items())[0]

        sample_count[i] += len(samp_list)

    print('histogram:')
    print(np.histogram(sample_count, bins=[0, 2, 10, 20, 50, 100, 200, 500, 1000, 2000])[0])
    print('----------------')

    print('Min: {}, Max: {}'.format(min(sample_count), max(sample_count)))
    print('Total: {}'.format(np.sum(sample_count)))
