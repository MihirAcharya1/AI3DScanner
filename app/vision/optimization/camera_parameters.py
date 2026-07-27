"""
Camera Parameters
"""

import cv2
import numpy as np


class CameraParameters:

    @staticmethod
    def pack(R, t):
        """
        Convert camera pose to parameter vector.
        """

        rvec, _ = cv2.Rodrigues(R)

        return np.hstack(
            (
                rvec.flatten(),
                t.flatten(),
            )
        )

    @staticmethod
    def unpack(parameters):
        """
        Convert parameter vector back to camera pose.
        """

        parameters = np.asarray(
            parameters,
            dtype=np.float64,
        )

        rvec = parameters[:3]

        t = parameters[3:].reshape(3, 1)

        R, _ = cv2.Rodrigues(rvec)

        return R, t