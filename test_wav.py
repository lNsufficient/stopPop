import os

import scipy.io.wavfile as siw
import scipy.ndimage.filters as filters
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.measurements import label as bwlabel

pop_path = r'C:\Users\edjn\not_job\stopPop'
#pop_path = r'/home/edjn/git/stopPop'
#os.chdir(pop_path)
path = r'popcorn.wav'
rate, a = siw.read(path)
dt = 1.0/rate
t = np.array(range(len(a)))*dt

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
    if marker == "o":
        continue
    plt.plot(data[0:short_range], color=color, linestyle=linestyle, marker=marker)
plt.show()

#%% Save data for recorded pops. 
#THIS IS A FAILURE!
"""
pop_recording_length = 3 #seconds
pop_recording_samples = rate*pop_recording_length//2

row_inds = np.where(pops > 0)
inds = row_inds[0]
pop_inds = []
len(inds)
print inds
#group inds...
pop_recording = a[0:short_range]
copied_data = np.empty(a.shape)
copied_data[:] = False
start_inds = inds - pop_recording_samples
stop_inds = inds + pop_recording_samples
good_inds =  []
for start_ind, stop_ind in zip(*(start_inds, stop_inds)):
    i
    #print start_ind, stop_ind
    copied_tmp = copied_data[start_ind:stop_ind]
    tot_nbrs = stop_ind - start_ind
    copied_nbrs = sum(copied_tmp)
    q = copied_nbrs*1.0/tot_nbrs
    if q < 0.5:
        good_inds.append((start_ind, stop_ind))
        copied_data[start_ind:stop_ind] = True
    #siw.write("pop_ind_"+str(ind)+"_popnbr_"+str(i), rate, data_tmp)
"""
#%% Smarter way of saving recorded pops:
labeled, nbr_labels = bwlabel(pops)
plt.plot(t, labeled)    
#%%
from matplotlib.pyplot import psd
import matplotlib.pyplot
import scipy.signal as scs
Nx = 256*8
#psd(a, NFFT=Nx, Fs=rate, Fc=0, detrend='mean',window=scs.get_window('hamming', Nx), noverlap=0, pad_to=None,sides='default', scale_by_freq=None, return_line=None)
plt.figure()
matplotlib.pyplot.specgram(a, NFFT=Nx, Fs=rate, Fc=0, detrend=None, window=scs.get_window('hamming', Nx), noverlap=Nx/4, cmap='jet', xextent=None, pad_to=Nx*2, sides=None, scale_by_freq=None, mode=None, scale=None, vmin=None, vmax=None, data=None)
bottom, top = plt.ylim()  # return the current ylim
#%%
plt.figure()
labeled, nbr_labels = bwlabel(pops)
pop_vec = (labeled > 0)*top*0.9
pop_vec[pop_vec == 0] = np.nan
plt.plot(t, pop_vec, 'kx', alpha=0.5)
#Only keep first label of each pop:
#bwlabel so there are always zeros between groups:
first_inds = (np.diff(labeled) > 0)*top*0.9
first_inds[first_inds==0] = np.nan
plt.plot(t[:-1], first_inds, 'ko', alpha=0.1)
