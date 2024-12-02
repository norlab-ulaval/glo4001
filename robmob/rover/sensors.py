import ast
import base64
import re
from io import BytesIO

import depthai as dai
import numpy as np
from PIL import Image

from robmob.robot import Robot
from robmob.sensors import Sensor


class RobotEspSensor(Sensor):
    TOPIC = '/rover/state'
    MESSAGE_TYPE = 'std_msgs/msg/String'
    SAMPLE_RATE = 62.4
    TICKS_TO_METER = 2 * np.pi / 2048 * Robot.WHEEL_RADIUS
    SEC_REGEX = r'\bsec=([0-9]*)'
    NANOSEC_REGEX = r'\bnanosec=([0-9]*)'

    def __init__(self, buffer_size=100_000):
        super().__init__(buffer_size)

    def parse_message(self, message):
        data = message['msg']['data']
        return ast.literal_eval(data)

    def peek_odom(self):
        data = self.peek_data()
        return self._data_to_odom(data)

    def read_odom(self):
        data = self.read_buffer()
        return np.array([self._data_to_odom(x) for x in data])

    def _data_to_odom(self, data):
        timestamp = data['timestamp']
        sec = int(re.search(self.SEC_REGEX, timestamp).group(1))
        nano = int(re.search(self.NANOSEC_REGEX, timestamp).group(1))
        t = sec + nano * 1e-9
        meter_to_tick = 2048 / (2 * np.pi * Robot.WHEEL_RADIUS)
        return t, int(data['en_odom_l'] * meter_to_tick), int(data['en_odom_r'] * meter_to_tick)

    def peek_gyro(self):
        data = self.peek_data()
        return self._data_to_gyro(data)

    def sample_gyro_for_x_sec(self, duration):
        samples = [self._data_to_gyro(x) for x in self.sample_data_for_x_sec(duration)]
        return np.array([list(x.values()) for x in samples])

    def read_gyro(self):
        data = self.read_buffer()
        return [self._data_to_gyro(x) for x in data]

    def _data_to_gyro(self, data):
        values = dict(x=data['rgx'], y=data['rgy'], z=data['rgz'])
        return {k: np.rad2deg(v) for k, v in values.items()}


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
    # TODO bypass ROS and use the camera directly
    TOPIC = '/color/video/image/compressed'
    MESSAGE_TYPE = 'sensor_msgs/msg/CompressedImage'
    SAMPLE_RATE = 30

    def __init__(self, buffer_size=5):
        super().__init__(buffer_size)

    def parse_message(self, message):
        image_data = message['msg']['data']
        decompressed_image = Image.open(BytesIO(base64.b64decode(image_data)))
        return np.array(decompressed_image)


class CameraDepthSensor(Sensor):
    # TODO bypass ROS and use the camera directly
    TOPIC = '/stereo/depth'
    MESSAGE_TYPE = ('sensor_msgs/msg/Image')
    # TOPIC = '/stereo/depth/compressedDepth'
    # MESSAGE_TYPE = ('sensor_msgs/msg/CompressedImage')
    SAMPLE_RATE = 30

    def __init__(self, buffer_size=5):
        super().__init__(buffer_size)

    def parse_message(self, message):
        msg = message['msg']
        base64_bytes = msg['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        image = np.frombuffer(image_bytes, dtype=np.uint16)
        image = image.reshape((msg['height'], msg['width'], 1))
        return image


class OakLiteCamera:
    RESOLUTION_RGB = (1920, 1080)
    CENTER_X_RGB = RESOLUTION_RGB[0] / 2
    CENTER_Y_RGB = RESOLUTION_RGB[1] / 2
    RESOLUTION_DEPTH = (1920, 1080)
    CENTER_X_DEPTH = RESOLUTION_DEPTH[0] / 2
    CENTER_Y_DEPTH = RESOLUTION_DEPTH[1] / 2
    FOCAL_LENGTH = 3030.1787109375
    FOV_X = 69
    FOV_Y = 54
    FREQUENCY = 10

    def __init__(self, use_rgb=False, use_depth=False, use_april=False):
        self.pipeline = dai.Pipeline()

        if use_rgb:
            # RGB
            cam_rgb = self.pipeline.create(dai.node.ColorCamera)
            cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)
            cam_rgb.setInterleaved(False)
            cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
            cam_rgb.setFps(self.FREQUENCY)

            # Link
            xout_rgb = self.pipeline.create(dai.node.XLinkOut)
            xout_rgb.setStreamName('rgb')
            cam_rgb.video.link(xout_rgb.input)

        # Left
        cam_left = self.pipeline.create(dai.node.MonoCamera)
        cam_left.setCamera('left')
        cam_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
        cam_left.setFps(self.FREQUENCY)
        xout_left = self.pipeline.create(dai.node.XLinkOut)
        xout_left.setStreamName('left')
        cam_left.out.link(xout_left.input)

        if use_depth:
            # Right
            cam_right = self.pipeline.create(dai.node.MonoCamera)
            cam_right.setCamera('right')
            cam_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
            cam_right.setFps(self.FREQUENCY)
            # Depth
            cam_stereo = self.pipeline.create(dai.node.StereoDepth)
            cam_stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
            # cam_stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
            cam_stereo.setRectifyEdgeFillColor(0)
            cam_stereo.setLeftRightCheck(True)
            cam_stereo.setSubpixel(True)
            cam_stereo.setDepthAlign(dai.CameraBoardSocket.RGB)

            # Links
            cam_right.out.link(cam_stereo.right)
            cam_left.out.link(cam_stereo.left)
            xout_depth = self.pipeline.create(dai.node.XLinkOut)
            xout_depth.setStreamName('depth')
            cam_stereo.depth.link(xout_depth.input)

        if use_april:
            apriltag = self.pipeline.create(dai.node.AprilTag)
            apriltag.initialConfig.setFamily(dai.AprilTagConfig.Family.TAG_16H5)

            april_config = apriltag.initialConfig.get()
            april_config.quadDecimate = 4
            april_config.quadSigma = 0
            april_config.refineEdges = True
            april_config.decodeSharpening = 0.25
            april_config.maxHammingDistance = 1
            april_config.quadThresholds.minClusterPixels = 5
            april_config.quadThresholds.maxNmaxima = 10
            april_config.quadThresholds.criticalDegree = 10
            april_config.quadThresholds.maxLineFitMse = 10
            april_config.quadThresholds.minWhiteBlackDiff = 5
            april_config.quadThresholds.deglitch = False

            xout_apriltag = self.pipeline.create(dai.node.XLinkOut)
            apriltag.passthroughInputImage.link(xout_left.input)
            cam_left.out.link(apriltag.inputImage)
            apriltag.out.link(xout_apriltag.input)
            apriltag.inputImage.setBlocking(False)
            apriltag.inputImage.setQueueSize(1)

            xout_apriltag.setStreamName('apriltagdata')


        self.device = dai.Device(self.pipeline)
        self.queue_left = self.device.getOutputQueue(name='left', maxSize=4, blocking=False)
        if use_rgb:
            self.queue_rgb = self.device.getOutputQueue(name='rgb', maxSize=4, blocking=False)
        if use_depth:
            self.queue_depth = self.device.getOutputQueue(name='depth', maxSize=4, blocking=False)
        if use_april:
            self.queue_apriltag = self.device.getOutputQueue(name='apriltagdata', maxSize=8, blocking=False)

        # Intrinsics
        self.calibration = self.device.readCalibration()

    def __del__(self):
        self.device.close()

    def peek_left(self):
        in_left = self.queue_left.get()
        return in_left.getCvFrame()

    def peek_apriltag(self):
        in_apriltag = self.queue_apriltag.get().aprilTags
        return in_apriltag

    def peek_rgb(self):
        in_rgb = self.queue_rgb.get()
        return in_rgb.getCvFrame()[:, :, ::-1]

    def peek_depth(self):
        in_depth = self.queue_depth.get()
        return in_depth.getFrame()

    def get_focal_length(self):
        calibration = self.device.readCalibration()
        intrinsics = calibration.getCameraIntrinsics(dai.CameraBoardSocket.RGB)
        return intrinsics[0][0]


class LDLidarSensor(Sensor):
    TOPIC = '/scan'
    MESSAGE_TYPE = 'sensor_msgs/LaserScan'
    SAMPLE_RATE = 5

    def __init__(self, buffer_size=500):
        super().__init__(buffer_size)

    def parse_message(self, message):
        return {'angle_min': message['msg']['angle_min'],
                'angle_max': message['msg']['angle_max'],
                'angle_increment': message['msg']['angle_increment'],
                'range_min': message['msg']['range_min'],
                'range_max': message['msg']['range_max'],
                'ranges': np.nan_to_num(np.array(message['msg']['ranges']).astype(np.float32))
                }
