from app.vision.tracks.feature_track import FeatureTrack


class TrackBuilder:

    def __init__(self):

        self.tracks = []

    def build(self, graph):

        self.tracks.clear()

        track_id = 0

        for node in graph.nodes:

            for neighbour, matches in node.connections.items():
                if node.index > neighbour:  
                    continue

                neighbour_node = graph.nodes[neighbour]

                for match in matches:

                    track = FeatureTrack(track_id)
                    # print(f"\nNode {node.index}")
                    # print(f"Keypoints in node : {len(node.keypoints)}")
                    # print(f"queryIdx          : {match.queryIdx}")
                    # print(f"trainIdx          : {match.trainIdx}")
                    # Observation in first image
                    pt1 = node.keypoints[
                        match.queryIdx
                    ].pt

                    track.add(
                        node.index,
                        match.queryIdx,
                        pt1,
                    )

                    # Observation in second image
                    pt2 = neighbour_node.keypoints[
                        match.trainIdx
                    ].pt

                    track.add(
                        neighbour,
                        match.trainIdx,
                        pt2,
                    )

                    self.tracks.append(track)

                    track_id += 1

        print()
        print("========== FEATURE TRACKS ==========")
        print(f"Tracks : {len(self.tracks)}")