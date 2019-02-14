import numpy as np

class Event(object):
    def __init__(self, seed=None):
        if seed == None:
            seed = np.random.randint(np.iinfo(np.uint32).max+1)
        self.seed = seed
        self.rng = np.random.RandomState(seed)

    # expand this...
    def setDirection(self, vector):
        self.direction = vector

    # Convenience functions. Should see if there's a 3D vector class
    # somewhere.
    def getAngles(self):
        return [ self.getTheta(), self.getPhi() ]

    def getPhi(self):
        return np.arctan2(self.direction[0], self.direction[1])

    def getTheta(self):
        return np.arccos(self.direction[2])
    
    def getElevation(self):
        return np.pi/2 - self.getTheta()
    
