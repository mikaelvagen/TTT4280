import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import statistics
import warnings

"""
This module aims to calculate and plot
signal-to-noise ratios of one accurate
measurement and one inaccurate one.

Chosen measurements: 1 and 11 in results.txt.

Method:
signal_amplitude / mean(noise_peak_amplitudes)
"""

fig, ax = plt.subplots(2)
fig.tight_layout(pad=5)
for i in range(0,2):
    ax[i].set_xlabel("Frequency [Hz]")
    ax[i].set_ylabel("Amplitude")
ax[0].set_title("FFT spectrum of measurement 1")
ax[1].set_title("FFT spectrum of measurement 11")

def calc_snr(sig, sig_status):

    """
    Parameters:
    :: samples [int] :: number of samples in a given signal.
    :: f [array] :: for conversion to frequency from samples.
    :: sig [array] :: signal passed in containing all color channels.
    :: sig_status [bool] :: true if good signal, false if bad signal.
    :: <color>_data [array] :: contains signal for <color> channel.
    :: fft_<color> :: fft of <color> signal.
    :: <color>_sig_bucket [list] :: contains freq bucket of wanted <color> signal.
    :: <color>_noise_bucket [list] :: contains freq bucket of <color> noise peaks.

    Returns:
    :: sig_snr [number] :: signal to noise ratio of signal.
    """

    samples = 1198
    f = np.linspace(0, 50, samples)

    red_data = sig[:, 0]
    green_data = sig[:, 1]
    blue_data = sig[:, 2]

    fft_red = np.fft.fftshift(np.fft.fft(red_data))
    fft_green = np.fft.fftshift(np.fft.fft(green_data))
    fft_blue = np.fft.fftshift(np.fft.fft(blue_data))

    fft_red[0:599] = 0
    fft_green[0:599] = 0
    fft_blue[0:599] = 0

    if sig_status:
        ax[0].plot(f - 25, abs(np.log(fft_red)), color = "Red")
        ax[0].plot(f - 25, abs(np.log(fft_green)), color = "Green")
        ax[0].plot(f - 25, abs(np.log(fft_blue)), color = "Blue")

        red_sig_bucket = signal.find_peaks(abs(np.log(fft_red)), prominence = 4.2)[0]
        green_sig_bucket = signal.find_peaks(abs(np.log(fft_green)), prominence = 4.2)[0]
        blue_sig_bucket = signal.find_peaks(abs(np.log(fft_blue)), prominence = 4.2)[0]

        red_noise_bucket = signal.find_peaks(abs(np.log(fft_red)), prominence = 1.0)[0]
        green_noise_bucket = signal.find_peaks(abs(np.log(fft_green)), prominence = 1.0)[0]
        blue_noise_bucket = signal.find_peaks(abs(np.log(fft_blue)), prominence = 1.0)[0]

    if not sig_status:
        ax[1].plot(f - 25, abs(np.log(fft_red)), color = "Red")
        ax[1].plot(f - 25, abs(np.log(fft_green)), color = "Green")
        ax[1].plot(f - 25, abs(np.log(fft_blue)), color = "Blue")

        """
        Due to the low quality of the measurement, we assume signal at sample 636.
        This sample corresponds to the sample for the good signal, and
        the expected heartbeat is very close, so should be very close.

        Either way, this is just to illustrate that the signal is lost in noise,
        and thus illustrate the difference between a good and bad measurement.
        """

        red_sig_bucket = [636]
        green_sig_bucket = [636]
        blue_sig_bucket = [636]

        red_noise_bucket = signal.find_peaks(abs(np.log(fft_red)), prominence = 2.0)[0]
        green_noise_bucket = signal.find_peaks(abs(np.log(fft_green)), prominence = 2.0)[0]
        blue_noise_bucket = signal.find_peaks(abs(np.log(fft_blue)), prominence = 2.0)[0]

    red_noise_bucket = np.delete(red_noise_bucket, 0) # Remove signal amplitude
    green_noise_bucket = np.delete(green_noise_bucket, 0)
    blue_noise_bucket = np.delete(blue_noise_bucket, 0)

    sig_red = abs(np.log(fft_red))[red_sig_bucket[0]]
    sig_green = abs(np.log(fft_green))[green_sig_bucket[0]]
    sig_blue = abs(np.log(fft_blue))[blue_sig_bucket[0]]
    red_noise_amplitude = []
    green_noise_amplitude = []
    blue_noise_amplitude = []
    num_meas = 0
    while num_meas < 3:
        if num_meas == 0:
            for i in range(0, len(red_noise_bucket)):
                red_noise_amplitude.append(abs(np.log(fft_red))[red_noise_bucket[i]])
            red_noise_mean = statistics.mean(red_noise_amplitude)
        elif num_meas == 1:
            for i in range(0, len(green_noise_bucket)):
                green_noise_amplitude.append(abs(np.log(fft_green))[green_noise_bucket[i]])
            green_noise_mean = statistics.mean(green_noise_amplitude)
        elif num_meas == 2:
            for i in range(0, len(blue_noise_bucket)):
                blue_noise_amplitude.append(abs(np.log(fft_blue))[blue_noise_bucket[i]])
            blue_noise_mean = statistics.mean(blue_noise_amplitude)
        else: break
        num_meas += 1

    red_snr = sig_red / red_noise_mean
    green_snr = sig_green / green_noise_mean
    blue_snr = sig_blue / blue_noise_mean

    return red_snr, green_snr, blue_snr


if __name__ == '__main__':

    # ignoring log(0) errors, no impact on result.
    warnings.filterwarnings("ignore") # we realize it's not usually a good solution to ignore warnings...

    sig_good = np.loadtxt("målinger/pulse1.txt")
    sig_bad = np.loadtxt("målinger/pulse11.txt")

    print("\nSNR Measurement 1:\nRed Channel: {:.5f}\nGreen Channel: {:.5f}\nBlue Channel: {:.5f}\n"
        .format(calc_snr(sig_good, True)[0], calc_snr(sig_good, True)[1], calc_snr(sig_good, True)[2]))
    print("SNR Measurement 11:\nRed Channel: {:.5f}\nGreen Channel: {:.5f}\nBlue Channel: {:.5f}"
        .format(calc_snr(sig_bad, False)[0], calc_snr(sig_bad, False)[1], calc_snr(sig_bad, False)[2]))

    plt.show()
