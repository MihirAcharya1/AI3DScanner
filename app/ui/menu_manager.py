"""
Menu Manager

Responsible for creating the application's menu bar.
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMainWindow
from pathlib import Path


class MenuManager:
    """Creates and manages the application's menu bar."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self._create_menu()

    def _create_menu(self) -> None:

        menu_bar = self.window.menuBar()

        file_menu = menu_bar.addMenu("&File")

        self.new_action = QAction("&New Project", self.window)
        self.open_action = QAction("&Open Project", self.window)
        self.save_action = QAction("&Save Project", self.window)
        self.save_as_action = QAction("Save &As...", self.window)
        self.exit_action = QAction("E&xit", self.window)
        self.import_action = QAction("&Import Images...", self.window)

        self.new_action.triggered.connect(self.new_project)
        self.open_action.triggered.connect(self.open_project)
        self.save_action.triggered.connect(self.save_project)
        self.save_as_action.triggered.connect(self.save_project_as)
        self.import_action.triggered.connect(self.import_images)
        self.exit_action.triggered.connect(self.window.close)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addAction(self.import_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        menu_bar.addMenu("&Edit")
        menu_bar.addMenu("&View")
        menu_bar.addMenu("&Project")
        menu_bar.addMenu("&Tools")
        menu_bar.addMenu("&Help")
        reconstruction_menu = menu_bar.addMenu("Reconstruction")
        start_action = reconstruction_menu.addAction("Start Reconstruction")
        view_action = reconstruction_menu.addAction("View Point Cloud")

    def new_project(self) -> None:
        self.window.project_manager.new_project()
        self.window.statusbar_manager.show_message("New project created")

    def open_project(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self.window, "Open AI3D Project", "", "AI3D Project (*.ai3d)"
        )

        if filename:
            from pathlib import Path

            self.window.project_manager.load(Path(filename))
            self.window.statusbar_manager.show_message("Project loaded")

    def save_project(self) -> None:
        self.save_project_as()

    def save_project_as(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(
            self.window, "Save AI3D Project", "", "AI3D Project (*.ai3d)"
        )

        if filename:
            from pathlib import Path

            self.window.project_manager.save(Path(filename))
            self.window.statusbar_manager.show_message("Project saved")

    # from pathlib import Path


    def import_images(self) -> None:

        filenames, _ = QFileDialog.getOpenFileNames(
            self.window,
            "Import Images",
            "",
            "Images (*.jpg *.jpeg *.png *.bmp *.tif *.tiff)",
        )

        if not filenames:

            return

        paths = [Path(f) for f in filenames]

        count = self.window.project_manager.import_images(paths)

        self.window.statusbar_manager.show_message(f"Imported {count} images")

        self.window.dock_manager.project_list.clear()

        for image in self.window.project_manager.project.images:

            self.window.dock_manager.project_list.addItem(image.name)
