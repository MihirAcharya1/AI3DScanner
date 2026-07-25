"""
Epipolar Geometry
"""

import cv2
import numpy as np


class EpipolarGeometry:
    """Geometry operations for photogrammetry."""

    def filter_matches(self, kp1, kp2, matches):
        """
        Filter matches using RANSAC.

        Returns:
            inlier_matches : list
            mask : ndarray
        """

        if len(matches) < 8:
            raise RuntimeError(
                "Not enough matches for RANSAC."
            )

        pts1 = np.float32(
            [kp1[m.queryIdx].pt for m in matches]
        )

        pts2 = np.float32(
            [kp2[m.trainIdx].pt for m in matches]
        )

        fundamental_matrix, mask = cv2.findFundamentalMat(
            pts1,
            pts2,
            cv2.FM_RANSAC,
        )

        if fundamental_matrix is None:
            raise RuntimeError(
                "Fundamental Matrix estimation failed."
            )

        inlier_matches = [
            matches[i]
            for i in range(len(matches))
            if mask[i]
        ]

        return inlier_matches, mask


    def find_essential_matrix(
        self,
        kp1,
        kp2,
        matches,
        camera_matrix,
    ):

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
                "Essential Matrix estimation failed."
            )

        return E, mask


    def recover_camera_pose(
        self,
        E,
        kp1,
        kp2,
        matches,
        camera_matrix,
    ):

        pts1 = np.float32(
            [kp1[m.queryIdx].pt for m in matches]
        )

        pts2 = np.float32(
            [kp2[m.trainIdx].pt for m in matches]
        )

        _, R, t, mask = cv2.recoverPose(
            E,
            pts1,
            pts2,
            camera_matrix,
        )

        return R, t, mask