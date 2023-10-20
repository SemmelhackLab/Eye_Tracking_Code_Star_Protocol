def nd2_to_tif(nd2_file, raw_tif_file):  # , n_trials):
    '''
    Step 1: converts nd2 to tif by how many trials
    '''
    with ND2Reader(nd2_file) as imaging_series:
        global umperpix, imaging_series_mappped_arr
        umperpix = imaging_series.metadata['pixel_microns']
        imaging_series_arr = np.array([i for i in imaging_series])
        print(imaging_series.metadata)
        imaging_series_8bit_arr = cv2.convertScaleAbs(imaging_series_arr, alpha=0.07)
        imaging_series_mapped_arr = map_stack_to('ilp', 'ial',
                                                 imaging_series_8bit_arr)  ##refer to bg-space AnatomicalSpace
        print(imaging_series_mapped_arr.shape)
        frames_per_trial = int(np.ceil(imaging_series_mapped_arr.shape[0] / 18))
        print("frames_per_trial: " + frames_per_trial)

        for i in range(0, imaging_series_mapped_arr.shape[0]):

        # print(imaging_series_mapper_arr)

            imwrite(raw_tif_file, imaging_series_mapped_arr, imagej=True, resolution=(1 / umperpix, 1 / umperpix))