# template for a detector class.

class Detector(object):
    def __init__(self, geometry=None):
        self.geometry = geometry

    def getDetectionPoints(self):
        return self.geometry.getPoints()

    
