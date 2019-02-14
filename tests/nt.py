import numpy as np
import scipy

def rollingWindow(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def snrVsLen(signal, noise):
    xaxis = [ 20, 40, 60, 80, 100, 120, 140, 160, 180 ]

    noiseMean = np.zeros(len(xaxis))
    noiseStd = np.zeros(len(xaxis))
    snr = np.zeros(len(xaxis))
    for length in xaxis:
        rollingNoise = rollingWindow(noise, length)
        rollingNoiseSum = np.sum(rollingNoise*rollingNoise, axis=1)
        mean = np.mean(rollingNoiseSum)
        std = np.std(rollingNoiseSum)
        noiseMean[(length/20)-1] = mean
        noiseStd[(length/20)-1] = std
        rollingWfm = rollingWindow(signal, length)
        rollingWfmSum = np.sum(rollingWfm*rollingWfm, axis=1)
        snr[(length/20)-1] = (np.max(rollingWfmSum)-mean)/std
    print noiseMean
    print noiseStd
    return snr

