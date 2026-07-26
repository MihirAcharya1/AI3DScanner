class Optimizer:
    """
    Base optimization interface.
    """

    def optimize(
        self,
        camera_poses,
        points3d,
    ):
        raise NotImplementedError