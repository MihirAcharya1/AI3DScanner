import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from app.vision.image_loader import ImageLoader
from app.vision.feature_detector import FeatureDetector
from app.vision.feature_matcher import FeatureMatcher


image1 = ImageLoader.load(Path("examples/chair/image1.png"))
image2 = ImageLoader.load(Path("examples/chair/image2.png"))
image3 = ImageLoader.load(Path("examples/chair/image3.png"))
image4 = ImageLoader.load(Path("examples/chair/image4.png"))
image5 = ImageLoader.load(Path("examples/chair/image5.png"))
image6 = ImageLoader.load(Path("examples/chair/image6.png"))

gray1 = ImageLoader.to_gray(image1)
gray2 = ImageLoader.to_gray(image2)
gray3 = ImageLoader.to_gray(image3)
gray4 = ImageLoader.to_gray(image4)
gray5 = ImageLoader.to_gray(image5)
gray6 = ImageLoader.to_gray(image6)


detector = FeatureDetector()

kp1, des1 = detector.detect(gray1)
kp2, des2 = detector.detect(gray2)
kp3, des3 = detector.detect(gray3)
kp4, des4 = detector.detect(gray4)
kp5, des5 = detector.detect(gray5)
kp6, des6 = detector.detect(gray6)


matcher = FeatureMatcher()

matches = matcher.match(des1, des2)

print(f"Image 1 Keypoints : {len(kp1)}")
print(f"Image 2 Keypoints : {len(kp2)}")
print(f"Matches           : {len(matches)}")

result = cv2.drawMatches(
    image1,
    kp1,
    image2,
    kp2,
    matches[:100],
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
)

cv2.imshow("ORB Feature Matching", result)

cv2.waitKey(0)

cv2.destroyAllWindows()