import numpy as np


class CloudMerger:

    def merge(self, clouds):

        merged = []

        for cloud in clouds:

            merged.extend(cloud)

        return np.asarray(
            merged,
            dtype=np.float64,
        )