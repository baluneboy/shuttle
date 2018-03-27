#!/usr/bin/env python

import os
import glob
import numpy as np


# see p. 5 of Summary Report of Mission Acceleration Measurements for STS-87
SAMS = {
    ('Unit F', 'TSH A'): ( 50,  10, 'Forward MPESS Carrier (Near AADSF)'),
    ('Unit F', 'TSH B'): (125,  25, 'Forward MPESS Carrier (Near MEPHISTO)'),
    ('Unit G', 'TSH A'): ( 50,   5, 'Rear MPESS Carrier (Inside IDGE)'),
    ('Unit G', 'TSH B'): (250, 100, 'Rear MPESS Carrier (Inside CHeX)'),
}


def get_accel_dir(day, unit, tsh, data_dir):
    """return accel subdirectory string given integer day and strings for unit, head and usmp4 dir"""
    # like /home/ken/data/usmp4/usmp_4F_1/HEADB/DAY000/ACCEL
    u = 'usmp_4%s_1' % unit
    h = 'HEAD%s' % tsh
    d = 'DAY%03d' % day
    return os.path.join(data_dir, u, h, d, 'ACCEL')


def get_hour_files(axis, day, hour, unit, tsh, data_dir='/home/ken/data/usmp4'):
    """return list of accel data files for given axis, day, hour, etc."""
    acc_dir = get_accel_dir(day, unit=unit, tsh=tsh, data_dir=data_dir)
    glob_pat = os.path.join(acc_dir, '%s%sM%03d%02d.*' % (tsh, axis, day, hour))  # full filename to like BXM00018.55R
    files = sorted(glob.glob(glob_pat))
    return files


def padread(filename, columns=4, out_dtype=np.float32):
    """return 2d numpy array of float32's read from filename input"""
    with open(filename, "rb") as f:
        A = np.fromfile(f, dtype=np.float32) # accel file: 32-bit float "singles"
    B = np.reshape(A, (-1, columns))
    if B.dtype == out_dtype:
        return B
    return B.astype(out_dtype)


def build_numpy_array(fnames):
    """build numpy array from data read from list of filenames"""
    arr = np.empty((0, 1), dtype=np.float32)
    print 'building array...'
    for fname in fnames:
        # read data from file
        a = padread(fname, columns=1)
        a[:, 0] = a[:, 0] - a[:, 0].mean(axis=0)  # demean column(s)
        print '+ %d data pts from %s' % (a.shape[0], fname)
        arr = np.append(arr, a, axis=0)
    return arr[:, 0]


def get_hour_range_files(data_dir, day, h1, h2, unit='F', tsh='B', axis='X'):
    """get list of accel data files for this day, hour range, unit, etc."""
    some_files = []
    for hr in range(h1, h2+1):
        some_files += get_hour_files(axis, day, hr, unit, tsh, data_dir=data_dir)
    return some_files
