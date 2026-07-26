import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
import open3d as o3d

from app.viewers.scene_viewer import SceneViewer
from app.config.reconstruction_config import ReconstructionConfig
from app.vision.reconstruction.incremental_reconstructor import (
    IncrementalReconstructor,
)

config = ReconstructionConfig()

reconstructor = IncrementalReconstructor(config)

reconstructor.load_images("examples/chair")

reconstructor.detect_features()

reconstructor.match_features()

reconstructor.build_feature_graph()

reconstructor.filter_graph()

reconstructor.build_tracks()

reconstructor.show_statistics()

reconstructor.estimate_camera_poses()

reconstructor.triangulate_pairs()

reconstructor.reconstruction_summary()

reconstructor.optimize()

reconstructor.run_bundle_adjustment()

pcd = o3d.io.read_point_cloud(
    "outputs/chair_sparse.ply"
)

SceneViewer.show(
    pcd,
    reconstructor.trajectory,
)
