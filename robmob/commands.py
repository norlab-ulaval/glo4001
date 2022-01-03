import _thread
import json
import time

DO_NOT_SEND_REPEATEDLY_FLAG = None
DEFAULT_LINEAR_SPEED = 0.12
DEFAULT_ANGULAR_SPEED = 1.0
MAX_LINEAR_SPEED = 0.4
MAX_ANGULAR_SPEED = 1.8


class RosTwistMessage:

    def __init__(self, linear_velocity, angular_velocity):
        self.message = {
            'linear': {
                'x': linear_velocity,
                'y': 0.0,
                'z': 0.0
            },
            'angular': {
                'x': 0.0,
                'y': 0.0,
                'z': angular_velocity
            }
        }


class CommandPublisher:

    def __init__(self):
        self.stop = False

    def start_publishing(self, send_fn, command):
        command_json = json.dumps(command.message_to_publish)
        frequency_hz = command.publish_frequency_hz

        if frequency_hz == DO_NOT_SEND_REPEATEDLY_FLAG:
            send_fn(command_json)
        else:
            _thread.start_new_thread(self._publish_repeatedly, (send_fn, command_json, frequency_hz))

    def stop_publishing(self):
        self.stop = True

    def _publish_repeatedly(self, send_fn, json, frequency_hz):
        sleep_time_sec = 1.0 / frequency_hz
        while not self.stop:
            send_fn(json)
            time.sleep(sleep_time_sec)


class Command:
    def __init__(self, send_frequency_hz=10):
        self.publish_frequency_hz = send_frequency_hz
        self.message_to_publish = {
            'op': 'publish',
            'topic': '/mobile_base/commands/velocity'
        }

    def _add_twist_message(self, twist):
        self.message_to_publish['msg'] = twist.message


class ResetCommand(Command):
    def __init__(self):
        super().__init__(DO_NOT_SEND_REPEATEDLY_FLAG)
        self._add_twist_message(RosTwistMessage(0, 0))


class MovementCommand(Command):
    def __init__(self, linear, angular):
        super().__init__()
        if abs(linear) > MAX_LINEAR_SPEED:
            raise ValueError(
                'La vitesse fournie est trop grande. La vitesse maximale du robot est {}'.format(MAX_LINEAR_SPEED))
        if abs(angular) > MAX_ANGULAR_SPEED:
            raise ValueError(
                'La vitesse linéaire fournie est trop grande. La vitesse de rotation maximale du robot est {}'.format(
                    MAX_ANGULAR_SPEED))

        self._add_twist_message(RosTwistMessage(linear, angular))


class RotationCommand(MovementCommand):
    def __init__(self, speed):
        super().__init__(0.0, speed)


class LinearMovementCommand(MovementCommand):
    def __init__(self, speed):
        super().__init__(speed, 0.0)


class TurnLeftCommand(RotationCommand):
    def __init__(self):
        super().__init__(DEFAULT_ANGULAR_SPEED)


class TurnRightCommand(RotationCommand):
    def __init__(self):
        super().__init__(-DEFAULT_ANGULAR_SPEED)


class MoveForwardCommand(LinearMovementCommand):
    def __init__(self):
        super().__init__(DEFAULT_LINEAR_SPEED)


class MoveBackwardCommand(LinearMovementCommand):
    def __init__(self):
        super().__init__(-DEFAULT_LINEAR_SPEED)
