"""
Parameter Update
"""

import numpy as np


class ParameterUpdater:

    def apply(
        self,
        parameters,
        delta,
        learning_rate=1.0,
    ):
        """
        Apply one optimization step.
        """

        parameters = np.asarray(
            parameters,
            dtype=np.float64,
        )

        delta = np.asarray(
            delta,
            dtype=np.float64,
        )

        return parameters - learning_rate * delta