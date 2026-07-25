"""
JSON Helper Functions
"""

import json
from pathlib import Path


def write_json(path: Path, data: dict) -> None:
    """
    Write dictionary to JSON.
    """

    with path.open("w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
            default=str,
        )


def read_json(path: Path) -> dict:

    with path.open("r", encoding="utf-8") as file:

        return json.load(file)