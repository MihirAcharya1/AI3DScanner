import numpy as np

from app.vision.optimization.optimizer import Optimizer
from app.vision.optimization.reprojection_error import (
    ReprojectionError,
)
from app.vision.optimization.camera_parameters import CameraParameters
from app.vision.calibration.camera_model import CameraModel
from app.vision.optimization.jacobian import JacobianComputer
from app.vision.optimization.linear_solver import LinearSolver

class BundleAdjustment(Optimizer):
    """
    Bundle Adjustment Framework
    """
    def __init__(self):
        super().__init__()
        self.camera_parameters = CameraParameters()
        self.camera_model = CameraModel()
        self.reprojection = ReprojectionError()
        self.jacobian = JacobianComputer()
        self.linear_solver = LinearSolver()
         
    def optimize(
        self,
        camera_poses,
        points3d,
        tracks,
        camera_matrix,
    ):

        print()

        print("========== BUNDLE ADJUSTMENT ==========")

        print(f"Cameras : {len(camera_poses)}")
        print(f"Points  : {len(points3d)}")

        parameters = self.create_parameter_vector(
            camera_poses,
            points3d,
        )

        print()

        print(
            f"Optimization Variables : {len(parameters)}"
        )

        print()

        print("Running Gauss-Newton...")

        for iteration in range(5):

            parameters, residuals = self.optimize_iteration(
                parameters,
                tracks,
                len(camera_poses),
                camera_matrix,
            )

            rms = np.sqrt(
                np.mean(residuals ** 2)
            )

            print(
                f"Iteration {iteration+1} "
                f"RMS Error = {rms:.3f}"
            )

        residuals = self.objective_function(
            parameters,
            tracks,
            len(camera_poses),
            camera_matrix,
        )

        print(
            f"Initial Residual Count : {len(residuals)}"
        )

        return camera_poses, points3d

    def pack_cameras(self, camera_poses):

        parameters = []

        for R, t in camera_poses:

            parameters.append(
                self.camera_parameters.pack(R, t)
            )

        return parameters
    
    def unpack_cameras(self, parameters):

        poses = []

        for p in parameters:

            poses.append(
                self.camera_parameters.unpack(p)
            )

        return poses
    
    def flatten_points(self, points3d):

        if len(points3d) == 0:
            return np.array([], dtype=np.float64)

        return np.asarray(
            points3d,
            dtype=np.float64,
        ).reshape(-1)


    def unflatten_points(self, vector):

        if len(vector) == 0:
            return []

        return vector.reshape(-1, 3)
    
    def create_parameter_vector(
        self,
        camera_poses,
        points3d,
    ):

        parameters = []

        for pose in camera_poses:

            R, t = pose

            parameters.extend(
                self.camera_parameters.pack(
                R,
                t,
            )
            )

        parameters.extend(
            self.flatten_points(
                points3d
            )
        )

        return np.asarray(
            parameters,
            dtype=np.float64,
        )

    def split_parameter_vector(
        self,
        parameters,
        number_of_cameras,
    ):

        parameters = np.asarray(
            parameters,
            dtype=np.float64,
        )

        camera_size = number_of_cameras * 6

        camera_vector = parameters[:camera_size]

        point_vector = parameters[camera_size:]

        cameras = []

        for i in range(number_of_cameras):

            start = i * 6

            end = start + 6

            cameras.append(
                self.camera_parameters.unpack(
                    camera_vector[start:end]
                )
            )

        points = self.unflatten_points(
            point_vector
        )

        return cameras, points
    
    def compute_residuals(
        self,
        tracks,
        rotations,
        translations,
        camera_matrix,
    ):

        residuals = []

        for track in tracks:

            point3d = track.get_point3d()

            if point3d is None:
                continue

            for observation in track.observations:

                image = observation.image_index

                if image >= len(rotations):
                    continue

                projected = self.camera_model.project(
                    point3d,
                    rotations[image],
                    translations[image],
                    camera_matrix,
                )

                residual = (
                    observation.point2d
                    - projected
                )

                residuals.extend(
                    residual.tolist()
                )

        return np.asarray(
            residuals,
            dtype=np.float64,
        )
        
    def objective_function(
        self,
        parameters,
        tracks,
        camera_count,
        camera_matrix,
    ):

        cameras, points = self.split_parameter_vector(
            parameters,
            camera_count,
        )

        rotations = []
        translations = []

        for R, t in cameras:
            rotations.append(R)
            translations.append(t)

        # Assign optimized points back to tracks
        point_index = 0

        print(f"Tracks: {len(tracks)}")
        for track in tracks:

            if point_index >= len(points):
                break

            track.set_point3d(
                points[point_index]
            )

            point_index += 1
        residuals = self.compute_residuals(
            tracks,
            rotations,
            translations,
            camera_matrix,
        )
        print(f"Residuals: {len(residuals)}")
        return residuals
    
    def optimize_iteration(
        self,
        parameters,
        tracks,
        camera_count,
        camera_matrix,
    ):
        """
        Perform one Gauss-Newton optimization iteration.
        """

        residual_function = lambda p: self.objective_function(
            p,
            tracks,
            camera_count,
            camera_matrix,
        )

        residuals = residual_function(parameters)

        J = self.jacobian.compute(
            residual_function,
            parameters,
        )   

        delta = self.linear_solver.solve(
            J,
            residuals,
        )

        new_parameters = parameters + delta

        return new_parameters, residuals