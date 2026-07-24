"""
Dock Manager
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QTextEdit,
    QWidget,
    QMainWindow,
)


class DockManager:
    """Creates the application's dockable panels."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self._create_docks()

    def _create_docks(self) -> None:

        # Project Explorer
        project = QDockWidget("Project Explorer", self.window)
        project.setWidget(QListWidget())
        self.window.addDockWidget(Qt.LeftDockWidgetArea, project)

        # Properties
        properties = QDockWidget("Properties", self.window)
        properties.setWidget(QTextEdit())
        self.window.addDockWidget(Qt.RightDockWidgetArea, properties)

        # Console
        console = QDockWidget("Console", self.window)
        console.setWidget(QTextEdit())
        self.window.addDockWidget(Qt.BottomDockWidgetArea, console)

        # Central widget
        self.window.setCentralWidget(QWidget())