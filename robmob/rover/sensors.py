import ast
import base64
from io import BytesIO

import numpy as np
from PIL import Image

from robmob.sensors import Sensor


class RobotEspSensor(Sensor):
    TOPIC = '/rover/state'
    MESSAGE_TYPE = 'std_msgs/msg/String'
    SAMPLE_RATE = 10

    def __init__(self, buffer_size=100000):
        super().__init__(buffer_size)

    def parse_message(self, message):
        data = message['msg']['data']
        return ast.literal_eval(data)


class SharpSensor(Sensor):
    TOPIC = '/range'
    MESSAGE_TYPE = 'std_msgs/msg/Float32'
    SAMPLE_RATE = 100

    # Calibration table of the high range sharp sensor, for 15+ cm.
    HIGH_RANGE_CALIB_TABLE = np.asarray([
        [15, 2.76],
        [20, 2.53],
        [30, 1.99],
        [40, 1.53],
        [50, 1.23],
        [60, 1.04],
        [70, 0.91],
        [80, 0.82],
        [90, 0.72],
        [100, 0.66],
        [110, 0.6],
        [120, 0.55],
        [130, 0.50],
        [140, 0.46],
        [150, 0.435],
        [200, 0],
        [np.inf, 0]
    ])

    def __init__(self, buffer_size=100):
        """
        There are two Sharp sensors on the robot. The analog_input_id 0 is the long range sensor
        and the analog_input_id 1 is the short range sensor.
        """
        super().__init__(buffer_size)

    def parse_message(self, message):
        return float(message['msg']['data'])


class CameraRGBSensor(Sensor):
    TOPIC = '/color/video/image/compressed'
    MESSAGE_TYPE = 'sensor_msgs/msg/CompressedImage'
    SAMPLE_RATE = 30

    def __init__(self, buffer_size=60):
        super().__init__(buffer_size)

    def parse_message(self, message):
        image_data = message['msg']['data']
        decompressed_image = Image.open(BytesIO(base64.b64decode(image_data)))
        return decompressed_image


class CameraDepthSensor(Sensor):
    # TOPIC = '/stereo/depth'
    # MESSAGE_TYPE = ('sensor_msgs/msg/Image')
    TOPIC = '/stereo/depth/compressedDepth'
    MESSAGE_TYPE = ('sensor_msgs/msg/CompressedImage')
    SAMPLE_RATE = 30

    def __init__(self, buffer_size=60):
        super().__init__(buffer_size)

    def parse_message(self, message):
        msg = message['msg']
        base64_bytes = msg['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        with open('a.jpg', 'wb') as image_file:
            image_file.write(image_bytes)
        # compressed_str = message['msg']['data']
        # compressed_data = base64.b64decode(compressed_str)
        # np_arr = np.frombuffer(compressed_data, np.uint8)
        # depth_image = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
        # return depth_image
