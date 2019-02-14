#!/usr/bin/python

import csv
import numpy as np
from scipy.signal import tukey, lfilter, lfiltic
import prony

class Signal(object):
    def __init__(self,
                 filename='impulse.dat',
                 order=192,
                 window=None):
        self.filename = filename
        self.order = order
        if window == None:
            tuk1 = tukey(820, 0.024)
            tuk2 = tukey(820, 0.219)
            tuk1[400:820] = 0
            tuk2[0:400] = 0
            win = tuk1 + tuk2
            self.window = np.pad(win, (0,1024-820),'constant', constant_values=(0,0))
        else:
            self.window = window

        self.filter = None

    def initializeFilter(self):
        # Read impulse response.
        self.rawImpulseResponse = []
        with open(self.filename,'rb') as csvfile:
            reader = csv.reader(csvfile,delimiter=' ', quotechar='|')
            for row in reader:
                self.rawImpulseResponse.append(float(row[1]))
        # Window it.
        self.windowedImpulseResponse = self.rawImpulseResponse * self.window
        # Now normalize it.
        # This is what *we* call an impulse response.
        self.impulseResponse = self.windowedImpulseResponse/np.linalg.norm(self.windowedImpulseResponse)

        # Store the impulse peak normalization
        # This is what you normalize an impulse by.
        self.impulseNorm = (np.max(self.impulseResponse) - np.min(self.impulseResponse))/2
        
        # Generate an IIR from it.
        self.filter = prony.prony(self.impulseResponse,
                                  self.order,
                                  self.order)
        # And construct the initial conditions.
        self.filterState = lfiltic(self.filter[0],
                                   self.filter[1],
                                   np.zeros(len(self.filter[1]-1)),
                                   np.zeros(len(self.filter[0]-1)))
        

    def runFilter(self, data):
        arr, self.filterState = lfilter(self.filter[0],
                                        self.filter[1],
                                        data,
                                        zi=self.filterState)
        return arr
        
