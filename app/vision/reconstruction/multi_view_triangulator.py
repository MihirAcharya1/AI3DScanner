"""
Multi View Triangulator
"""

import cv2
import numpy as np


class MultiViewTriangulator:

    def triangulate(
        self,
        tracks,
        camera_matrix,
        rotations,
        translations,
    ):

        points3d = []

        if len(rotations) == 0:
            return points3d

        for track in tracks:

            if track.size() < 2:
                continue

            obs1 = track.observations[0]
            obs2 = track.observations[1]

            image1 = obs1["image"]
            image2 = obs2["image"]

            if (
                image1 >= len(rotations)
                or image2 >= len(rotations)
            ):
                continue

            P1 = camera_matrix @ np.hstack(
                (
                    rotations[image1],
                    translations[image1],
                )
            )

            P2 = camera_matrix @ np.hstack(
                (
                    rotations[image2],
                    translations[image2],
                )
            )

            pt1 = np.array(
                obs1["point"],
                dtype=np.float64,
            ).reshape(2, 1)

            pt2 = np.array(
                obs2["point"],
                dtype=np.float64,
            ).reshape(2, 1)

            point4d = cv2.triangulatePoints(
                P1,
                P2,
                pt1,
                pt2,
            )

            point3d = (
                point4d[:3]
                / point4d[3]
            ).flatten()

            track.set_point3d(point3d)

            points3d.append(point3d)

        print()
        print("========== MULTI VIEW TRIANGULATION ==========")
        print(f"Triangulated : {len(points3d)}")

        return points3d