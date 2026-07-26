class FeatureTrack:

    def __init__(self, track_id):

        self.track_id = track_id

        self.observations = []

    def add(self, image_index, keypoint_index):

        self.observations.append(
            (
                image_index,
                keypoint_index,
            )
        )

    def size(self):

        return len(self.observations)