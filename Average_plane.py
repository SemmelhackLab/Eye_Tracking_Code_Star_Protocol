import tiffile

def avg_imaging(imaging_tif_path, avg_tif_path):
    """
    Step 2: generates averaged_video.tif for brain registration input
    This function averages the calcium imaging data into a single tif.
    """
    imaging_tif_original = tifffile.imread(imaging_tif_path)
    nframes, h, w = imaging_tif_original.shape
    temp = np.zeros((h, w), dtype=np.float64)
    for n in range(nframes):
        curframe = imaging_tif_original[n]
        temp+=curframe
    avg = temp/nframes
    avg_tif = avg.astype(np.uint8)
    plt.imshow(avg_tif, cmap='gray')
    tifffile.imwrite(avg_tif_path, avg_tif, imagej=True, resolution=(1/umperpix, 1/umperpix))