#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
from load import get_hour_range_files, build_numpy_array
from load import SAMS, parse_basename

SCALE_FACTOR = {
    'g': 1.0,
    'mg': 1.0e-3,
    'ug': 1.0e-6,
}


def check_units():
    """
    Check the units of the pyplot specgram to determine if the
    output is in terms of the original unit or unit-squared.
    """
    # see https://gist.github.com/superlou/4977824

    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return idx, array[idx]

    Fs = 10000.0  # Hz
    duration = 10  # seconds
    t = np.arange(0, duration, 1 / Fs)

    frequency = 100.0  # Hz
    amplitude = 4.0  # volts
    y = amplitude * np.sin(2 * np.pi * frequency * t)

    plt.subplot(311)
    plt.plot(t, y)

    plt.subplot(312)
    nfft = 8192
    Pxx, freqs, bins, im = plt.specgram(y, Fs=Fs, NFFT=nfft, pad_to=nfft)
    plt.ylim([0, 300])

    plt.subplot(313)
    index, nearest_freq = find_nearest(freqs, frequency)
    print "Nearest frequency: " + str(nearest_freq)
    plt.plot(bins, Pxx[index, :])
    plt.ylim([0, 5])

    plt.tight_layout()
    plt.show()


def plot_example_sleep_to_wake(data_dir, unit='F', tsh='B', axis='X', units='g'):
    """plot a specific MET day's hour range for given unit, tsh, axis"""

    # sleep-to-wake transition
    day, hour = 0, 19

    # load wake transition data
    xfiles = get_hour_range_files(data_dir, day, hour-1, hour, unit=unit, tsh=tsh, axis=axis)
    tsh1, axis1, day1, hour1, this_file, num_files = parse_basename(os.path.basename(xfiles[0]))
    minute1 = int(60.0 * (float(this_file) - 1) / float(num_files))
    ddd_hh_mm = '%s/%s:%02d:00' % (day1, hour1, minute1)
    x = build_numpy_array(xfiles)
    print '%d total data pts in array' % x.shape[0]

    # FIXME fine-tune nfft and noverlap to get desired freq. and time resolution
    # that is, compute nfft and noverlap from your desired resolution
    # -- nfft for freq. resolution
    # -- noverlap for temporal resolution
    # NOTE: many canned routines like a power of two for nfft for computational
    #       efficiency/speed [check matplotlib's underlying routine]

    # plot color spectrogram to see crew wake at 19:00
    nfft = 4096  # the length of the windowing segments (finer freq. resolution comes from larger nfft)
    head = SAMS[('Unit %s' % unit, 'TSH %s' % tsh)]
    (Fs, Fc, location) = head  # Fs (sa/sec)

    # build time array (seconds relative to first file's start)
    dt = 1.0 / Fs
    t = np.arange(0.0, x.shape[0] / Fs, dt)

    # figure for plots
    fig = plt.figure(num=None, figsize=(8, 6), dpi=120, facecolor='w', edgecolor='k')

    # super title
    plt.suptitle('SAMS Unit %s, TSH %s\n%s\nt = 0 at MET %s' % (unit, tsh, location, ddd_hh_mm))

    # plot x-axis accel. vs. time
    ax1 = plt.subplot(211)
    plt.plot(t, x / SCALE_FACTOR[units])
    plt.ylabel('%s-Axis Accel. [%s]' % (axis, units))

    # plot spectrogram of time-frequency domain data (to better see wake transition), where:
    # -- pxx = segments x freqs array of instantaneous power
    # -- freqs = frequency vector
    # -- bins = centers of the time bins in which power is computed
    # -- im = matplotlib.image.AxesImage instance
    ax2 = plt.subplot(212, sharex=ax1)
    pxx, freqs, bins, im = plt.specgram(x[:], NFFT=nfft, Fs=Fs, noverlap=nfft/2, cmap='jet', vmin=-140, vmax=-70)

    # FIXME incorporate combined PSDs computation...
    # see Appendix p. B-1 of Summary Report of Mission Acceleration Measurements for STS-87
    # to get equation that shows how to compute overall (combined XYZ) PSDs

    # FIXME verify absolute PSD magnitude, try using Parseval's theorem, but...
    # be sure to demean the (vibratory) data as a first step; no fidelity for DC component (average value)

    # set y-limits for cut-off frequency of this sensor head (25 Hz)
    plt.ylim((0, Fc))

    # add labeling
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Relative Time [sec]')

    # add colorbar
    cbar = fig.colorbar(im)
    cbar.set_label('dB')

    # fix top axes position to compensate for bottom axes colorbar adjustment
    pos1, pos2 = ax1.get_position(), ax2.get_position()  # get the original positions
    pos1 = [pos1.x0, pos1.y0, pos2.width, pos1.height]
    ax1.set_position(pos1)  # set a new position

    plt.show()


def main():
    # local top-level path where you have saved the data
    data_dir = 'G:\usmp4'  # FIXME change this to your local storage

    # plot wake transition (try unit='F', tsh='B', axis='X' for starters)
    plot_example_sleep_to_wake(data_dir, unit='F', tsh='B', axis='X', units='ug')

    # compare with Appendix p. B-7 of Summary Report of Mission Acceleration Measurements for STS-87


if __name__ == "__main__":
    check_units()
    raise SystemExit
    main()
