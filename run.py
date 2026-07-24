"""
Application entry point.

This file is intentionally minimal.
It only starts the application.
"""

from app.core.application import Application


def main() -> None:
    """Application launcher."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()