import ee


if __name__ == '__main__':

    ee.Initialize()

    file_name = "C:/Users/Richard/Downloads/del_ee_asset.sh"

    with open(file_name, 'w') as f:

        f.write("#!/bin/sh\n")

        for i in range(2013, 2017):

            for j in range(1, 366):

                f.write("earthengine rm -v users/masseyr44/bluesky_albedo/bluesky_albedo_{}_{}_albedo\n".format(str(i),
                                                                                                             str(j)
                                                                                                             .zfill(3)
                                                                                                             ))


