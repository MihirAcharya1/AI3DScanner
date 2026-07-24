"""
Application entry point.
"""

import sys

from app.core.application import Application


def main() -> None:
    """Application launcher."""

    app = Application()

    exit_code = app.run()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()