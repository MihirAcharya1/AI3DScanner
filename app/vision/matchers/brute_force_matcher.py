import cv2


class FeatureMatcher:

    def __init__(self, matcher_type="BF", ratio=0.75):

        self.ratio = ratio

        self.matcher = cv2.BFMatcher(
            cv2.NORM_HAMMING,
            crossCheck=False,
        )

    def match(self, des1, des2):

        if des1 is None or des2 is None:
            return []

        knn_matches = self.matcher.knnMatch(
            des1,
            des2,
            k=2,
        )

        good_matches = []

        for pair in knn_matches:

            if len(pair) != 2:
                continue

            m, n = pair

            if m.distance < self.ratio * n.distance:
                good_matches.append(m)

        return good_matches