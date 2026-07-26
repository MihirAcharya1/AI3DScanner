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
from app.vision.calibration.camera_model import CameraModel
from app.vision.reconstruction.multi_view_triangulator import (
    MultiViewTriangulator
)
from app.vision.optimization.reprojection_error import (
    ReprojectionError
)
from app.vision.optimization.point_filter import PointFilter
from app.vision.dense.dense_reconstructor import DenseReconstructor
from app.vision.models.image_pair import ImagePair


class IncrementalReconstructor:

    def __init__(self, config):

        self.config = config
        self.point_filter = PointFilter(max_error=3.0)
        self.camera_poses = []
        self.rotations = []
        self.translations = []
        self.graph = ImageGraph()
        self.loader = ImageLoader()
        self.bundle_adjuster = BundleAdjustment()
        self.trajectory = CameraTrajectory()
        self.dense = DenseReconstructor()

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
        self.reprojection_errors = []
        
        self.cloud = SparsePointCloud()
        self.track_builder = TrackBuilder()
        # self.points3d = []
        self.camera_model = CameraModel()
        self.multi_view = MultiViewTriangulator()
        self.reprojection = ReprojectionError()

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

                self.gray_images.append(
                    self.loader.to_gray(image)
                )

                # Create one graph node per image
                node = ImageNode(
                    index=len(self.images) - 1,
                    filename=file.name,
                )

                self.graph.add_node(node)

        # Initialize camera model from the first image
        if self.images:

            height, width = self.images[0].shape[:2]

            # Approximate intrinsics (will be replaced by calibration later)
            self.camera_model.fx = float(width)
            self.camera_model.fy = float(width)

            self.camera_model.cx = width / 2.0
            self.camera_model.cy = height / 2.0

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

            for j in range(i + 1, len(self.images)):

                matches = self.matcher.match(self.descriptors[i],self.descriptors[j],)

                self.graph.connect(i,j,matches,)

                pair = ImagePair(i, j)

                pair.matches = matches

                self.matches.append(pair)

                print(
                f"Pair {i}-{j}: "
                f"{len(matches)} matches"
                )  
                
                
    def show_statistics(self):

        print("\n========== MULTI-VIEW ==========\n")

        print(f"Images : {len(self.images)}\n")

        for i, kp in enumerate(self.keypoints):

            print(f"Image {i+1:02d} : " f"{len(kp)} keypoints")

        print()

        for pair in self.matches:

            print(
                f"Pair {pair.image1+1}-{pair.image2+1} : "
                f"{pair.number_of_matches()} matches"
            )

    def estimate_camera_poses(self):

        self.rotations.clear()
        self.translations.clear()
        self.trajectory.cameras.clear()

        camera_matrix = self.get_camera_matrix()

        for pair in self.matches:

            image1 = pair.image1
            image2 = pair.image2
            matches = pair.matches

            if len(matches) < 8:

                print(
                    f"Pair {image1+1}-{image2+1}: "
                    f"skipped ({len(matches)} matches)"
                )

                continue

            kp1 = self.keypoints[image1]
            kp2 = self.keypoints[image2]

            try:

                R, t, inlier_matches = self.geometry.estimate_pose(
                    kp1,
                    kp2,
                    matches,
                    camera_matrix,
                )

                if R is None:

                    print(
                        f"Pair {image1+1}-{image2+1}: "
                        "insufficient inliers"
                    )

                    continue

            # ----------------------------------
            # Store inside ImagePair
            # ----------------------------------

                pair.rotation = R
                pair.translation = t
                pair.inlier_matches = inlier_matches

            # ----------------------------------
            # Global containers (kept for compatibility)
            # ----------------------------------

                self.rotations.append(R)
                self.translations.append(t)

                self.trajectory.add_camera(
                    Camera(R, t)
                )

                print(
                    f"Pair {image1+1}-{image2+1}: "
                    f"{len(inlier_matches)} inliers"
                )

            except Exception as e:

                print(
                    f"Pair {image1+1}-{image2+1}: "
                    f"{e}"
                ) 
                   
                   
    def get_camera_matrix(self):

        return self.camera_model.matrix()
    
    # triangulate_pairs
    def triangulate_pairs(self):

        self.cloud.clear()

        camera_matrix = self.get_camera_matrix()

        for pair in self.matches:

            # Skip pairs without a valid pose
            if pair.rotation is None or pair.translation is None:
                continue

            image1 = pair.image1
            image2 = pair.image2

            kp1 = self.keypoints[image1]
            kp2 = self.keypoints[image2]

            # Use RANSAC inliers if available
            matches = (
                pair.inlier_matches
                if pair.inlier_matches
                else pair.matches
            )

            if len(matches) < 2:
                continue

            try:

                points = self.geometry.triangulate_points(
                    kp1,
                    kp2,
                    matches,
                    pair.rotation,
                    pair.translation,
                    camera_matrix,
                )

            # Store inside ImagePair
                pair.points3d = points

            # Add to global cloud
                self.cloud.add_points(points)

                print(
                    f"Pair {image1+1}-{image2+1}: "
                    f"{len(points)} points"
                )

            except Exception as e:

                print(
                    f"Pair {image1+1}-{image2+1}: "
                    f"triangulation skipped ({e})"
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
        
    def triangulate_tracks(self):

        self.points3d = self.multi_view.triangulate(
            self.track_builder.tracks,
            self.get_camera_matrix(),
            self.rotations,
            self.translations,
        )
        
    def compute_reprojection_errors(self):

        self.reprojection_errors.clear()

        if not self.rotations:
            return

        camera_matrix = self.get_camera_matrix()

        for track in self.track_builder.tracks:

            point3d = track.get_point3d()

            if point3d is None:
                continue

            for obs in track.observations:

                image = obs["image"]

                if image >= len(self.rotations):
                    continue

                error = self.reprojection.compute(
                    point3d,
                    obs["point"],
                    camera_matrix,
                    self.rotations[image],
                    self.translations[image],
                )

                self.reprojection_errors.append(error)

        print()
        print("========== REPROJECTION ==========")

        if self.reprojection_errors:

            print(
                f"Observations : {len(self.reprojection_errors)}"
            )

            print(
                f"Average Error : "
                f"{sum(self.reprojection_errors)/len(self.reprojection_errors):.3f} px"
            )

            print(
                f"Maximum Error : "
                f"{max(self.reprojection_errors):.3f} px"
            )
            
    def filter_sparse_points(self):

        self.track_builder.tracks = (
            self.point_filter.filter_tracks(
                self.track_builder.tracks
            )
        )
        
    def dense_reconstruction(self):

        self.dense.depth_maps.clear()

        for i in range(len(self.gray_images) - 1):

            self.dense.compute_depth(
                self.gray_images[i],
                self.gray_images[i + 1],
            )

        self.dense.summary()