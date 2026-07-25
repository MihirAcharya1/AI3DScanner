"""
Epipolar Geometry
"""

import cv2
import numpy as np


class EpipolarGeometry:

    def estimate_pose(
        self,
        kp1,
        kp2,
        matches,
        camera_matrix,
    ):
        """
        Estimate camera pose using the Essential Matrix.
        """

        pts1 = np.float32(
            [kp1[m.queryIdx].pt for m in matches]
        )

        pts2 = np.float32(
            [kp2[m.trainIdx].pt for m in matches]
        )

        E, mask = cv2.findEssentialMat(
            pts1,
            pts2,
            camera_matrix,
            method=cv2.RANSAC,
            prob=0.999,
            threshold=1.0,
        )

        if E is None:
            raise RuntimeError(
                "Essential Matrix could not be computed."
            )

        _, R, t, pose_mask = cv2.recoverPose(
            E,
            pts1,
            pts2,
            camera_matrix,
        )

        return R, t, pose_mask