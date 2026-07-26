from pathlib import Path

import numpy as np
from app.vision.camera import camera
from app.vision.image_loader import ImageLoader
from app.vision.feature_detector import FeatureDetector
from app.vision.matchers.brute_force_matcher import FeatureMatcher
from app.vision.geometry.epipolar_geometry import EpipolarGeometry
from app.vision.point_cloud.sparse_cloud import SparsePointCloud
from app.vision.optimization.bundle_adjustment import BundleAdjustment
from app.vision.camera.camera_trajectory import CameraTrajectory
from app.vision.camera.camera import Camera

class IncrementalReconstructor:

    def __init__(self, config):

        self.config = config
        
        self.camera_poses = []
        self.rotations = []
        self.translations = []

        self.loader = ImageLoader()
        self.bundle_adjustment = BundleAdjustment()
        self.trajectory = CameraTrajectory()

        self.detector = FeatureDetector(
            max_features=config.max_features
        )

        self.matcher = FeatureMatcher(
            matcher_type=config.matcher,
            ratio=config.ratio_test,
        )

        self.geometry = EpipolarGeometry()

        self.images = []
        self.gray_images = []

        self.keypoints = []
        self.descriptors = []

        self.matches = []
        self.filtered_matches = []
        self.cloud = SparsePointCloud()
        # self.points3d = []

    # ← ADD THIS HERE
    def load_images(self, folder):

        folder = Path(folder)

        self.images.clear()
        self.gray_images.clear()

        extensions = ("*.png", "*.jpg", "*.jpeg")

        for ext in extensions:
            for file in sorted(folder.glob(ext)):
                image = self.loader.load(file)
                self.images.append(image)
                self.gray_images.append(
                    self.loader.to_gray(image)
                )

        print(f"Loaded {len(self.images)} images.")

    # ← ADD THIS HERE
    def detect_features(self):

        self.keypoints.clear()
        self.descriptors.clear()

        for gray in self.gray_images:

            kp, des = self.detector.detect(gray)

            self.keypoints.append(kp)
            self.descriptors.append(des)

        print("Feature detection complete.")

    # ← ADD THIS HERE
    def match_features(self):

        self.matches.clear()

        for i in range(len(self.images) - 1):

            matches = self.matcher.match(
                self.descriptors[i],
                self.descriptors[i + 1],
            )

            self.matches.append(matches)

            print(
                f"Pair {i+1}: {len(matches)} matches"
            )
    
    def show_statistics(self):

        print("\n========== MULTI-VIEW ==========\n")

        print(f"Images : {len(self.images)}\n")

        for i, kp in enumerate(self.keypoints):

            print(
                f"Image {i+1:02d} : "
                f"{len(kp)} keypoints"
            )

        print()

        for i, matches in enumerate(self.matches):

            print(
                f"Pair {i+1:02d} : "
                f"{len(matches)} matches"
            )
            
    def estimate_camera_poses(self):

        self.camera_poses.clear()

        for i, matches in enumerate(self.matches):

            if len(matches) < 8:

                print(
                    f"Pair {i+1}: skipped (only {len(matches)} matches)"
                )

                continue

            kp1 = self.keypoints[i]
            kp2 = self.keypoints[i + 1]

            R, t, inliers = self.geometry.estimate_pose(
                kp1,
                kp2,
                matches,
                self.get_camera_matrix(),
            )
            if R is None:
                print(f"Pair {i+1}: skipped (insufficient inliers)")
                continue

            self.rotations.append(R)
            self.translations.append(t)
            camera = Camera(R, t)
            self.trajectory.add_camera(camera)

            print(
                f"Pair {i+1}: "
                f"{len(inliers)} inliers"
            )
    
    def get_camera_matrix(self):

        width = self.images[0].shape[1]
        height = self.images[0].shape[0]

        focal = max(width, height)

        return np.array(
            [
                [focal, 0, width / 2],
                [0, focal, height / 2],
                [0, 0, 1],
            ],
            dtype=np.float64,
        )
    
    def triangulate_pairs(self):

        # self.points3d.clear()
        self.cloud.clear()

        camera_matrix = self.get_camera_matrix()

        for i in range(len(self.rotations)):

            R = self.rotations[i]
            t = self.translations[i]

            kp1 = self.keypoints[i]
            kp2 = self.keypoints[i + 1]

            matches = self.matches[i]

            try:

                points = self.geometry.triangulate_points(
                    kp1,
                    kp2,
                    matches,
                    R,
                    t,
                    camera_matrix,
                )

                # self.points3d.extend(points)
                self.cloud.add_points(points)

                print(
                    f"Pair {i+1}: {len(points)} points"
                )

            except Exception as e:

                print(
                    f"Pair {i+1}: triangulation skipped ({e})"
                )
                
    def reconstruction_summary(self):

        print("\n========== SUMMARY ==========")

        print(f"Images        : {len(self.images)}")
        print(f"Camera Poses  : {len(self.trajectory.cameras)}")
        print(f"3D Points     : {len(self.cloud)}")
        
    def optimize(self):

        camera_poses = list(
            zip(
                self.rotations,
                self.translations,
            )
        )

        self.bundle_adjustment.optimize(
            camera_poses,
            self.cloud.to_numpy(),
        )