"""
Reconstruction Service
Coordinates the complete reconstruction pipeline.
"""

from pathlib import Path

from app.vision.pipeline.reconstruction_pipeline import ReconstructionPipeline


class ReconstructionService:

    def __init__(self):
        self.pipeline = ReconstructionPipeline()

    def reconstruct(self, image_folder: str):

        print("\n========== AI3DScanner Reconstruction ==========\n")

        image_folder = Path(image_folder)

        self.pipeline.load_images(image_folder)

        print("✓ Images Loaded")

        self.pipeline.detect_features()

        print("✓ Features Detected")

        self.pipeline.match_features()

        print("✓ Features Matched")

        self.pipeline.filter_matches()

        print("✓ Matches Filtered")

        self.pipeline.estimate_camera_pose()

        print("✓ Camera Pose Estimated")

        self.pipeline.triangulate()

        print("✓ Point Cloud Generated")

        output = "outputs/reconstruction.ply"

        self.pipeline.export_sparse_cloud(output)

        print("✓ Point Cloud Exported")

        return output