import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.vision.pipeline.reconstruction_pipeline import ReconstructionPipeline
from app.viewers.point_cloud_viewer import PointCloudViewer
from app.config.reconstruction_config import ReconstructionConfig

config = ReconstructionConfig(
    detector="ORB",
    max_features=8000,
    matcher="BF",
    ratio_test=0.95,
    ransac_threshold=1.0,
)

pipeline = ReconstructionPipeline(config)

pipeline.load_images("examples/chair")

pipeline.detect_features()

pipeline.match_features()

pipeline.show_statistics()

pipeline.filter_matches()

pipeline.estimate_camera_pose()

pipeline.triangulate()

pipeline.export_sparse_cloud(
    "outputs/chair_sparse.ply"
)

PointCloudViewer.show(
    "outputs/chair_sparse.ply"
)

# pipeline.show_matches(filtered=False)

# pipeline.show_matches(filtered=True)