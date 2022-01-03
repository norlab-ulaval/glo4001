import json

import numpy as np


class PointCloud:
    SCALE = 0.01

    def __init__(self, points_optical_system, colors=None):
        if type(points_optical_system) is not np.ndarray or points_optical_system.shape[1] != 3:
            raise ValueError("points must be a numpy array of shape (n, 3)")
        if colors is not None and not points_optical_system.shape == points_optical_system.shape:
            raise ValueError("colors and points must have the same size")

        points = np.zeros_like(points_optical_system)
        points[:, 0] = points_optical_system[:, 2]
        points[:, 1] = -1 * points_optical_system[:, 0]
        points[:, 2] = -1 * points_optical_system[:, 1]

        self.points = points
        self.colors = colors if colors is not None else self._red_color_matrix(points.shape)

        self.min_x, self.min_y, self.min_z = np.amin(self.points, axis=0)
        self.max_x, self.max_y, self.max_z = np.amax(self.points, axis=0)

    def _red_color_matrix(self, shape):
        colors = np.zeros(shape, dtype=np.uint8)
        colors[:, 0] = 255
        return colors

    def _write_r_hrc(self):
        n_of_points = self.points.shape[0]
        n_of_points_bytes = int(n_of_points).to_bytes(4, byteorder='little')
        hrc_content = b'\x00' + n_of_points_bytes
        with open("./point_cloud/data/r/r.hrc", "wb") as f:
            f.write(hrc_content)

    def _write_cloud_js(self):
        cloud_js_content = {
            "version": "1.6",
            "octreeDir": "data",
            "boundingBox": {
                "lx": self.min_x,
                "ly": self.min_y,
                "lz": self.min_z,
                "ux": self.max_x,
                "uy": self.max_y,
                "uz": self.max_z
            },
            "tightBoundingBox": {
                "lx": self.min_x,
                "ly": self.min_y,
                "lz": self.min_z,
                "ux": self.max_x,
                "uy": self.max_y,
                "uz": self.max_z
            },
            "pointAttributes": [
                "POSITION_CARTESIAN",
                "COLOR_PACKED"
            ],
            "spacing": 0.01,
            "scale": self.SCALE,
            "hierarchyStepSize": 1
        }
        with open("./point_cloud/cloud.js", "w") as f:
            f.write(json.dumps(cloud_js_content))

    def _write_points(self):
        with open("./point_cloud/data/r/r.bin", "wb") as f:
            for point, color in zip(self.points, self.colors):
                point_uint = (point - np.array([self.min_x, self.min_y, self.min_z])) / self.SCALE

                x, y, z = np.asarray(point_uint, dtype='int')
                r, g, b = np.asarray(color, dtype='int')

                point_bytes = int(x).to_bytes(4, byteorder='little') + \
                              int(y).to_bytes(4, byteorder='little') + \
                              int(z).to_bytes(4, byteorder='little') + \
                              int(r).to_bytes(1, byteorder='little') + \
                              int(g).to_bytes(1, byteorder='little') + \
                              int(b).to_bytes(1, byteorder='little') + \
                              b'\x00'
                f.write(point_bytes)

    def save(self):
        self._write_r_hrc()
        self._write_cloud_js()
        self._write_points()
