"""
3D Point Projector
"""

import cv2
import numpy as np


class Projector:

    def project(
        self,
        point3d,
        R,
        t,
        K,
    ):

        point3d = np.asarray(
            point3d,
            dtype=np.float64,
        ).reshape(1, 3)

        rvec, _ = cv2.Rodrigues(R)

        image_point, _ = cv2.projectPoints(
            point3d,
            rvec,
            t,
            K,
            None,
        )

        return image_point.reshape(2)