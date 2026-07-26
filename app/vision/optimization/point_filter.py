"""
Point Cloud Filter
"""


class PointFilter:

    def __init__(self, max_error=3.0):

        self.max_error = max_error

    def filter_tracks(self, tracks):

        kept_tracks = []

        removed = 0

        for track in tracks:

            if track.point3d is None:
                continue

            if not hasattr(track, "reprojection_error"):
                kept_tracks.append(track)
                continue

            if track.reprojection_error <= self.max_error:
                kept_tracks.append(track)
            else:
                removed += 1

        print()
        print("========== POINT FILTER ==========")
        print(f"Kept    : {len(kept_tracks)}")
        print(f"Removed : {removed}")

        return kept_tracks