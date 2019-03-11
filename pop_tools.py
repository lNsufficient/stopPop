import numpy as np

def threshold_pop(a):
    #Threshold filtering by guessing that most of the noise will not be pop corn but ambient noise.
    abs_a = np.abs(a)
    median_volume = np.percentile(abs_a, 85)
    max_volume = np.percentile(abs_a, 99)
    #remove all sound that's background:
    background_threshold = median_volume + (max_volume-median_volume)*0.1
    thresh_a = a.copy()
    thresh_a[np.abs(thresh_a)<background_threshold] = 0
    return thresh_a, background_threshold
