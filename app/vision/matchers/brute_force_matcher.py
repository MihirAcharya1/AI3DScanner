"""
Brute Force Matcher
"""

import cv2
import numpy as np


class FeatureMatcher:
    """Matches ORB descriptors using Brute Force."""

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
        if descriptors1 is None or descriptors2 is None:
            return []

        matches = self.matcher.match(
            descriptors1,
            descriptors2,
        )

        matches = sorted(
            matches,
            key=lambda m: m.distance,
        )

        return matches