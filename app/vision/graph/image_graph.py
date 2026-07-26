class ImageGraph:

    def __init__(self):

        self.nodes = []

    def add_node(self, node):

        self.nodes.append(node)

    def connect(self, index1, index2, matches):

        self.nodes[index1].connections[index2] = list(matches)
        self.nodes[index2].connections[index1] = list(matches)