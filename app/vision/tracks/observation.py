"""
Observation
"""

import numpy as np


class Observation:

    def __init__(
        self,
        image_index,
        keypoint_index,
        point2d,
    ):

        self.image_index = image_index

        self.keypoint_index = keypoint_index

        self.point2d = np.asarray(
            point2d,
            dtype=np.float64,
        )

    def __str__(self):

        return (
            f"Image {self.image_index} | "
            f"Keypoint {self.keypoint_index}"
        )