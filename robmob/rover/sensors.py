import ast

import numpy as np

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
