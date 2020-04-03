# TTT4280
Lab work for TTT4280: Sensors and Instrumentation, at NTNU.

** Information about measurements: **

__All measurements are found in /resultater/results.txt__

Measurements 1 through 6, as well as 12, are measured using transmittance.\
All of these measurements are completed using PiCam v2 at Fs = 40 Frames/s.

Measurements 7 through 11 are reflectance measurements.\
These are conducted using the phone camera (Samsung Galaxy S10+) and flashlight, at Fs = 1/30 Frames/s.
The exception is measurement 11, which is measured using PiCam v2.

We've mixed in various tests:

Measurement 1 and 2 are done in a dark room void of all external lights.
Measurement 11 attempts to measure the pulse in the forehead by using reflectance.
Measurement 12 is a measurement of a slightly higher pulse after a couple of trips up/down the stairs.

__Discussion__:

Two dataprocessing files are included. This is due to the fact that our group cannot meet during these times of\
COVID-19. Therefore, each contributor has commited one processing script each. "readData.py" writes directly to console and plots the data from each sample,
while "read_data.py" writes to results.txt. Data is processed using autocorrelation, and these autocorrelation plots are available by running "readdata.py".

We observe that the results are varying. To begin with, the forehead measurement (11) is quite far off, even though we've tried several flashlights and positionings. Secondly, observe that the reflectance measurements are off. These are conducted using a smartphone camera at Fs = 1/30 Frames/s. The red color channel performs relatively well here, apart from measurement 7, which shows green to be the only one even remotely close (which might be a coincidence. In the case of having to write a report, these reflectance measurements will be retaken, and it seems to be of value to get hold of a small flashlight which can be taped to the finger.


Except deviations explained above from the reflectance measurements, we see that the red color channel yields the most accurate results (which is expected, as a longer wavelength means more transmittance).

