"""
Image Viewer Widget
"""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ImageViewer(QLabel):
    """Displays imported images."""

    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText("No Image Selected")
        self.setMinimumSize(600, 400)

    def load_image(self, image_path: Path) -> None:
        """Load and display an image."""

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            self.setText("Unable to load image.")
            return

        self.setPixmap(
            pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def resizeEvent(self, event):
        """Redisplay image when window is resized."""
        if self.pixmap() is not None:
            self.setPixmap(
                self.pixmap().scaled(
                    self.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )
        super().resizeEvent(event)