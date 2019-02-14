#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, lfilter, deconvolve, correlate
from tiscsim import Signal, prony
from scipy.fftpack import fft

invSignal = Signal.Signal()
invSignal.initializeFilter()
invSignal.runFilter(np.random.normal(0, 0.5, 1024))

signal = Signal.Signal()
signal.initializeFilter()
signal.runFilter(np.random.normal(0, 0.5, 1024))

invSig = np.zeros(4096)
invSig[90] = 50
b, a = butter(5, 0.12, btype='low', analog=False)
invSig = lfilter(b, a, invSig)
invSig = invSig + np.random.normal(0, 0.5, 4096)

sig = np.zeros(4096)
sig[100] = 50

b, a = butter(5, 0.32, btype='low', analog=False)
sig = lfilter(b, a, sig)
sig = sig + np.random.normal(0, 0.5, 4096)

filtSig = signal.runFilter(sig)
filtHilbert = hilbert(filtSig)

invFiltSig = invSignal.runFilter(invSig)
invFiltHilbert = hilbert(invFiltSig)

t = np.arange(4096)
t = t*0.1

plt.subplot(311)
plt.plot(t[0:1000], filtSig[0:1000])
plt.plot(t[0:1000], invFiltSig[0:1000])

sumSig = filtSig[0:1000] + invFiltSig[0:1000]
plt.subplot(312)
plt.plot(t[0:1000], sumSig)
plt.subplot(313)
plt.plot(correlate(filtSig[0:1000],sumSig))
plt.show()
