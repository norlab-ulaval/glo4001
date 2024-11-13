import time
import unittest

import matplotlib.pyplot as plt

from robmob.robot import Robot
from robmob.rover.commands import ResetCommand, MovementPWMCommand
from robmob.rover.sensors import RobotEspSensor, SharpSensor, CameraRGBSensor, CameraDepthSensor, OakLiteCamera, \
    LDLidarSensor


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

    def test_camera_rgb_oak(self):
        camera = OakLiteCamera(use_rgb=True)
        img = camera.peek_rgb()
        assert img.shape == (1080, 1920, 3)
        plt.imshow(img)
        plt.show()

    def test_camera_left_oak(self):
        camera = OakLiteCamera()
        img = camera.peek_left()
        assert img.shape == (480, 640)
        plt.imshow(img, cmap='gray')
        plt.show()

    def test_camera_depth_oak(self):
        camera = OakLiteCamera(use_depth=True)
        img = camera.peek_depth()
        assert img.shape == (480, 640)
        # normalize
        img = (img - img.min()) / (img.max() - img.min())
        plt.imshow(img)
        plt.show()

    def test_camera_apriltag(self):
        camera = OakLiteCamera(use_april=True)
        tag = camera.peek_apriltag()
        print(tag)

    def test_lidar(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = LDLidarSensor()
        robot.add_sensor(sensor)

        time.sleep(2)
        msg = sensor.peek_data()
        print(msg)

