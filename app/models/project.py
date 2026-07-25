"""
AI3D Project Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class AI3DProject:
    """
    Represents an AI3DScanner project.
    """

    project_name: str = "Untitled"

    version: str = "0.3.0"

    images: list[Path] = field(default_factory=list)

    point_cloud: str | None = None

    mesh: str | None = None

    textures: list[str] = field(default_factory=list)

    created: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    modified: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )