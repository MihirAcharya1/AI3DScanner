"""
Graph Filter
"""


class GraphFilter:

    def __init__(self, min_matches=30):

        self.min_matches = min_matches

    def filter(self, graph):

        print()

        print("========== GRAPH FILTER ==========")

        for node in graph.nodes:

            remove = []

            for neighbour, matches in node.connections.items():

                if len(matches) < self.min_matches:

                    remove.append(neighbour)

            for neighbour in remove:

                del node.connections[neighbour]

            print(
                f"{node.filename} -> "
                f"{len(node.connections)} connections"
            )