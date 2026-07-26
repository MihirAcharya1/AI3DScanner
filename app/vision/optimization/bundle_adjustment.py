import numpy as np

from app.vision.optimization.optimizer import Optimizer
from app.vision.optimization.reprojection_error import (
    ReprojectionError,
)


class BundleAdjustment(Optimizer):
    """
    Bundle Adjustment Framework
    """

    def optimize(
        self,
        camera_poses,
        points3d,
        image_points=None,
        camera_matrix=None,
    ):

        print("\n========== BUNDLE ADJUSTMENT ==========")

        print(f"Cameras : {len(camera_poses)}")
        print(f"Points  : {len(points3d)}")

        # Compute reprojection error if data is available
        if (
            image_points is not None
            and camera_matrix is not None
            and len(camera_poses) > 0
            and len(points3d) > 0
        ):

            rotation, translation = camera_poses[0]

            error = ReprojectionError.compute(
                points3d,
                image_points,
                camera_matrix,
                rotation,
                translation,
            )

            print(f"Reprojection Error : {error:.4f}")

        print("\nOptimization completed (framework).\n")

        return camera_poses, points3d