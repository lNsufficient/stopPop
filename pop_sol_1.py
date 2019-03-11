import matplotlib.pyplot as plt

import wav_tools
import pop_tools

path = r'pop_1.wav'

rate, a, t = wav_tools.read(path)

a_max = pop_tools.max_window(a)
thresh_a, background_threshold = pop_tools.threshold_pop(a_max)
grouped = pop_tools.pop_grouping(thresh_a, rate=rate)
bwlabeled, nbr_labels = pop_tools.bwlabel(grouped)
plt.figure()
ax1 = plt.subplot(311)
ax1.plot(t, a)
ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(t, thresh_a)
ax3 = plt.subplot(313, sharex=ax1)
ax3.plot(t, bwlabeled)
plt.show()
