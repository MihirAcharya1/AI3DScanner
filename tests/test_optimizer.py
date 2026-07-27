import numpy as np

from app.vision.optimization.optimizer import Optimizer


optimizer = Optimizer()


def residual(x):

    return np.array([
        x[0] - 5
    ])


result = optimizer.optimize_vector(
    np.array([20.0]),
    residual,
)

print()

print("Optimized Parameter")

print(result)