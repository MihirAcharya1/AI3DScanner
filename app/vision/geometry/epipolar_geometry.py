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
            return [], None

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
            return [], None

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

    def estimate_pose(
        self,
        kp1,
        kp2,
        matches,
        camera_matrix,
    ):
        """
        Estimate camera pose directly from feature matches.

        Returns:
            R : Rotation matrix
            t : Translation vector
            inlier_matches : list
        """

        # Remove outliers first
        inlier_matches, _ = self.filter_matches(
            kp1,
            kp2,
            matches,
        )

        if len(inlier_matches) < 8:
            return None, None, []

        # Essential matrix
        E, _ = self.find_essential_matrix(
            kp1,
            kp2,
            inlier_matches,
            camera_matrix,
        )

        # Camera pose
        R, t, pose_mask = self.recover_camera_pose(
            E,
            kp1,
            kp2,
            inlier_matches,
            camera_matrix,
        )

        final_inliers = [
            inlier_matches[i]
            for i in range(len(inlier_matches))
            if pose_mask[i]
        ]

        return R, t, final_inliers
    
    def triangulate_points(
        self,
        kp1,
        kp2,
        matches,
        R,
        t,
        camera_matrix,
    ):
        """
        Triangulate 3D points from one image pair.
        """

        import numpy as np
        import cv2

        pts1 = np.float32(
            [kp1[m.queryIdx].pt for m in matches]
        ).T

        pts2 = np.float32(
            [kp2[m.trainIdx].pt for m in matches]
        ).T

        P1 = camera_matrix @ np.hstack(
            (
                np.eye(3),
                np.zeros((3, 1)),
            )
        )

        P2 = camera_matrix @ np.hstack(
            (
                R,
                t,
            )
        )

        points4d = cv2.triangulatePoints(
            P1,
            P2,
            pts1,
            pts2,
        )

        points3d = (
            points4d[:3] / points4d[3]
        ).T

        return points3d