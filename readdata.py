import os
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy import signal
import warnings

fs=1/40

def autocorr(x):
    
    result = np.correlate(x, x, mode='full')
    return result[result.size // 2:]
    #return result[::]

def heartbeat(x):
    #peaks=signal.find_peaks(x,prominence)[0][:]
    peaks_index = signal.argrelextrema(x, np.greater) #Calculate the relative extrema of data. find peaks and give back a array of indices aof x axis
    peaks_index = np.insert(peaks_index[0], 0, 0) #insert 0 at the beginning, and make a list
    diff = np.diff(peaks_index)
    std=np.std(diff)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mean=np.mean(diff)
    
    return 60/(mean*fs),std

#freq for the camera:
RGB=[0,1,2]
clr=['red','green','blue']
data_autocorr=[]
data_heartbeat=[0,0,0]
std=[0,0,0]
expected = [75, 71, 65, 70, 82, 69]


for file in range(1,7):
    mindiff=1000
    filename='Målinger/pulse'+str(file)+'.txt'
    data=np.loadtxt(filename)
    #remove the detrend:remove the best straight line fit
    data=signal.detrend(data,axis=0)
    print('\nThe data in file pulse{}.txt is:'.format(file))
    #g=plt.figure(1)
    fig, axs = plt.subplots(2)
    for i in RGB:
    #autocorrelation of itself: autocorrelation refers to the correlation of a time series with a lagged version of itself
        data_row=data[:,i]
        axs[0].plot(data_row,color=clr[i])
        axs[0].title.set_text('The puls data for sample {}BPM'.format(file))
        data_autocorr=autocorr(data_row)
        axs[1].plot(data_autocorr,color=clr[i])
        axs[1].title.set_text('The autocorrelated puls signal for sample {} BPM'.format(file))
        data_heartbeat[i],std[i]=heartbeat(data_autocorr)
        newdiff=abs(data_heartbeat[i]-expected[file-1])
        if newdiff < mindiff:
            best=i
            mindiff=newdiff
        print('The heartbeat of color {} is {:.3f}, with standard deviation {:.3f}'.format(clr[i],data_heartbeat[i],std[i]))
    #find the colour with the best pulse, closes to expected and lowest std
    print("The expected heartbeat for this measurement is {}, the closet color channel is {} with heartbeat {:.1f}".format(expected[file-1],clr[best],data_heartbeat[best]))
    plt.show()
    
