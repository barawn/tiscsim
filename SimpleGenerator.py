import Generator as gn
import numpy as np
import Event

# theta_min/theta_max are in proper theta
# Convenience function for setting the elevation range.
class SimpleGenerator(gn.Generator):
    def __init__(self,
                 seed=None,
                 theta_min=80.0, theta_max=130.0,
                 phi_min=0.0, phi_max=360.0):
        self.setThetaRange(theta_min, theta_max)
        self.setPhiRange(phi_min, phi_max)
        if seed != None:
            np.random.seed(seed)

    # Theta is defined as straight up = 0, straight down = 180
    # Elevation is defined as straight up = 90, straight down = -90
    # so do 90-el and flip max/min.
    def setElevationRange(self, el_min, el_max):
        self.setThetaRange(90.0-el_max, 90.0-el_min)
        
    def setThetaRange(self, theta_min, theta_max):
        # Compute min/max z (cos(theta))
        self.z = [ np.cos(np.radians(theta_min)), np.cos(np.radians(theta_max)) ]
    def setPhiRange(self, phi_min, phi_max):
        # Compute the min/max phi
        self.phi = [np.radians(phi_min), np.radians(phi_max)]

    def generate(self):        
        # Create event and give it its own RNG based on a random seed.
        event = Event.Event(np.random.randint(np.iinfo(np.uint32).max + 1))
        # Now draw its direction.
        rnd = event.rng.rand(2)
        # Shape to random-Z...
        rz = rnd[0] * (self.z[1] - self.z[0]) + self.z[0]
        # Shape to random-phi...
        rphi = rnd[1] * (self.phi[1]-self.phi[0]) + self.phi[0]
        # Now set the direction.
        # This is just cos(phi)sin(theta) sin(phi)sin(theta) cos(theta)
        # with rz = cos(theta). sqrt(1-rz*rz) is therefore sin(theta).
        uv = [ np.sqrt(1-rz*rz)*np.cos(rphi), np.sqrt(1-rz*rz)*np.sin(rphi),
               rz ]
        # And assign it to the event.
        event.setDirection(uv)
        # That's it, done.
        return event
    
