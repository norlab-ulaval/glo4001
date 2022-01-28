import base64
import collections
import math
import time
from io import BytesIO

import numpy as np
from PIL import Image

IN_SIMULATION = True


class Sensor:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = collections.deque([], maxlen=buffer_size)
        self.continuous_buffer = None
        self.subscription_message = {'op': 'subscribe',
                                     'type': self.MESSAGE_TYPE,
                                     'topic': self.TOPIC}
        self.unsubscribe_message = {'op': 'unsubscribe',
                                    'topic': self.TOPIC}

    def on_message(self, message):
        parsed_message = self.parse_message(message)
        self.buffer.append(parsed_message)
        if self.continuous_buffer != None:
            self.continuous_buffer.append(parsed_message)

    def read_data(self):
        try:
            return self.buffer.popleft()
        except IndexError:
            raise IndexError('Le buffeur du capteur est vide')

    def peek_data(self):
        try:
            return self.buffer[-1]
        except IndexError:
            raise IndexError('Le buffeur du capteur est vide')

    def read_buffer(self):
        old_buffer = self.buffer
        self.buffer = collections.deque([], maxlen=self.buffer_size)
        return self.format_buffer_numpy(old_buffer)

    def peek_buffer(self):
        return self.format_buffer_numpy(self.buffer)

    def sample_data_for_x_sec(self, x):
        self.continuous_buffer = []
        time.sleep(x)
        samples, self.continuous_buffer = self.continuous_buffer, None
        return self.format_buffer_numpy(samples)

    def format_buffer_numpy(self, buf):
        return np.asarray(buf)


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

    # Calibration table of the high range sharp sensor, for 15+ cm.
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

    def __init__(self, buffer_size=200):
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
    FOV_X = 365.456
    FOV_Y = 365.456
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
    TICK_TO_METER = 0.000085292090497737556558  # TODO simulation
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
