import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.vision.pipeline.reconstruction_pipeline import ReconstructionPipeline


pipeline = ReconstructionPipeline()

pipeline.load_images("examples/chair")

pipeline.detect_features()

pipeline.match_features()

pipeline.show_statistics()

pipeline.estimate_camera_pose()

pipeline.show_matches()