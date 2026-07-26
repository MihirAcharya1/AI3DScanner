"""
Reprojection Error
"""

import cv2
import numpy as np


class ReprojectionError:

    def compute(
        self,
        point3d,
        point2d,
        camera_matrix,
        rotation,
        translation,
    ):
        """
        Compute reprojection error for a single 3D point.

        Parameters
        ----------
        point3d : ndarray (3,)
        point2d : tuple(x, y)
        camera_matrix : ndarray (3x3)
        rotation : ndarray (3x3)
        translation : ndarray (3x1)

        Returns
        -------
        float
        """

        rvec, _ = cv2.Rodrigues(rotation)

        projected, _ = cv2.projectPoints(
            point3d.reshape(1, 3),
            rvec,
            translation,
            camera_matrix,
            None,
        )

        projected = projected.reshape(2)

        point2d = np.array(
            point2d,
            dtype=np.float64,
        )

        error = np.linalg.norm(
            projected - point2d
        )

        return float(error)