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

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        res=10*np.log((np.where(sd == 0, 0, m/sd)/10**(-3)))
    return res

#freq for the camera:
RGB=[0,1,2]
clr=['red','green','blue']
data_autocorr=[]
data_heartbeat=[0,0,0]
std=[0,0,0]
expected = [75, 71, 65, 70, 82, 69]
noiseratio=0


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
        #noiseratio=signaltonoise(data_row) #gives wrong output
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

print('''\nThe first six measurements are done by measuring the transmittance through a finger. We see that for these measurements the red channel gives us the closes result compare to the expected value, and has for the most part the lowest standard deviation. Measurement seven to ten are done with reflectance off the finger.
  To stress test the model we have done several tests:
    1) Dark room: measurement 1 and 2
    2)Measurement on the forehead: measurement 11
    3) variating heartbeat do to exercise: measurement 12
      ''')
    
