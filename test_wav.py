import os

import scipy.io.wavfile as siw
import scipy.ndimage.filters as filters
import numpy as np
import matplotlib.pyplot as plt

path = r'popcorn.wav'
rate, a = siw.read(path)

def visualize_a(a):
    print(a)
    plt.plot(a)
    plt.show()

def play(a, rate=44100, filename='tmp.wav'):
    siw.write(filename, rate, a)
    print("playing sound...("+filename+")")
    os.system('aplay ' + filename)
    print("...sound was played!")


def max_window(a):
    #It seems like a good idea to track max for signals because noise
    #fluctuates around zero...
    return filters.maximum_filter1d(np.abs(a), 100)

#visualize_a(a)
#play(a)    
a_max = max_window(a)
#%%
   
def threshold_pop(a):
    abs_a = np.abs(a)
    median_volume = np.percentile(abs_a, 85)
    max_volume = np.percentile(abs_a, 99)
    #remove all sound that's background:
    background_threshold = median_volume + (max_volume-median_volume)*0.1
    thresh_a = a.copy()
    thresh_a[np.abs(thresh_a)<background_threshold] = 0
    return thresh_a, background_threshold

thresh_a, background_threshold = threshold_pop(a_max)   
pops = (thresh_a > 0)*max(thresh_a)

short_range = rate*50
plt.figure(10, clear=True)
for (data, color, linestyle, marker) in [(a, 'b', '-', ""), (a_max, 'y', '-', ""), (thresh_a, 'r', '-', ""), (pops, 'k', '', 'o')]:
    plt.plot(data[0:short_range], color=color, linestyle=linestyle, marker=marker)
plt.show()