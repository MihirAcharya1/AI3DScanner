"""
Triangulator
"""

import cv2
import numpy as np


class Triangulator:

    def triangulate(
        self,
        kp1,
        kp2,
        matches,
        R,
        t,
        camera_matrix,
    ):
        """
        Triangulate 3D points from two camera views.
        """

        pts1 = np.float32(
            [kp1[m.queryIdx].pt for m in matches]
        ).T

        pts2 = np.float32(
            [kp2[m.trainIdx].pt for m in matches]
        ).T

        P1 = camera_matrix @ np.hstack(
            (
                np.eye(3),
                np.zeros((3, 1))
            )
        )

        P2 = camera_matrix @ np.hstack(
            (
                R,
                t
            )
        )

        points4d = cv2.triangulatePoints(
            P1,
            P2,
            pts1,
            pts2,
        )

        points3d = (
            points4d[:3] /
            points4d[3]
        ).T

        return points3d