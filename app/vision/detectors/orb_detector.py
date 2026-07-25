"""
ORB Feature Detector
"""

import cv2
import numpy as np


class FeatureDetector:
    """ORB feature detector."""

    def __init__(self, nfeatures: int = 5000):
        self.detector = cv2.ORB_create(
            nfeatures=nfeatures
        )

    def detect(self, image: np.ndarray):
        """
        Detect keypoints and descriptors.
        """

        keypoints, descriptors = self.detector.detectAndCompute(
            image,
            None,
        )

        return keypoints, descriptors