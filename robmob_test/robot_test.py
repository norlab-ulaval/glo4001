import ast
import time

import numpy as np

from robmob.robot import Robot
import unittest

from robmob.sensors import Sensor


class RobotEspSensor(Sensor):
    TOPIC = '/rover'
    MESSAGE_TYPE = 'std_msgs/msg/String'
    SAMPLE_RATE = 10

    def __init__(self, buffer_size=100000):
        super().__init__(buffer_size)

    def parse_message(self, message):
        data = message['msg']['data']
        d = ast.literal_eval(data)
        return {k: d[k] for k in ('rax', 'ray', 'raz', 'mx', 'my', 'mz', 'rgx', 'rgy', 'rgz')}


class TestRobot(unittest.TestCase):
    def test_connect(self):
        robot = Robot('localhost', port=9090)
        robot.connect()
        self.assertTrue(robot.connection_established)

    def test_send_message(self):
        robot = Robot('localhost', port=9090)
        robot.connect()
        robot.linear_movement(0.3, 1)
        self.assertTrue(False)

    def test_receive_msg(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = RobotEspSensor()
        robot.add_sensor(sensor)

        time.sleep(0.1)
        msg = sensor.peek_data()

        self.assertTrue(all(k in msg for k in ('rax', 'ray', 'raz', 'mx', 'my', 'mz', 'rgx', 'rgy', 'rgz')))
