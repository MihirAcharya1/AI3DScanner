"""
Image Loader

Loads images for the computer vision pipeline.
"""

from pathlib import Path

import cv2
import numpy as np


class ImageLoader:
    """Loads images using OpenCV."""

    @staticmethod
    def load(path: Path) -> np.ndarray:

        image = cv2.imread(str(path))

        if image is None:
            raise FileNotFoundError(
                f"Unable to load image: {path}"
            )

        return image

    @staticmethod
    def to_rgb(image: np.ndarray) -> np.ndarray:

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

    @staticmethod
    def to_gray(image: np.ndarray) -> np.ndarray:

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )