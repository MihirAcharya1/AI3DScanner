from dataclasses import dataclass
@dataclass
class ReconstructionConfig:
    detector: str = "ORB"
    max_features: int = 5000
    matcher: str = "BF"
    ratio_test: float = 0.75
    ransac_threshold: float = 1.0
    bundle_adjustment: bool = True
    export_colors: bool = True
    point_size: float = 2.0