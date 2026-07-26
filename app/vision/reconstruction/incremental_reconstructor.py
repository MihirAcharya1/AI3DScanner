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
from app.vision.graph.image_graph import ImageGraph
from app.vision.graph.image_node import ImageNode
from app.vision.graph.feature_graph_builder import FeatureGraphBuilder
from app.vision.camera.camera import Camera
from app.vision.graph.graph_filter import GraphFilter
from app.vision.tracks.track_builder import TrackBuilder


class IncrementalReconstructor:

    def __init__(self, config):

        self.config = config

        self.camera_poses = []
        self.rotations = []
        self.translations = []
        self.graph = ImageGraph()
        self.loader = ImageLoader()
        self.bundle_adjuster = BundleAdjustment()
        self.trajectory = CameraTrajectory()

        self.detector = FeatureDetector(max_features=config.max_features)

        self.matcher = FeatureMatcher(
            matcher_type=config.matcher,
            ratio=config.ratio_test,
        )
        self.graph_builder = FeatureGraphBuilder(self.matcher)
        
        self.graph_filter = GraphFilter(min_matches=10)

        self.geometry = EpipolarGeometry()

        self.images = []
        self.gray_images = []

        self.keypoints = []
        self.descriptors = []

        self.matches = []
        self.filtered_matches = []
        self.cloud = SparsePointCloud()
        self.track_builder = TrackBuilder()
        # self.points3d = []

    # ← ADD THIS HERE


    def load_images(self, folder):

        folder = Path(folder)

        self.images.clear()
        self.gray_images.clear()

        # Reset graph for a new project
        self.graph = ImageGraph()

        extensions = ("*.png", "*.jpg", "*.jpeg")

        for ext in extensions:
            for file in sorted(folder.glob(ext)):

                image = self.loader.load(file)

                self.images.append(image)

                self.gray_images.append(self.loader.to_gray(image))

                # Create one graph node per image
                node = ImageNode(
                    index=len(self.images) - 1,
                    filename=file.name,
                )

                self.graph.add_node(node)

        print(f"Loaded {len(self.images)} images.")

    # ← ADD THIS HERE
    def detect_features(self):

        self.keypoints.clear()
        self.descriptors.clear()

        for i, gray in enumerate(self.gray_images):

            kp, des = self.detector.detect(gray)

            # Store in existing lists
            self.keypoints.append(kp)
            self.descriptors.append(des)

            # Store inside the Image Graph
            self.graph.nodes[i].keypoints = kp
            self.graph.nodes[i].descriptors = des

        print("Feature detection complete.")

    # ← ADD THIS HERE
    def match_features(self):

        self.matches.clear()

        for i in range(len(self.images) - 1):

            matches = self.matcher.match(
                self.descriptors[i],
                self.descriptors[i + 1],
            )

            # Store in existing list
            self.matches.append(matches)

            # Store inside the Image Graph
            self.graph.connect(
                i,
                i + 1,
                matches,
            )

            print(f"Pair {i+1}: {len(matches)} matches")
            
    def show_statistics(self):

        print("\n========== MULTI-VIEW ==========\n")

        print(f"Images : {len(self.images)}\n")

        for i, kp in enumerate(self.keypoints):

            print(f"Image {i+1:02d} : " f"{len(kp)} keypoints")

        print()

        for i, matches in enumerate(self.matches):

            print(f"Pair {i+1:02d} : " f"{len(matches)} matches")

    def estimate_camera_poses(self):

        self.camera_poses.clear()

        for i, matches in enumerate(self.matches):

            if len(matches) < 8:

                print(f"Pair {i+1}: skipped (only {len(matches)} matches)")

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

            print(f"Pair {i+1}: " f"{len(inliers)} inliers")

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

                print(f"Pair {i+1}: {len(points)} points")

            except Exception as e:

                print(f"Pair {i+1}: triangulation skipped ({e})")

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

        self.bundle_adjuster.optimize(
            camera_poses,
            self.cloud.to_numpy(),
        )

    def build_feature_graph(self):

        print()

        print("========== GRAPH ==========")

        self.graph_builder.build(
            self.graph
        )
    
    def filter_graph(self):

        self.graph_filter.filter(
            self.graph
        )
        
    def build_tracks(self):

        self.track_builder.build(
            self.graph
        )
        
    
    def run_bundle_adjustment(self):

        print()

        print("Running Bundle Adjustment...")

        if len(self.rotations) == 0:

            print("No camera poses available.")

            return

        camera_poses = list(
            zip(
                self.rotations,
                self.translations,
            )
        )

        camera_poses, points3d = (
            self.bundle_adjuster.optimize(
                camera_poses,
                self.cloud.to_numpy(),
            )
        )

        self.rotations = [
            pose[0]
            for pose in camera_poses
        ]

        self.translations = [
            pose[1]
            for pose in camera_poses
        ]