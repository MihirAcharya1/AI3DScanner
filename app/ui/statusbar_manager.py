"""
Status Bar Manager
"""

from PySide6.QtWidgets import QLabel, QMainWindow


class StatusBarManager:

    def __init__(self, window: QMainWindow) -> None:

        self.window = window

        self.status_bar = self.window.statusBar()

        self.message = QLabel()

        self.version = QLabel("AI3DScanner v0.2")

        self.python = QLabel("Python 3.12")

        self._create()

    def _create(self) -> None:

        self.status_bar.showMessage("Ready")

        self.status_bar.addPermanentWidget(self.version)

        self.status_bar.addPermanentWidget(self.python)

    def show_message(self, text: str) -> None:

        self.status_bar.showMessage(text)