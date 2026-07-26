"""
Dense Reconstruction
"""

import cv2
import numpy as np


class DenseReconstructor:

    def __init__(self):

        self.depth_maps = []
        self.point_cloud = None

    def compute_depth(self, left, right):

        # ----------------------------
        # Convert to grayscale
        # ----------------------------

        if len(left.shape) == 3:
            left = cv2.cvtColor(
                left,
                cv2.COLOR_BGR2GRAY,
            )

        if len(right.shape) == 3:
            right = cv2.cvtColor(
                right,
                cv2.COLOR_BGR2GRAY,
            )

        # ----------------------------
        # Ensure uint8
        # ----------------------------

        if left.dtype != np.uint8:
            left = left.astype(np.uint8)

        if right.dtype != np.uint8:
            right = right.astype(np.uint8)

        # ----------------------------
        # Make both images same size
        # ----------------------------

        if left.shape != right.shape:

            h = min(left.shape[0], right.shape[0])
            w = min(left.shape[1], right.shape[1])

            left = cv2.resize(
                left,
                (w, h),
            )

            right = cv2.resize(
                right,
                (w, h),
            )

        # ----------------------------
        # Stereo Matcher
        # ----------------------------

        stereo = cv2.StereoSGBM_create(

            minDisparity=0,

            numDisparities=128,

            blockSize=5,

            P1=8 * 3 * 5 ** 2,

            P2=32 * 3 * 5 ** 2,

            disp12MaxDiff=1,

            uniquenessRatio=10,

            speckleWindowSize=100,

            speckleRange=32,

            preFilterCap=63,

            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY,
        )

        disparity = stereo.compute(
            left,
            right,
        ).astype(np.float32)

        disparity /= 16.0

        self.depth_maps.append(disparity)

        return disparity

    def summary(self):

        print()

        print("========== DENSE RECONSTRUCTION ==========")

        print(
            f"Depth Maps : {len(self.depth_maps)}"
        )