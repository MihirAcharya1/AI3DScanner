"""
Application bootstrap.
"""

import sys

from PySide6.QtWidgets import QApplication

from app.core.logger import Logger
from app.ui.main_window import MainWindow
from app.services.project_manager import ProjectManager
from pathlib import Path


class Application:
    """Creates and starts the Qt application."""

    def __init__(self) -> None:

        Logger.setup()

        self.qt_app = QApplication(sys.argv)

        self.project_manager = ProjectManager()

        self.window = MainWindow()

        self.window.project_manager = self.project_manager

    def run(self) -> int:
        """Start the Qt application."""
        self.window.show()

        return self.qt_app.exec()