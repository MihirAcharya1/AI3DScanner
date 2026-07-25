"""
Feature Matcher

Matches ORB descriptors between two images.
"""

import cv2
import numpy as np


class FeatureMatcher:
    """Matches ORB feature descriptors."""

    def __init__(self):

        self.matcher = cv2.BFMatcher(
            cv2.NORM_HAMMING,
            crossCheck=True,
        )

    def match(
        self,
        descriptors1: np.ndarray,
        descriptors2: np.ndarray,
    ):

        matches = self.matcher.match(
            descriptors1,
            descriptors2,
        )

        matches = sorted(
            matches,
            key=lambda x: x.distance,
        )

        return matches