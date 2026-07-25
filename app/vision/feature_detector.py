"""
Feature Detector

Base class for all feature detection algorithms.
"""

import cv2
import numpy as np


class FeatureDetector:

    def __init__(self):

        self.detector = cv2.ORB_create(
            nfeatures=5000
        )

    def detect(
        self,
        image: np.ndarray,
    ):

        return self.detector.detectAndCompute(
            image,
            None,
        )