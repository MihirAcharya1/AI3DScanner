"""
Dock Manager

Creates and manages all dockable panels.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QListWidget,
    QDockWidget,
    QTextEdit,
    QWidget,
    QMainWindow,
)
from app.ui.widgets.image_viewer import ImageViewer



class DockManager:
    """Creates and stores the application's dock widgets."""

    def __init__(self, window: QMainWindow) -> None:

        self.window = window

        self.project_list = QListWidget()

        self.properties_editor = QTextEdit()

        self.console_output = QTextEdit()

        self._create_docks()

    def _create_docks(self) -> None:

        self.project_dock = QDockWidget("Project Explorer", self.window)
        self.project_dock.setWidget(self.project_list)
        self.project_list.itemClicked.connect(self.on_image_selected)
        self.window.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)

        self.properties_dock = QDockWidget("Properties", self.window)
        self.properties_dock.setWidget(self.properties_editor)
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)

        self.console_dock = QDockWidget("Console", self.window)
        self.console_dock.setWidget(self.console_output)
        self.window.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)


        self.image_viewer = ImageViewer()

        self.window.setCentralWidget(self.image_viewer)
        
    def on_image_selected(self, item):

        for image in self.window.project_manager.project.images:

            if image.name == item.text():

                self.image_viewer.load_image(image)

                self.window.statusbar_manager.show_message(
                    f"Viewing: {image.name}"
                )

                break