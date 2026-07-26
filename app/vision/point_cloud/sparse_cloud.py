import numpy as np


class SparsePointCloud:

    def __init__(self):

        self.points = []
        self.colors = []
    
    def __len__(self):
        return len(self.points)

    def add_points(self, points):

        if len(points):

            self.points.extend(points)

    def clear(self):

        self.points.clear()

    def to_numpy(self):

        return np.asarray(
            self.points,
            dtype=np.float64,
        )