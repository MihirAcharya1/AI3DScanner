from app.vision.tracks.feature_track import FeatureTrack


class TrackBuilder:

    def __init__(self):

        self.tracks = []

    def build(self, graph):

        track_id = 0

        for node in graph.nodes:

            for neighbour, matches in node.connections.items():

                for match in matches:

                    track = FeatureTrack(track_id)

                    track.add(
                        node.index,
                        match.queryIdx,
                    )

                    track.add(
                        neighbour,
                        match.trainIdx,
                    )

                    self.tracks.append(track)

                    track_id += 1

        print()

        print("========== FEATURE TRACKS ==========")

        print(
            f"Tracks : {len(self.tracks)}"
        )