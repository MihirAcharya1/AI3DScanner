"""
Optimization Base Class
"""

import numpy as np
from app.vision.optimization.residuals import ResidualComputer
from app.vision.optimization.jacobian import JacobianComputer
from app.vision.optimization.linear_solver import LinearSolver
from app.vision.optimization.parameter_update import ParameterUpdater

class Optimizer:
    """
    Base optimizer for Bundle Adjustment.
    """

    def __init__(self):

        self.max_iterations = 20

        self.tolerance = 1e-6
        
        self.residuals = ResidualComputer()
        
        self.jacobian = JacobianComputer()
        
        self.linear_solver = LinearSolver()
        
        self.parameter_updater = ParameterUpdater()

    def compute_cost(
        self,
        residuals,
    ):
        """
        Sum of squared residuals.
        """

        residuals = np.asarray(
            residuals,
            dtype=np.float64,
        )

        return 0.5 * np.sum(
            residuals ** 2
        )

    def convergence(
        self,
        old_cost,
        new_cost,
    ):

        return abs(
            old_cost - new_cost
        ) < self.tolerance
    
    def evaluate(
        self,
        observations,
        projections,
    ):

        residuals = self.residuals.compute(
            observations,
            projections,
        )

        rms = self.residuals.rms(
            residuals
        )

        cost = self.compute_cost(
            residuals
        )

        return rms, cost
    
    def compute_jacobian(
        self,
        function,
        parameters,
    ):

        return self.jacobian.numerical(
            function,
            parameters,
        )
        
    def solve(
        self,
        J,
        residuals,
    ):

        return self.linear_solver.solve(
            J,
            residuals,
        )
        
    def update(
        self,
        parameters,
        delta,
    ):

        return self.parameter_updater.apply(
            parameters,
            delta,
        )
    
    def optimize_vector(
        self,
        parameters,
        function,
    ):

        parameters = np.asarray(
            parameters,
            dtype=np.float64,
        )

        for iteration in range(
            self.max_iterations
        ):

            residual = np.asarray(
                function(parameters),
                dtype=np.float64,
            )

            cost = self.compute_cost(
                residual
            )

            J = self.compute_jacobian(
                function,
                parameters,
            )

            delta = self.solve(
                J,
                residual,
            )

            parameters = self.update(
                parameters,
                delta,
            )

            print(
                f"Iteration {iteration+1:02d} "
                f"Cost={cost:.6f}"
            )

            if np.linalg.norm(delta) < self.tolerance:

                print("Converged.")

                break

        return parameters