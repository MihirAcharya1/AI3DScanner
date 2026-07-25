"""
Test ORB Feature Matching on Multiple Images
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from app.vision.image_loader import ImageLoader
from app.vision.feature_detector import FeatureDetector
from app.vision.feature_matcher import FeatureMatcher


# -------------------------------------------------
# Load all images from folder
# -------------------------------------------------

IMAGE_FOLDER = Path("examples/chair")

# Supported image extensions
EXTENSIONS = ("*.jpg", "*.jpeg", "*.png", "*.bmp")

image_paths = []

for ext in EXTENSIONS:
    image_paths.extend(IMAGE_FOLDER.glob(ext))

image_paths = sorted(image_paths)

if len(image_paths) < 2:
    raise RuntimeError("Need at least two images to perform feature matching.")

print(f"Found {len(image_paths)} images.\n")


# -------------------------------------------------
# Load images
# -------------------------------------------------

images = [
    ImageLoader.load(path)
    for path in image_paths
]

gray_images = [
    ImageLoader.to_gray(image)
    for image in images
]


# -------------------------------------------------
# Detect ORB Features
# -------------------------------------------------

detector = FeatureDetector()

features = []

for i, gray in enumerate(gray_images):

    keypoints, descriptors = detector.detect(gray)

    features.append((keypoints, descriptors))

    print(
        f"{image_paths[i].name:<20} "
        f"Keypoints: {len(keypoints)}"
    )


print("\n------------------------------\n")


# -------------------------------------------------
# Match Consecutive Images
# -------------------------------------------------

matcher = FeatureMatcher()

for i in range(len(features) - 1):

    kp1, des1 = features[i]
    kp2, des2 = features[i + 1]

    matches = matcher.match(des1, des2)

    print(
        f"{image_paths[i].name}  <-->  {image_paths[i+1].name}"
    )

    print(
        f"Matches: {len(matches)}"
    )

    result = cv2.drawMatches(
        images[i],
        kp1,
        images[i + 1],
        kp2,
        matches[:100],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    cv2.imshow(
        f"Matches {i+1}",
        result,
    )

    cv2.waitKey(0)

cv2.destroyAllWindows()