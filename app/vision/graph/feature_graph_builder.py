"""
Feature Graph Builder
"""

class FeatureGraphBuilder:

    def __init__(self, matcher):

        self.matcher = matcher

    def build(self, graph):

        for i in range(len(graph.nodes)):

            node1 = graph.nodes[i]

            for j in range(i + 1, len(graph.nodes)):

                node2 = graph.nodes[j]

                matches = self.matcher.match(
                    node1.descriptors,
                    node2.descriptors,
                )

                graph.connect(
                    i,
                    j,
                    matches,
                )

                print(
                    f"{node1.filename} <-> "
                    f"{node2.filename} : "
                    f"{len(matches)} matches"
                )