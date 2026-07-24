"""
Application logging.
"""

import logging


class Logger:
    """Central application logger."""

    @staticmethod
    def setup() -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(levelname)s] %(message)s",
        )