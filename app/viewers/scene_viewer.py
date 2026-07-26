"""
Scene Viewer

Displays the reconstructed point cloud together with
the estimated camera trajectory.
"""

import open3d as o3d
import numpy as np


class SceneViewer:

    @staticmethod
    def create_camera(position, size=0.05):
        """
        Create a coordinate frame representing a camera.
        """

        camera = o3d.geometry.TriangleMesh.create_coordinate_frame(
            size=size
        )

        camera.translate(position)

        return camera

    @staticmethod
    def create_origin(size=0.10):
        """
        Create the world origin coordinate frame.
        """

        return o3d.geometry.TriangleMesh.create_coordinate_frame(
            size=size
        )

    @staticmethod
    def show(point_cloud, trajectory):
        """
        Display the complete reconstruction scene.

        Parameters
        ----------
        point_cloud : open3d.geometry.PointCloud

        trajectory : CameraTrajectory
        """

        geometries = []

        # -------------------------------------------------
        # World Origin
        # -------------------------------------------------

        geometries.append(
            SceneViewer.create_origin()
        )

        # -------------------------------------------------
        # Sparse Point Cloud
        # -------------------------------------------------

        geometries.append(point_cloud)

        # -------------------------------------------------
        # Cameras
        # -------------------------------------------------

        for camera in trajectory.cameras:

            geometries.append(

                SceneViewer.create_camera(

                    camera.position

                )

            )

        # -------------------------------------------------
        # Open3D Viewer
        # -------------------------------------------------

        o3d.visualization.draw_geometries(
            geometries,
            window_name="AI3DScanner Scene Viewer",
            width=1400,
            height=900,
        )