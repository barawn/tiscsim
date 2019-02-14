import abc
#
# Wrapper class. Any real simulation imports its own geometry class,
# but the main simulation only knows about the wrapper.
#
class Geometry(object):

    @abc.abstractmethod
    def getPoints():
        pass

    
