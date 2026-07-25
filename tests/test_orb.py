from pathlib import Path

import cv2

from app.vision.image_loader import ImageLoader
from app.vision.detectors import FeatureDetector


image_path = Path("examples/image1.jpeg")

image = ImageLoader.load(image_path)

gray = ImageLoader.to_gray(image)

detector = FeatureDetector()

keypoints, descriptors = detector.detect(gray)

print(f"Keypoints: {len(keypoints)}")

output = cv2.drawKeypoints(
    image,
    keypoints,
    None,
)

cv2.imshow(
    "ORB Features",
    output,
)

cv2.waitKey(0)

cv2.destroyAllWindows()