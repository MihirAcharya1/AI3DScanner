"""
Main application window.
"""

from PySide6.QtWidgets import QMainWindow

from app.ui.menu_manager import MenuManager
from app.ui.toolbar_manager import ToolbarManager
from app.ui.statusbar_manager import StatusBarManager
from app.ui.dock_manager import DockManager


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("AI3DScanner")

        self.resize(1024,600)

        self.menu_manager = MenuManager(self)
        self.toolbar_manager = ToolbarManager(self)
        self.statusbar_manager = StatusBarManager(self)
        self.dock_manager = DockManager(self)