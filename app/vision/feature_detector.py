from app.vision.detectors.orb_detector import ORBDetector


class FeatureDetector:

    def __init__(self, max_features=5000):
        self.detector = ORBDetector(max_features)

    def detect(self, gray_image):
        return self.detector.detect(gray_image)