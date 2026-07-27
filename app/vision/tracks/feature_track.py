"""
Feature Track
"""

import numpy as np

from app.vision.tracks.observation import Observation


class FeatureTrack:

    def __init__(self, track_id):

        self.track_id = track_id

        self.observations = []

        self.point3d = None

        self.error = 0.0

    def add(
        self,
        image_index,
        keypoint_index,
        point2d,
    ):

        observation = Observation(
            image_index,
            keypoint_index,
            point2d,
        )

        self.observations.append(
            observation
        )

    def set_point3d(self, point):

        self.point3d = np.asarray(
            point,
            dtype=np.float64,
        )
        
    def get_point3d(self):

        return self.point3d

    def number_of_observations(self):

        return len(
            self.observations
        )
        
        
    def size(self):

        return len(self.observations)

    def __len__(self):

        return len(
            self.observations
        )

    def __iter__(self):

        return iter(
            self.observations
        )