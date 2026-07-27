import numpy as np


class JacobianComputer:

    def compute(
        self,
        residual_function,
        parameters,
        epsilon=1e-6,
    ):
        """
        Numerical Jacobian.
        """

        parameters = parameters.astype(np.float64)

        residuals = residual_function(parameters)

        J = np.zeros(
            (
                len(residuals),
                len(parameters),
            ),
            dtype=np.float64,
        )

        for i in range(len(parameters)):

            perturbed = parameters.copy()

            perturbed[i] += epsilon

            residuals2 = residual_function(
                perturbed
            )

            J[:, i] = (
                residuals2 - residuals
            ) / epsilon

        return J