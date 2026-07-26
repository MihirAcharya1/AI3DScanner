"""
Image Pair
"""


class ImagePair:

    def __init__(self, image1, image2):

        self.image1 = image1
        self.image2 = image2

        # Feature matching
        self.matches = []
        self.inlier_matches = []

        # Camera pose
        self.rotation = None
        self.translation = None

        # Geometry
        self.points3d = []

        # Statistics
        self.reprojection_error = 0.0

    def number_of_matches(self):

        return len(self.matches)

    def number_of_inliers(self):

        return len(self.inlier_matches)

    def __str__(self):

        return (
            f"Pair {self.image1}-{self.image2} "
            f"Matches={self.number_of_matches()} "
            f"Inliers={self.number_of_inliers()}"
        )