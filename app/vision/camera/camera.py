import numpy as np


class Camera:

    def __init__(self, R, t):

        self.rotation = R
        self.translation = t

    @property
    def position(self):

        return (-self.rotation.T @ self.translation).flatten()