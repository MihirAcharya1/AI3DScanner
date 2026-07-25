import open3d as o3d


class PointCloudViewer:

    @staticmethod
    def show(filename):

        cloud = o3d.io.read_point_cloud(filename)

        o3d.visualization.draw_geometries(
            [cloud]
        )