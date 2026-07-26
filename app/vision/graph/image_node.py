class ImageNode:

    def __init__(self, index, filename):

        self.index = index
        self.filename = filename

        self.keypoints = None
        self.descriptors = None

        self.connections = {}