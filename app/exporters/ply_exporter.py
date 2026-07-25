"""
PLY Exporter
"""

from pathlib import Path
import numpy as np


class PLYExporter:
    """Exports 3D point clouds to ASCII PLY format."""

    @staticmethod
    def export(points: np.ndarray, filename: str):

        if points is None or len(points) == 0:
            raise RuntimeError("No points to export.")

        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:

            file.write("ply\n")
            file.write("format ascii 1.0\n")
            file.write(f"element vertex {len(points)}\n")
            file.write("property float x\n")
            file.write("property float y\n")
            file.write("property float z\n")
            file.write("end_header\n")

            for point in points:

                file.write(
                    f"{point[0]} {point[1]} {point[2]}\n"
                )

        print(f"\nPLY exported successfully:\n{filename}")