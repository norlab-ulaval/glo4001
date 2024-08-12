import ast

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
