import base64
import collections
import time
from abc import ABC, abstractmethod
from io import BytesIO

import math
import numpy as np
from PIL import Image

from robmob.sensors import Sensor
from robmob.simulation import IN_SIMULATION


class HokuyoSensor(Sensor):
    TOPIC = '/scan'
    MESSAGE_TYPE = 'sensor_msgs/LaserScan'
    SAMPLE_RATE = 10

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


class RPlidarSensor(Sensor):
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


class SharpSensor(Sensor):
    TOPIC = '/range/front' if IN_SIMULATION else '/mobile_base/sensors/core'
    MESSAGE_TYPE = 'sensor_msgs/LaserScan' if IN_SIMULATION else 'kobuki_msgs/SensorState'
    SAMPLE_RATE = 50

    # TODO which table to use?
    # Calibration table of the high range sharp sensor, for 15+ cm.
    # HIGH_RANGE_CALIB_TABLE = np.asarray([
    #     [15, 2.76],
    #     [20, 2.53],
    #     [30, 1.99],
    #     [40, 1.53],
    #     [50, 1.23],
    #     [60, 1.04],
    #     [70, 0.91],
    #     [80, 0.82],
    #     [90, 0.72],
    #     [100, 0.66],
    #     [110, 0.6],
    #     [120, 0.55],
    #     [130, 0.50],
    #     [140, 0.46],
    #     [150, 0.435],
    #     [200, 0],
    #     [np.inf, 0]
    # ])
    HIGH_RANGE_CALIB_TABLE = np.asarray(
        [[15, 2.76], [20, 2.53], [30, 1.99], [40, 1.53], [50, 1.23], [60, 1.04], [70, 0.91], [80, 0.82], [90, 0.72],
         [100, 0.66], [110, 0.6], [120, 0.55], [130, 0.50], [140, 0.46], [150, 0.435], [150, 0]])

    def __init__(self, analog_input_id=0, buffer_size=100):
        """
        There are two Sharp sensors on the robot. The analog_input_id 0 is the long range sensor
        and the analog_input_id 1 is the short range sensor.
        """
        super().__init__(buffer_size)
        self.analog_input_id = analog_input_id

    def parse_message(self, message):
        if IN_SIMULATION:
            val = message['msg']['ranges'][0]
            if val is None:
                return math.inf
            return float(val)
        else:
            return float(message['msg']['analog_input'][self.analog_input_id]) / 4096 * 3.3


class OracleSharpSensor(Sensor):
    TOPIC = '/proximity/front'
    MESSAGE_TYPE = 'sensor_msgs/LaserScan'
    SAMPLE_RATE = 50

    def __init__(self, analog_input_id=0, buffer_size=100):
        """
        Oracle sensor that can give you the ground truth distance from the sensor.
        Returns a value in cm
        """
        super().__init__(buffer_size)
        if not IN_SIMULATION:
            raise RuntimeError(f'Cannot instantiate {type(self).__name__} while not in a simulator')
        self.analog_input_id = analog_input_id

    def parse_message(self, message):
        try:
            return float(message['msg']['ranges'][0] * 100)
        except:
            return np.inf


class GyroSensor(Sensor):
    TOPIC = '/imu' if IN_SIMULATION else '/mobile_base/sensors/imu_data_raw'
    MESSAGE_TYPE = 'sensor_msgs/Imu'
    SAMPLE_RATE = 108
    SAMPLE_RATE_SIM = 930

    def __init__(self, buffer_size=None):
        if buffer_size is None:
            if IN_SIMULATION:
                buffer_size = int(self.SAMPLE_RATE_SIM * 2)
            else:
                buffer_size = int(self.SAMPLE_RATE_SIM * 2.5)
        super().__init__(buffer_size)

    def parse_message(self, message):
        return {
            'x': math.degrees(message['msg']['angular_velocity']['x']),
            'y': math.degrees(message['msg']['angular_velocity']['y']),
            'z': math.degrees(message['msg']['angular_velocity']['z'])
        }

    def format_buffer_numpy(self, buf):
        return np.asarray(list(map((lambda m: [m['x'], m['y'], m['z']]), buf)))


class KinectRGBSensor(Sensor):
    TOPIC = '/camera/color/image_raw/compressed' if IN_SIMULATION else '/kinect_rgb_compressed'
    MESSAGE_TYPE = 'sensor_msgs/CompressedImage'
    SAMPLE_RATE = 5

    def __init__(self, buffer_size=10):
        super().__init__(buffer_size)

    def parse_message(self, message):
        image_data = message['msg']['data']
        decompressed_image = Image.open(BytesIO(base64.b64decode(image_data)))
        return decompressed_image


class KinectDepthSensor(Sensor):
    TOPIC = '/camera/depth/image_raw/compressedDepth' if IN_SIMULATION else '/kinect_depth_compressed'
    MESSAGE_TYPE = 'sensor_msgs/CompressedImage' if IN_SIMULATION else 'sensor_msgs/CompressedImage'
    SAMPLE_RATE = 5
    FOCAL_LENGTH = 365.456
    CENTER_X = 254.878
    CENTER_Y = 205.395

    def __init__(self, buffer_size=10):
        super().__init__(buffer_size)

    def parse_message(self, message):
        image_data = message['msg']['data']
        data_bytes = base64.b64decode(image_data)
        data_numpy = np.asarray(Image.open(BytesIO(data_bytes[12:]))).astype(np.float32)

        old_err = np.seterr(divide='ignore')
        distances_meter = 8460.134739 / data_numpy
        distances_meter[distances_meter == np.inf] = 0.0
        np.seterr(**old_err)

        return distances_meter


class OdometerTicksSensor(Sensor):
    TOPIC = '/joint_states' if IN_SIMULATION else '/mobile_base/sensors/core'
    MESSAGE_TYPE = 'sensor_msgs/JointState' if IN_SIMULATION else 'kobuki_msgs/SensorState'
    SAMPLE_RATE = 50

    """
    <wheelSeparation>0.160</wheelSeparation>
    <wheelDiameter>0.066</wheelDiameter>
    """
    TICK_TO_METER = 1 / 30.529114682212146 if IN_SIMULATION else 0.000085292090497737556558
    ENCODER_MAX_VALUE = 65535

    def __init__(self, buffer_size=200):
        super().__init__(buffer_size)
        self.last_left = 0
        self.last_right = 0
        self.base_right = 0
        self.base_left = 0

    def parse_message(self, message):
        left = message['msg']['position'][1] if IN_SIMULATION else message['msg']['left_encoder']
        right = message['msg']['position'][0] if IN_SIMULATION else message['msg']['right_encoder']

        if left - self.last_left > 10000:
            self.base_left -= self.ENCODER_MAX_VALUE
        elif left - self.last_left < -10000:
            self.base_left += self.ENCODER_MAX_VALUE

        if right - self.last_right > 10000:
            self.base_right -= self.ENCODER_MAX_VALUE
        elif right - self.last_right < -10000:
            self.base_right += self.ENCODER_MAX_VALUE

        self.last_left = left
        self.last_right = right

        return (message['msg']['header']['stamp']['secs'] + message['msg']['header']['stamp']['nsecs'] / 1e9,
                left + self.base_left,
                right + self.base_right)


class FullOdomSensor(Sensor):
    TOPIC = '/odom'
    MESSAGE_TYPE = 'nav_msgs/Odometry'
    SAMPLE_RATE = 50

    def __init__(self, buffer_size=200):
        super().__init__(buffer_size)

    def parse_message(self, message):
        return (message['msg']['pose']['pose']['position']['x'],
                message['msg']['pose']['pose']['position']['y'],
                2 * math.acos(message['msg']['pose']['pose']['orientation']['w']))


class SimulatorSensor(Sensor):
    TOPIC = '/gazebo/performance_metrics'
    MESSAGE_TYPE = 'gazebo_msgs/PerformanceMetrics'
    SAMPLE_RATE = 6

    def __init__(self, buffer_size=10):
        super().__init__(buffer_size)

    def parse_message(self, message):
        return {'real_time_factor': message['msg']['real_time_factor']}

    def mean_real_time_factor(self):
        return np.mean([x['real_time_factor'] for x in self.buffer])
