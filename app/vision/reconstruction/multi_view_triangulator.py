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

            if len(track) < 2:
                continue

            obs1 = track.observations[0]
            obs2 = track.observations[1]

            image1 = obs1.image_index
            image2 = obs2.image_index

            if (
                image1 >= len(rotations)
                or image2 >= len(rotations)
            ):
                continue

            R1 = rotations[image1]
            t1 = translations[image1]

            R2 = rotations[image2]
            t2 = translations[image2]

            P1 = camera_matrix @ np.hstack(
                (
                    R1,
                    t1,
                )
            )

            P2 = camera_matrix @ np.hstack(
                (
                    R2,
                    t2,
                )
            )

            pt1 = np.asarray(
                obs1.point2d,
                dtype=np.float64,
            ).reshape(2, 1)

            pt2 = np.asarray(
                obs2.point2d,
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

            if (
                np.isnan(point3d).any()
                or np.isinf(point3d).any()
            ):
                continue

            track.set_point3d(point3d)

            points3d.append(point3d)

        print()
        print("========== MULTI VIEW TRIANGULATION ==========")
        print(f"Triangulated : {len(points3d)}")

        return points3d