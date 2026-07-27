import numpy as np
import cv2


class CameraModel:

    def __init__(self):

        self.fx = None
        self.fy = None

        self.cx = None
        self.cy = None

        self.distortion = np.zeros(5)

    def matrix(self):

        return np.array(
            [
                [self.fx, 0, self.cx],
                [0, self.fy, self.cy],
                [0, 0, 1],
            ],
            dtype=np.float64,
        )
    
    def project(
        self,
        point3d,
        R,
        t,
        K,
    ):
        """
        Project one 3D point into the image.
        """

        point3d = np.asarray(
            point3d,
            dtype=np.float64,
        ).reshape(1, 3)

        rvec, _ = cv2.Rodrigues(R)

        image_point, _ = cv2.projectPoints(
            point3d,
            rvec,
            t,
            K,
            self.distortion,
        )

        return image_point.reshape(2)