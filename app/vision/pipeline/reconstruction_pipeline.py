"""
Reconstruction Pipeline

Coordinates the complete computer vision workflow.
"""

from pathlib import Path

from app.vision.image_loader import ImageLoader
from app.vision.detectors.orb_detector import FeatureDetector
from app.vision.matchers.brute_force_matcher import FeatureMatcher
from app.vision.geometry.epipolar_geometry import EpipolarGeometry
import cv2
import numpy as np


class ReconstructionPipeline:
    """Main reconstruction pipeline."""

    def __init__(self):
        self.images = []
        self.image_paths = []
        self.gray_images = []

        self.features = []
        self.matches = []

        self.detector = FeatureDetector()
        self.matcher = FeatureMatcher()
        self.geometry = EpipolarGeometry()

    def load_images(self, folder: str):

        folder = Path(folder)

        extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp")

        self.image_paths.clear()
        self.images.clear()
        self.gray_images.clear()

        for ext in extensions:
            self.image_paths.extend(folder.glob(ext))

        self.image_paths = sorted(self.image_paths)

        if len(self.image_paths) < 2:
            raise RuntimeError("Need at least two images.")

        for path in self.image_paths:

            image = ImageLoader.load(path)

            self.images.append(image)
            self.gray_images.append(
                ImageLoader.to_gray(image)
            )

    def detect_features(self):

        self.features.clear()

        for gray in self.gray_images:

            kp, des = self.detector.detect(gray)

            self.features.append((kp, des))

    def match_features(self):

        self.matches.clear()

        for i in range(len(self.features) - 1):

            kp1, des1 = self.features[i]
            kp2, des2 = self.features[i + 1]

            matches = self.matcher.match(des1, des2)

            self.matches.append(matches)
            
    def show_statistics(self):

        print("\n========== PROJECT ==========\n")

        print(f"Images : {len(self.images)}")

        print()

        for i, (kp, des) in enumerate(self.features):

            print(
                f"{self.image_paths[i].name:<20}"
                f"Keypoints: {len(kp)}"
            )

        print()

        for i, matches in enumerate(self.matches):

            print(
                f"{self.image_paths[i].name}"
                f" <-> "
                f"{self.image_paths[i+1].name}"
            )

            print(
                f"Matches : {len(matches)}\n"
            )
            
    def show_matches(self):

        for i, matches in enumerate(self.matches):

            kp1, _ = self.features[i]
            kp2, _ = self.features[i + 1]

            result = cv2.drawMatches(

                self.images[i],
                kp1,

                self.images[i + 1],
                kp2,

                matches[:100],

                None,

                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
            )

            cv2.imshow(
                f"Match {i+1}",
                result,
            )

            cv2.waitKey(0)

        cv2.destroyAllWindows()
    
    def estimate_camera_pose(self):

        if len(self.features) < 2:
            return

        kp1, _ = self.features[0]
        kp2, _ = self.features[1]

        matches = self.matches[0]

        # Temporary camera matrix
        camera_matrix = np.array(
            [
                [1000, 0, 640],
                [0, 1000, 360],
                [0, 0, 1],
            ],
            dtype=np.float64,
        )

        R, t, mask = self.geometry.estimate_pose(
            kp1,
            kp2,
            matches,
            camera_matrix,
        )

        print("\nRotation Matrix\n")
        print(R)

        print("\nTranslation Vector\n")
        print(t)