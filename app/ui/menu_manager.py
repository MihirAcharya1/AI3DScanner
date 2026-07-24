"""
Menu Manager

Responsible for creating the application's menu bar.
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow


class MenuManager:
    """Creates and manages the application's menu bar."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self._create_menu()

    def _create_menu(self) -> None:
        menu_bar = self.window.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")

        new_action = QAction("&New Project", self.window)
        open_action = QAction("&Open Project", self.window)
        save_action = QAction("&Save Project", self.window)
        exit_action = QAction("E&xit", self.window)

        exit_action.triggered.connect(self.window.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Other Menus
        menu_bar.addMenu("&Edit")
        menu_bar.addMenu("&View")
        menu_bar.addMenu("&Project")
        menu_bar.addMenu("&Tools")
        menu_bar.addMenu("&Help")