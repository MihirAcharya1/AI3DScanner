"""
Reconstruction Pipeline

Coordinates the complete computer vision workflow.
"""

from pathlib import Path

from app.vision.image_loader import ImageLoader
from app.vision.feature_detector import FeatureDetector
from app.vision.matchers.brute_force_matcher import FeatureMatcher
from app.vision.geometry.epipolar_geometry import EpipolarGeometry
from app.vision.reconstruction.triangulator import Triangulator
from app.exporters.ply_exporter import PLYExporter
from app.config.reconstruction_config import ReconstructionConfig
import cv2
import numpy as np


class ReconstructionPipeline:
    """Main reconstruction pipeline."""

    def __init__(self, config: ReconstructionConfig | None = None):
        
        self.config = config or ReconstructionConfig()
        self.images = []
        self.image_paths = []
        self.gray_images = []

        self.features = []
        self.matches = []
        max_features=8000
        self.detector = FeatureDetector(max_features=self.config.max_features)
        self.matcher = FeatureMatcher(matcher_type=self.config.matcher,ratio=self.config.ratio_test,)
        self.geometry = EpipolarGeometry()
        self.triangulator = Triangulator()
        self.exporter = PLYExporter()
        self.filtered_matches = []
        self.camera_rotation = None
        self.camera_translation = None
        self.points3d = None

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
            
    def show_matches(self,  filtered=True):

        match_list = (
            self.filtered_matches
            if filtered and self.filtered_matches
            else self.matches
        )
        
        for i, matches in enumerate(match_list):

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
        
        if len(self.filtered_matches) == 0:
            raise RuntimeError(
            "Run filter_matches() first."
            )
            
        if len(self.features) < 2:
            return

        kp1, _ = self.features[0]
        kp2, _ = self.features[1]

        matches = self.matches[0]

        # Temporary camera matrix
        camera_matrix =  self.get_camera_matrix()

        E, _ = self.geometry.find_essential_matrix(
            kp1,
            kp2,
            matches,
            camera_matrix,
        )

        R, t, _ = self.geometry.recover_camera_pose(
            E,
            kp1,
            kp2,
            matches,
            camera_matrix,
        )
            
        self.camera_rotation = R
        self.camera_translation = t

        print("\nRotation Matrix\n")
        print(R)

        print("\nTranslation Vector\n")
        print(t)
        
    def filter_matches(self):

        self.filtered_matches.clear()

        for i in range(len(self.features) - 1):

            kp1, _ = self.features[i]
            kp2, _ = self.features[i + 1]

            matches = self.matches[i]

            inliers, mask = self.geometry.filter_matches(
                kp1,
                kp2,
                matches,
            )

            self.filtered_matches.append(inliers)

            print(
                f"Pair {i+1}: "
                f"{len(matches)} -> {len(inliers)} inliers"
            )
    
    def triangulate(self):

        kp1, _ = self.features[0]
        kp2, _ = self.features[1]

        matches = self.filtered_matches[0]

        camera_matrix =  self.get_camera_matrix()

        self.points3d = self.triangulator.triangulate(
            kp1,
            kp2,
            matches,
            self.camera_rotation,
            self.camera_translation,
            camera_matrix,
        )

        print(
            f"\nGenerated {len(self.points3d)} 3D points."
        )

    def export_sparse_cloud(self, filename):

        if self.points3d is None:
            raise RuntimeError(
                "Run triangulate() first."
            )

        self.exporter.export(
            self.points3d,
            filename,
        )
    def get_camera_matrix(self):

        return np.array(
            [
                [1000,0,640],
                [0,1000,360],
                [0,0,1],
            ],
            dtype=np.float64,
        )