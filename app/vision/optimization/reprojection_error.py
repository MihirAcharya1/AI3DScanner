"""
Reprojection Error
"""

import cv2
import numpy as np


class ReprojectionError:

    @staticmethod
    def compute(
        points3d,
        image_points,
        camera_matrix,
        rotation,
        translation,
    ):
        """
        Compute mean reprojection error.
        """

        if len(points3d) == 0:
            return 0.0

        rvec, _ = cv2.Rodrigues(rotation)

        projected, _ = cv2.projectPoints(
            np.asarray(points3d, dtype=np.float32),
            rvec,
            translation,
            camera_matrix,
            None,
        )

        projected = projected.reshape(-1, 2)

        image_points = np.asarray(
            image_points,
            dtype=np.float32,
        )

        error = np.linalg.norm(
            projected - image_points,
            axis=1,
        )

        return float(np.mean(error))