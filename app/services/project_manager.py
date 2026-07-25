"""
Project Manager
"""

from dataclasses import asdict
from pathlib import Path

from app.models.project import AI3DProject
from app.utils.json_utils import read_json, write_json


class ProjectManager:
    """
    Handles creating, loading and saving projects.
    """

    def __init__(self) -> None:

        self.project = AI3DProject()

    def new_project(self) -> None:

        self.project = AI3DProject()

    def save(self, path: Path) -> None:

        write_json(
            path,
            asdict(self.project),
        )

    def load(self, path: Path) -> None:

        data = read_json(path)

        self.project = AI3DProject(**data)