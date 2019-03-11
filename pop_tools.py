import scipy.ndimage.filters as filters
import numpy as np
from scipy.ndimage.measurements import label as sc_bwlabel


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


def max_window(a, nbr_samples=100):
    #It seems like a good idea to track max for signals because noise
    #fluctuates around zero...
    return filters.maximum_filter1d(np.abs(a), nbr_samples, mode='constant', cval=0)

def pop_grouping(pop_vec, rate=44100):
    #group adjacent pops to one if their space is less than 0.2 seconds
    #this is practically imdilate
    dt = 1.0/rate
    samples_space = int(np.ceil(0.2/dt))
    maxed = max_window(pop_vec, samples_space)
    #from here on, matching could be done to the pop_vec, so that
    # the pops are not dilated but simply grouped if they are close to each other.
    return maxed

def bwlabel(pop_vec):
    labeled_vector, nbr_labels = sc_bwlabel(pop_vec)
    return labeled_vector, nbr_labels
