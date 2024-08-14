import ast
import time

from robmob.robot import Robot
import unittest

from robmob.kobuki.sensors import Sensor
from robmob.rover.commands import MovementFloatCommand, ResetCommand, MovementCommand, MovementPWMCommand
from robmob.rover.sensors import RobotEspSensor


class TestRobot(unittest.TestCase):
    def test_connect(self):
        robot = Robot('localhost', port=9090)
        robot.connect()
        self.assertTrue(robot.connection_established)

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
