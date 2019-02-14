#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.stats import rice
from scipy.signal import lfilter, lfilter_zi
from tiscsim import Signal

# Noise amplitude.
noise = 1.0
amplitude = 1.0
duration = 1.0E-6
fs = 10.0E9
samples = int(fs*duration)
t = np.arange(samples)/fs
# cycles/sec
freq = 288.0E6

amplitude = 1.0
phase = None

def runRiceTest(amplitude=None, phase=None):

    signal = Signal.Signal()
    signal.initializeFilter()
    # Prime it with Gaussian noise
    signal.runFilter(np.random.normal(0, noise, 1024))


    # rad/sec
    angularFreq = freq*(2*np.pi)
    # rad/sample = (rad/sec)*(sec/sample) = (rad/sec)/(samples/sec)
    angularFreqInSampleUnits = angularFreq/fs

    # Figure out random phase. We'll need to screw with this a bit more.
    if phase == None:
        phase = np.random.ranf()*2*np.pi

    # Cheat and add a BUNCH of cycles to this to help the filter feed.
    # sin() obviously doesn't care.
    phase = phase + 20*np.pi
    if amplitude == None:
        amplitude = 1.0

    # We want sin(f*t - phase), but we want to feed the filter starting at 0
    # so it doesn't artifact. So we refactor this as
    # sin(f*(t-t0)) so phi = f*t0.
    numSampleOffset = int(np.round(phase/angularFreqInSampleUnits))
    # Now generate the equivalent rounded phase
    roundedPhase = numSampleOffset*angularFreqInSampleUnits
    # Now we generate the samples to feed to the filter.

    # First generate the times...
    t_prefeed = np.arange(numSampleOffset)/fs
    # and now the samples, with no phase
    prefeed = amplitude*np.sin(angularFreq*t_prefeed)
    # and now the noise
    prefeed_noise = np.random.normal(0, noise, numSampleOffset)
    # and now we feed them in
    prefeed_out = signal.runFilter(prefeed+prefeed_noise)

    # Now generate our signal, with the rounded phase.
    sig = amplitude*np.sin(angularFreq*t+roundedPhase)
    # ... and noise
    gaus = np.random.normal(0, noise, samples)
    # ... and add them
    noisy_signal = sig+gaus

    # Now generate the *filtered* version
    filtData = signal.runFilter(noisy_signal)

    # and return them
    return ( sig, gaus, noisy_signal, filtData )


def plotSignalNoiseEnvelope( sig, gaus, noisy_signal):

    signal_envelope = np.abs(hilbert(sig))
    noisy_signal_envelope = np.abs(hilbert(noisy_signal))
    noise_envelope = np.abs(hilbert(gaus))

    # OK, make our plots. Let's scale up the time.
    tscale = 1.0E9
    
    f, axarr = plt.subplots(4)

    axarr[0].plot(t*tscale, sig)
    axarr[0].plot(t*tscale, signal_envelope)
    axarr[0].set_title("Signal")
    axarr[0].set_xlabel("Time (ns)")
    axarr[0].set_ylabel("Voltage (noise units)")

    axarr[1].plot(t*tscale, gaus)
    axarr[1].plot(t*tscale, noise_envelope)
    axarr[1].set_title("Noise")
    axarr[1].set_xlabel("Time (ns)")
    axarr[1].set_ylabel("Voltage (noise units)")

    axarr[2].plot(t, noisy_signal)
    axarr[2].plot(t, noisy_signal_envelope)
    axarr[2].set_title("Signal+Noise")
    axarr[2].set_xlabel("Time (ns)")
    axarr[2].set_ylabel("Voltage (noise units)")

    # Now plot the distribution of the data plus the analytic PDF.
    # Get the x-space that makes the most sense, 100 points from 1-99%
    rv = rice(amplitude/noise)
    x = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 100)

    # Histogram the data.
    axarr[3].hist(noisy_signal_envelope,
                  normed=True, histtype='stepfilled', alpha=0.2)
    # And plot the PDF on top.
    axarr[3].plot(x, rv.pdf(x))

    axarr[3].set_title("PDF of Signal+Noise")
    axarr[3].set_xlabel("Envelope amplitude (noise units)")
    axarr[3].set_ylabel("Probability")

    f.tight_layout()

    plt.show()

def plotFilteredDataEnvelope(noisy_signal, filtData):
    
    filtDataEnvelope = np.abs(hilbert(filtData))
    noisy_signal_envelope = np.abs(hilbert(noisy_signal))

    tscale = 1.0E9
    
    f, axarr = plt.subplots(3)
    axarr[0].plot(t*tscale, noisy_signal)
    axarr[0].plot(t*tscale, noisy_signal_envelope)
    axarr[0].set_xlabel("Time (ns)")
    axarr[0].set_ylabel("Voltage (noise units)")

    axarr[1].plot(t*tscale, filtData)
    axarr[1].plot(t*tscale, filtDataEnvelope)
    axarr[1].set_xlabel("Time (ns)")
    axarr[1].set_ylabel("Voltage (noise units)")

    rv=rice(3.6)
    x = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 100)
    axarr[2].hist(filtDataEnvelope,
                  normed=True, histtype='stepfilled', alpha=0.2)
    axarr[2].plot(x, rv.pdf(x))
    axarr[2].set_title("PDF of Signal+Noise")
    axarr[2].set_xlabel("Envelope amplitude (noise units)")
    axarr[2].set_ylabel("Probability")

    f.tight_layout()
    plt.show()

# we get back sig, nois, sig+noise, filtered
def riceVersusAmplitude():
    myRes = []
    myAmps = []
    riceRes = []
    for i in xrange(20):
        results = runRiceTest(amplitude=i*0.5)
        envRes = np.abs(hilbert(results[2]))
        myAmps.append(i*0.5)
        myRes.append(np.mean(envRes))
        riceRes.append(rice.stats(i*0.5, moments='m'))
    return (myAmps, myRes, riceRes)

def plotRiceVersusAmplitude(results):        
    f, (axarr0, axarr1) = plt.subplots(2)
    axarr0.plot(results[0], results[1])    
    axarr0.set_title('Envelope mean')
    axarr0.set_xlabel('Sine amplitude (noise units)')
    axarr0.set_ylabel('Mean (noise units)')
    axarr1.set_title('Rice mean')
    axarr1.plot(results[0], results[2])   
    axarr1.set_xlabel('Rice parameter')
    axarr1.set_ylabel('Mean')
    plt.tight_layout()
    plt.subplots_adjust()
    plt.show()

#plotSignalNoiseEnvelope(results[0], results[1], results[2])
#plotFilteredDataEnvelope(results[2], results[3])

#results = riceVersusAmplitude()
#plotRiceVersusAmplitude(results)

res = runRiceTest(amplitude=0)
print np.mean(np.abs(hilbert(res[1])))
