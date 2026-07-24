"""
Toolbar Manager
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar


class ToolbarManager:
    """Creates the main application toolbar."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self._create_toolbar()

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")

        self.window.addToolBar(toolbar)

        toolbar.addAction(QAction("New", self.window))
        toolbar.addAction(QAction("Open", self.window))
        toolbar.addAction(QAction("Save", self.window))

        toolbar.addSeparator()

        toolbar.addAction(QAction("Import Images", self.window))