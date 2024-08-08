import ast
import time

from robmob.robot import Robot
import unittest

from robmob.kobuki.sensors import Sensor


class RobotEspSensor(Sensor):
    TOPIC = '/rover/state'
    MESSAGE_TYPE = 'std_msgs/msg/String'
    SAMPLE_RATE = 10

    def __init__(self, buffer_size=100000):
        super().__init__(buffer_size)

    def parse_message(self, message):
        data = message['msg']['data']
        return ast.literal_eval(data)


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

        self.assertTrue(
            all(k in msg for k in ('rax', 'ray', 'raz', 'mx', 'my', 'mz', 'rgx', 'rgy', 'rgz', 'odl', 'odr')))

    def test_send_message(self):
        robot = Robot('localhost', port=9090)
        robot.connect()

        sensor = RobotEspSensor()
        robot.add_sensor(sensor)

        time.sleep(0.1)
        start = sensor.peek_data()

        robot.send_command(MovementFloatCommand(0.5, 0.5))
        time.sleep(1)
        robot.send_command(ResetCommand())

        end = sensor.peek_data()

        dodl = end['odl'] - start['odl']
        dodr = end['odr'] - start['odr']

        self.assertTrue(dodl > 0)
        self.assertTrue(dodr > 0)
