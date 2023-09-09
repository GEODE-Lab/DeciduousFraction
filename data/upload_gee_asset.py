from modules import *
import datetime
import subprocess
import os

if __name__ == '__main__':

    collection = 'users/masseyr44/bluesky_albedo'
    bucket_name = 'masseyr44_store1'
    project = 'massey-01'
    bucket_folder = 'bluesky_albedo/geographic'
    search_str = '*albedo.tif'
    script_file = '/home/richard/gee_run.sh'
    nodata_value = -9999
    bandnames = 'albedo'
    srs = 'EPSG:4326'
    property_dict = {'type': 'bluesky'}

    bucket = Storage(bucket_name,
                     project=project,
                     input_path=bucket_folder)

    file_list = bucket.list_blobs(pattern=search_str)

    command = "earthengine ls {}".format(collection)

    list_proc = subprocess.Popen(command.split(" "),
                                 stdout=subprocess.PIPE)

    asset_list = list_proc.stdout.read().split('\n')[:-1]
    asset_name_list = list(asset_name.split(collection + '/')[1] for asset_name in asset_list)

    print('Assets in GEE: {}'.format(str(len(asset_name_list))))

    property_str = ' '.join(list('--property {k}={v}'.format(k=str(key),
                                                             v=str(val))
                                 for key, val in property_dict.items()))

    count = 0

    with open(script_file, 'w') as f:

        f.write('#!/bin/sh')

        for file_name in file_list:
            asset_name = file_name.split('.tif')[0]

            if asset_name not in asset_name_list:

                count += 1

                date_str = file_name.split('bluesky_albedo_')[1].split('_albedo.tif')[0].replace('_', '')
                date = datetime.datetime.strptime(date_str, '%Y%j').date().isoformat()

                command = "earthengine upload image " + \
                          "--asset_id '{c}/{n}' ".format(c=collection,
                                                         n=file_name.split('.tif')[0]) + \
                          "--nodata_value {nd} --bands '{b}' ".format(nd=nodata_value,
                                                                      b=bandnames) + \
                          "--crs '{srs}' ".format(srs=srs) + \
                          "{ps} ".format(ps=property_str) + \
                          "--time_start '{d}' ".format(d=date) + \
                          "gs://{bn}/{bf}/{n}".format(bn=bucket_name,
                                                      bf=bucket_folder,
                                                      n=file_name)

                f.write(command + '\n')

            else:
                pass
                # print('Asset {} already ingested'.format(asset_name))

    print('\n\nFound {} un-uploaded assets'.format(str(count)))

    print('\nWritten shell script ... {}'.format(script_file))

    os.system('sh {}'.format(script_file))

