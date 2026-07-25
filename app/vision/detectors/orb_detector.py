import cv2


class ORBDetector:

    def __init__(self, max_features=5000):
        self.detector = cv2.ORB_create(
            nfeatures=max_features
        )

    def detect(self, gray_image):
        return self.detector.detectAndCompute(
            gray_image,
            None,
        )