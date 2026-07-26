import numpy as np


class CameraTrajectory:

    def __init__(self):

        self.cameras = []

    def add_camera(self, camera):

        self.cameras.append(camera)

    def positions(self):

        return np.array(
            [
                camera.position
                for camera in self.cameras
            ]
        )