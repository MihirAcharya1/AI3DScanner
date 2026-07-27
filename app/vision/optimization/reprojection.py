"""
Reprojection Error
"""

import cv2
import numpy as np
from app.vision.optimization.projector import Projector

class ReprojectionError:
    
    def __init__(self):

        self.projector = Projector()

    def compute(
        self,
        points3d,
        observations,
        R,
        t,
        K,
    ):
        """
        Compute reprojection error.

        Parameters
        ----------
        points3d : Nx3 ndarray
        observations : Nx2 ndarray
        R : Rotation matrix
        t : Translation vector
        K : Camera matrix
        """

        if len(points3d) == 0:
            return []

        projected, _ = cv2.projectPoints(
            np.asarray(points3d),
            cv2.Rodrigues(R)[0],
            t,
            K,
            None,
        )

        projected = projected.reshape(-1, 2)

        errors = np.linalg.norm(
            projected -
            np.asarray(observations),
            axis=1,
        )

        return errors

    def statistics(self, errors):

        if len(errors) == 0:

            print()

            print("========== REPROJECTION ==========")

            print("No observations.")

            return

        print()

        print("========== REPROJECTION ==========")

        print(
            f"Observations : {len(errors)}"
        )

        print(
            f"Average Error : {np.mean(errors):.3f} px"
        )

        print(
            f"Median Error  : {np.median(errors):.3f} px"
        )

        print(
            f"Maximum Error : {np.max(errors):.3f} px"
        )
    
    def residual(
        self,
        point3d,
        observation,
        R,
        t,
        K,
    ):

        projected = self.projector.project(
            point3d,
            R,
            t,
            K,
        )

        return (
            observation
            -
            projected
        )
        
    def residual_norm(
        self,
        point3d,
        observation,
        R,
        t,
        K,
    ):

        residual = self.residual(
            point3d,
            observation,
            R,
            t,
            K,
        )

        return np.linalg.norm(
            residual
        )