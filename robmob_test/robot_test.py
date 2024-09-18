import time
import unittest

import matplotlib.pyplot as plt
import numpy as np

from robmob.robot import Robot
from robmob.rover.commands import ResetCommand, MovementPWMCommand
from robmob.rover.sensors import RobotEspSensor, SharpSensor, CameraRGBSensor, CameraDepthSensor


class TestRobot(unittest.TestCase):
    def test_connect(self):
        robot = Robot('localhost', port=9090)
        robot.connect()
        self.assertTrue(robot.connection_established)

    def test_range(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = SharpSensor()
        robot.add_sensor(sensor)

        time.sleep(2)
        msg = sensor.peek_data()
        assert isinstance(msg, float)

    def test_receive_msg(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = RobotEspSensor()
        robot.add_sensor(sensor)

        time.sleep(1)
        msg = sensor.peek_data()

        for k in (
                'speedGetA', 'speedGetB', 'gx', 'gy', 'gz', 'ax', 'ay', 'az', 'mx', 'my', 'mz', 'rgx', 'rgy', 'rgz',
                'rax', 'ray', 'raz', 'rmx', 'rmy', 'rmz', 'ax_offset', 'ay_offset', 'az_offset', 'gx_offset',
                'gy_offset', 'gz_offset', 'en_odom_l', 'en_odom_r', 'loadVoltage_V'):
            self.assertTrue(k in msg)

    def test_send_message(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = RobotEspSensor()
        robot.add_sensor(sensor)

        time.sleep(0.5)
        start = sensor.peek_data()

        robot.send_command(MovementPWMCommand(255, 127))
        # robot.send_command(MovementFloatCommand(1, 0.5))
        # robot.send_command(MovementCommand(1, 0))
        time.sleep(1)
        robot.send_command(ResetCommand())

        time.sleep(0.1)
        end = sensor.peek_data()

        dodl = end['en_odom_l'] - start['en_odom_l']
        dodr = end['en_odom_r'] - start['en_odom_r']

        self.assertTrue(dodl > 0)
        self.assertTrue(dodr > 0)

    def test_plot(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = RobotEspSensor()
        robot.add_sensor(sensor)
        time.sleep(0.1)

        gz = []
        for i in range(100):
            time.sleep(0.02)
            gz.append(sensor.peek_data()['rgz'])

        import matplotlib.pyplot as plt
        plt.plot(gz)
        plt.show()

    def test_camera_rgb(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = CameraRGBSensor()
        robot.add_sensor(sensor)
        time.sleep(3)

        img = sensor.peek_data()
        print(img)
        assert img is not None
        assert img.size == (1920, 1080)

    def test_camera_depth(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = CameraDepthSensor()
        robot.add_sensor(sensor)
        time.sleep(3)
        while True:
            ...

        img = sensor.peek_data()
        print(img)
        assert img is not None
        assert img.size == (640, 480)
        x = np.array(img)
        plt.hist(x.flatten(), bins=256)
        plt.show()
