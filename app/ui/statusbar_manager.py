"""
Status Bar Manager
"""

from PySide6.QtWidgets import QLabel, QMainWindow


class StatusBarManager:
    """Creates the application's status bar."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self._create_statusbar()

    def _create_statusbar(self) -> None:
        status = self.window.statusBar()

        status.showMessage("Ready")

        status.addPermanentWidget(QLabel("AI3DScanner v0.2"))
        status.addPermanentWidget(QLabel("Python 3.12"))