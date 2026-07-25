from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ImageViewer(QLabel):

    def __init__(self):
        super().__init__()

        self.original_pixmap = None

        self.setAlignment(Qt.AlignCenter)
        self.setText("No Image Selected")

    def load_image(self, image_path: Path):

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():

            self.original_pixmap = None
            self.setText("Unable to load image.")

            return

        self.original_pixmap = pixmap

        self._update_pixmap()

    def resizeEvent(self, event):

        self._update_pixmap()

        super().resizeEvent(event)

    def _update_pixmap(self):

        if self.original_pixmap is None:
            return

        self.setPixmap(
            self.original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )