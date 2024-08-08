from overrides import overrides

from robmob.commands import Command


class RoverCommand(Command):
    COMMAND_TOPIC = '/rover/command'

    def __init__(self, send_frequency_hz=10):
        super().__init__(send_frequency_hz)
        self.message_to_publish['type'] = 'std_msgs/msg/String'

    @overrides
    def _set_message(self, msg):
        msg = self._to_ros_string(msg)
        self.message_to_publish['msg'] = msg

    def _to_ros_string(self, data):
        return {'data': str(data)}


class MovementCommand(RoverCommand):
    def __init__(self, linear, angular):
        super().__init__()
        self._set_message({"T": 13, "X": linear, "Y": angular})


class ResetCommand(RoverCommand):
    def __init__(self):
        super().__init__(Command.SEND_ONCE)
        self._set_message({"T": 13, "X": 0, "Y": 0})


class MovementFloatCommand(RoverCommand):
    def __init__(self, left: float, right: float):
        super().__init__()
        self._set_message({"T": 1, "L": left, "R": right})


class MovementPWMCommand(RoverCommand):
    def __init__(self, left: int, right: int):
        super().__init__()
        self._set_message({"T": 11, "L": left, "R": right})
