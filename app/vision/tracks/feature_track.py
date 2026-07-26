class FeatureTrack:

    """
    Represents one 3D feature observed in multiple images.
    """

    def __init__(self, track_id):

        self.track_id = track_id

        # List of observations
        self.observations = []

        # 3D point generated after triangulation
        self.point3d = None

    def add(
        self,
        image_index,
        keypoint_index,
        point2d,
    ):

        self.observations.append(
            {
                "image": image_index,
                "keypoint": keypoint_index,
                "point": point2d,
            }
        )

    def size(self):

        return len(self.observations)

    def images(self):

        return [
            obs["image"]
            for obs in self.observations
        ]

    def keypoints(self):

        return [
            obs["keypoint"]
            for obs in self.observations
        ]

    def points2d(self):

        return [
            obs["point"]
            for obs in self.observations
        ]

    def set_point3d(self, point3d):

        self.point3d = point3d

    def get_point3d(self):

        return self.point3d

    def __len__(self):

        return len(self.observations)

    def __repr__(self):

        return (
            f"FeatureTrack("
            f"id={self.track_id}, "
            f"observations={len(self.observations)}, "
            f"triangulated={self.point3d is not None})"
        )