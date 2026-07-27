"""
Residual Computation
"""

import numpy as np


class ResidualComputer:

    def compute(
        self,
        observations,
        projections,
    ):
        """
        Compute residual vectors.

        Parameters
        ----------
        observations : Nx2
        projections : Nx2
        """

        observations = np.asarray(
            observations,
            dtype=np.float64,
        )

        projections = np.asarray(
            projections,
            dtype=np.float64,
        )

        return observations - projections

    def rms(
        self,
        residuals,
    ):

        residuals = np.asarray(
            residuals,
            dtype=np.float64,
        )

        if residuals.size == 0:
            return 0.0

        return np.sqrt(
            np.mean(
                residuals ** 2
            )
        )