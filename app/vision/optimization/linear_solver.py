"""
Linear Solver
"""

import numpy as np


class LinearSolver:

    def solve(
        self,
        J,
        residuals,
    ):
        """
        Solve normal equations:
        (JᵀJ)Δ = Jᵀr
        """

        JT = J.T

        H = JT @ J

        g = JT @ residuals

        try:

            delta = np.linalg.solve(
                H,
                g,
            )

        except np.linalg.LinAlgError:

            delta = np.linalg.pinv(
                H
            ) @ g

        return delta