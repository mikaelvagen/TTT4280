import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from tabulate import tabulate
import itertools
"""
This script calculates heartbeat from file.

Input file contains three color channels,
using autocorrelation and PiCam v2, heartbeat
is calculated for each channel.

Parameters:
:: Fs (float) :: camera frequency
:: RGB (list) :: contains column numbers [red, green, blue]
:: pulse (list) :: stores calculated channel pulses
"""
Fs = 1/40
RGB = [0, 1, 2]
pulse = []
table = []
expected = []
deviance = []
std=[]

for file_num in range(1, 13):
    filename = "målinger/pulse" + str(file_num) + ".txt"
    data = np.loadtxt(filename)
    data = signal.detrend(data, axis=0)

    for column in RGB:
        corr_data = np.correlate(data[:, column], data[:, column], mode='full')
        corr_data = corr_data[corr_data.size // 2 + 1 :]
        peaks_index = signal.argrelextrema(corr_data, np.greater)
        peaks_index = np.insert(peaks_index[0], 0, 0)
        diff = np.diff(peaks_index)
        std.append(np.std(diff))
        average_beat = np.mean(diff)
        pulse.append(60 / (average_beat * Fs)) # this is fixed! average_beat * Fs is diff in seconds.
        c = ["red", "green", "blue"]
        plt.plot(corr_data, color = c[column])

channels = ['Red', 'Green', 'Blue'] * (len(pulse) // 3)
meas = [meas - i for meas, i in zip(range(1, len(pulse) + 1, 3), range(0, len(pulse), 2))]
meas = list(itertools.chain.from_iterable(itertools.repeat(x, 3) for x in meas))

for num_of_meas in range(0, (len(pulse) // 3)):
    expected = [75, 71, 65, 70, 82, 69, 62, 67, 69, 66, 72, 82]
expected = list(itertools.chain.from_iterable(itertools.repeat(x, 3) for x in expected))

for v, e in zip(pulse, expected):
    v = float(v)
    deviance.append(abs(v - e))

for i in range(0, len(pulse)):
    table.append([meas[i], channels[i], "{0:.1f} BPM".format(pulse[i]),
        "{0:.1f} BPM".format(expected[i]), "{0:.1f} BPM".format(deviance[i]),"{0:.1f}".format(std[i])])

with open("resultater/results.txt", "w") as results: # write results to file
    results.write(tabulate(table,
        headers=["Measurement #", "Channels", "Heartbeat", "Expected BPM", "Deviance","Standard deviation"],
        tablefmt="fancy_grid" ))

plt.show()
