import ee

if __name__ == '__main__':

    ee.Initialize()

    geometry = [[-170.73985511272565, 76.3502729972969],
                [-174.25548011272565, 45.20815673035308],
                [-124.68516761272565, 43.44792438269342],
                [-81.97032386272565, 34.73595898261199],
                [-31.87266761272565, 35.3117524939334],
                [-37.14610511272565, 74.95760622832898],
                [-55.07579261272565, 82.72009262995844],
                [-65.44688636272565, 83.88563291295817],
                [-136.81407386272565, 83.11024575198749]]

    asset_list = ['ABoVE_count_1992_181_225_12803_clear',
                  'ABoVE_count_2000_181_225_10265_clear',
                  'ABoVE_count_2005_181_225_13622_clear',
                  'ABoVE_count_2010_181_225_12538_clear',
                  'ABoVE_count_2015_181_225_18129_clear',
                  'ABoVE_count_mask_1992_136_180_10619_clear',
                  'ABoVE_count_mask_1992_181_225_12803_clear',
                  'ABoVE_count_mask_1992_226_273_10222_clear',
                  'ABoVE_count_mask_2000_136_180_8201_clear',
                  'ABoVE_count_mask_2000_181_225_10265_clear',
                  'ABoVE_count_mask_2000_226_273_9759_clear',
                  'ABoVE_count_mask_2005_136_180_11081_clear',
                  'ABoVE_count_mask_2005_181_225_13622_clear',
                  'ABoVE_count_mask_2005_226_273_12361_clear',
                  'ABoVE_count_mask_2010_136_180_11427_clear',
                  'ABoVE_count_mask_2010_181_225_12538_clear',
                  'ABoVE_count_mask_2010_226_273_10948_clear',
                  'ABoVE_count_mask_2015_136_180_16398_clear',
                  'ABoVE_count_mask_2015_181_225_18129_clear',
                  'ABoVE_count_mask_2015_226_273_16288_clear']

    for asset_name in asset_list:

        image_task_config = {'outputBucket': 'masseyr44_store1',
                             'outputPrefix': 'count/{}'.format(asset_name),
                             'region': geometry,
                             'maxPixels': 1e13,
                             'scale': 30}

        post_image_task = ee.batch.Export.image(ee.Image('users/masseyr44/decid/' + asset_name),
                                                description=asset_name,
                                                config=image_task_config)

        post_image_task.start()

