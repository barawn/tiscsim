import abc

# Template class. Don't actually use this class,
# inherit from this class and replace the propagate function.
# getTimes is a generic overridable function which
# returns the times that an event arrives at the
# detection points.
# For a simple detector (plane wave incident on
# fixed detection points) getTimes works fine here.
# For a more complicated detector (one in the transition region
# - i.e. a curved wavefront) this can be overridden to do proper
# propagation.
class Propagator():

    def __init__(self):
        return
        
    # Propagate takes the event from its interaction
    # point to the detector.
    @abc.abstractmethod
    def propagate(event=None, detector=None):
        pass

    # getTimes finds the arrival times incident at the
    # detector.
    def getTimes(event=None, detector=None):        
        # unitvector should be defined inside event here
        unitvector = event.getArrivalDirection()
        
        # Points is a list of a measurement points
        # in the geometry. It's a list of lists,
        # so it's functionally a 2-D array.
        # So ask the detector for them.
        points = detector.getDetectionPoints()

        # Dot product with the unit vector. This results in a 1-D array.
        projectedDistances = np.dot(points, unitvector)

        # Convert to time
        times = projectedDistances/scipy.constants.c

        # Done
        return times
    
