"""
Main application window.
"""

from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Main window of AI3DScanner."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("AI3DScanner")

        self.resize(1400, 900)

        self.statusBar().showMessage("Ready")