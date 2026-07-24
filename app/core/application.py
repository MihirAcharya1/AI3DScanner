"""
Application bootstrap.
"""

import sys

from PySide6.QtWidgets import QApplication

from app.core.logger import Logger
from app.ui.main_window import MainWindow


class Application:
    """Creates and starts the Qt application."""

    def __init__(self) -> None:

        Logger.setup()

        self.qt_app = QApplication(sys.argv)

        self.window = MainWindow()

    def run(self) -> None:

        self.window.show()

        sys.exit(self.qt_app.exec())