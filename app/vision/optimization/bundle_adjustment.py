import numpy as np

from app.vision.optimization.optimizer import Optimizer


class BundleAdjustment(Optimizer):
    """
    Placeholder Bundle Adjustment.
    """

    def optimize(
        self,
        camera_poses,
        points3d,
    ):

        print("\n========== BUNDLE ADJUSTMENT ==========")

        print(f"Cameras : {len(camera_poses)}")
        print(f"Points  : {len(points3d)}")

        print("\nOptimization completed (placeholder).\n")

        return camera_poses, points3d