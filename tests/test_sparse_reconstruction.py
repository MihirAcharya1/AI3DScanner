import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.vision.pipeline.reconstruction_pipeline import ReconstructionPipeline


def main():

    pipeline = ReconstructionPipeline()

    pipeline.load_images("examples/chair")

    pipeline.detect_features()

    pipeline.match_features()

    pipeline.filter_matches()

    pipeline.estimate_camera_pose()

    pipeline.triangulate()

    pipeline.export_sparse_cloud(
        "outputs/chair_sparse.ply"
    )


if __name__ == "__main__":
    main()