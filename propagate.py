#
# Simple projection of a plane wave onto a set of measurement
# points.
#
# Modified from E. Oberla's 'delays.py' script.
#

import numpy as np
import scipy.constants

'''
propagate: computes propagation times for a planewave to a set of
           measurement points.
           returns an array of times, in seconds.
'''
def propagate(points, theta, phi):
    '''
    points: Measurement points. List of x,y,z arrays. 
            (e.g. ( (x0,x1,x2),(y0,y1,y2),(z0,z1,z2)) )
    theta: elevation angle (0 = horizontal)
    phi: azimuthal angle
    '''

    # Compute the unit vector for the incoming direction.
    # Need to flip it for it to be incoming: (theta, phi) = (45 deg, 0)
    # gives (0.707, 0, 0.707) - e.g. (+x, +z), whereas we want (-x, -z).
    uv_x = -1.0*np.cos(np.radians(theta)) * np.cos(np.radians(phi))
    uv_y = -1.0*np.cos(np.radians(theta)) * np.sin(np.radians(phi))
    uv_z = -1.0*np.sin(np.radians(theta))

    # Compute the dot products of the unit vector with the measurement points.
    dotproduct = (points[0] * uv_x) + (points[1]*uv_y) + (point[2]*uv_z)

    # Convert to time
    times = dotproduct/scipy.constants.c
    
    # Done.
    return times
