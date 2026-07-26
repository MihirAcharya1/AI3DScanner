import numpy as np


class CameraModel:

    def __init__(self):

        self.fx = None
        self.fy = None

        self.cx = None
        self.cy = None

        self.distortion = np.zeros(5)

    def matrix(self):

        return np.array(
            [
                [self.fx, 0, self.cx],
                [0, self.fy, self.cy],
                [0, 0, 1],
            ],
            dtype=np.float64,
        )