"""
Image Service
"""

from pathlib import Path


class ImageService:
    """Validates image files."""

    VALID_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tif",
        ".tiff",
    }

    @classmethod
    def is_valid_image(cls, path: Path) -> bool:
        return (
            path.exists()
            and path.is_file()
            and path.suffix.lower() in cls.VALID_EXTENSIONS
        )