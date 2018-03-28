#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
from load import get_hour_range_files, build_numpy_array
from load import SAMS, parse_basename


def plot_example_sleep_to_wake(data_dir, unit='F', tsh='B', axis='X'):
    """plot a specific MET day's hour range for given unit, tsh, axis"""

    # sleep-to-wake transition
    day, hour = 0, 19

    # load wake transition data
    xfiles = get_hour_range_files(data_dir, day, hour-1, hour, unit=unit, tsh=tsh, axis=axis)
    tsh1, axis1, day1, hour1, this_file, num_files = parse_basename(os.path.basename(xfiles[0]))
    minute1 = int(60.0 * (float(this_file) - 1) / float(num_files))
    ddd_hh_mm = 'Day %s, Hour %s, Minute %02d' % (day1, hour1, minute1)
    x = build_numpy_array(xfiles)
    print '%d total data pts in array' % x.shape[0]

    # FIXME fine-tune NFFT and noverlap to get desired freq. and time resolution
    # that is, compute NFFT and noverlap from your desired resolution
    # -- NFFT for freq. resolution
    # -- noverlap for temporal resolution
    # NOTE: many canned routines like a power of two for NFFT for computational
    #       efficiency/speed [check matplotlib's underlying routine]

    # plot color spectrogram to see crew wake at 19:00
    NFFT = 4096  # the length of the windowing segments (finer freq. resolution comes from larger NFFT)
    head = SAMS[('Unit %s' % unit, 'TSH %s' % tsh)]
    (Fs, Fc, location) = head  # Fs (sa/sec)

    # build time array (seconds relative to first file's start)
    dt = 1.0 / Fs
    t = np.arange(0.0, x.shape[0] / Fs, dt)

    # figure for plots
    fig = plt.figure(num=None, figsize=(8, 6), dpi=120, facecolor='w', edgecolor='k')

    # super title
    plt.suptitle('SAMS Unit %s, TSH %s\n%s\nTime Zero: MET %s' % (unit, tsh, location, ddd_hh_mm))

    # plot x-axis accel. vs. time
    ax1 = plt.subplot(211)
    plt.plot(t, x)
    plt.ylabel('%s-Axis Accel. [g]' % axis)

    # plot spectrogram of time-frequency domain data (to better see wake transition), where:
    # -- Pxx = segments x freqs array of instantaneous power
    # -- freqs = frequency vector
    # -- bins = centers of the time bins in which power is computed
    # -- im = matplotlib.image.AxesImage instance
    ax2 = plt.subplot(212, sharex=ax1)
    Pxx, freqs, bins, im = plt.specgram(x[:], NFFT=NFFT, Fs=Fs, noverlap=NFFT/2, cmap='jet', vmin=-140, vmax=-70)

    # FIXME incorporate combined PSDs computation...
    # see Appendix p. B-1 of Summary Report of Mission Acceleration Measurements for STS-87
    # to get equation that shows how to compute overall (combined XYZ) PSDs

    # FIXME verify absolute PSD magnitude, try using Parseval's theorem, but...
    # be sure to demean the (vibratory) data as a first step (ignore DC component)

    # set y-limits for cut-off frequency of this sensor head (25 Hz)
    plt.ylim((0, Fc))

    # add labeling
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Relative Time [sec]')

    # add colorbar
    fig.colorbar(im)

    # fix ax position
    pos1, pos2 = ax1.get_position(), ax2.get_position()  # get the original positions
    pos1 = [pos1.x0, pos1.y0, pos2.width, pos1.height]
    ax1.set_position(pos1)  # set a new position

    plt.show()


if __name__ == "__main__":

    # local top-level path where you have saved the data
    data_dir = 'G:\usmp4'  # FIXME change this to your local storage

    # plot wake transition (try unit='F', tsh='B', axis='X' for starters)
    plot_example_sleep_to_wake(data_dir, unit='F', tsh='B', axis='X')

    # compare with Appendix p. B-7 of Summary Report of Mission Acceleration Measurements for STS-87
