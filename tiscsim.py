class TISCSimulation():

    def __init__(self,
                 detector=None,
                 signal=None,
                 generator=None,
                 propagator=None,
                 digitizer=None,
                 trigger=None):
        self.detector = detector
        self.signal = signal
        self.generator = generator
        self.propagator = propagator
        self.digitizer = digitizer
        self.trigger = trigger
        
    def runOne(self):
        # The overall simulation is pretty simple:
        # 1) Generate an event.
        # 2) Create the signal.
        # 3) Propagate the event.
        # 4) Receive the signal.
        # 5) Digitize the signal.
        # 6) Trigger on the signal.

        # Generate the event - that is, create the
        # interaction location and velocity (at minimum).
        event = self.generator.generate()

        # Propagate the event to the detector. At minimum
        # just copy the interaction velocity to the
        # arrival direction.
        self.propagator.propagate(event, self.detector)
        
        # Create the signal for the event (no noise).
        self.signal.generate(self.detector, event)

        # Generate the interaction times at the detector.
        times = self.propagator.getTimes(self.event, self.detector)
        
        # Receive the signal. Create noise for each detector,
        # and offset the signal in time from detector to detector.
        self.detector.receiveSignal(event, times)

        # Digitize the signal
        self.digitizer.digitizeSignal(event)
        
        # Trigger.
        self.trigger.runTrigger(event)
        
