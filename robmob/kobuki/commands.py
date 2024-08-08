import _thread
import json
import time

from robmob.commands import Command
from robmob.simulation import IN_SIMULATION

DO_NOT_SEND_REPEATEDLY_FLAG = None
DEFAULT_LINEAR_SPEED = 0.12
DEFAULT_ANGULAR_SPEED = 1.0
MAX_LINEAR_SPEED = 0.4
MAX_ANGULAR_SPEED = 1.8

SIMULATION_COMMAND_TOPIC = '/cmd_vel'
ROBOT_COMMAND_TOPIC = '/mobile_base/commands/velocity'
COMMAND_TOPIC = SIMULATION_COMMAND_TOPIC if IN_SIMULATION else ROBOT_COMMAND_TOPIC


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


class KobukiCommand(Command):
    COMMAND_TOPIC = COMMAND_TOPIC


class ResetCommand(KobukiCommand):
    def __init__(self):
        super().__init__(DO_NOT_SEND_REPEATEDLY_FLAG)
        self._set_message(RosTwistMessage(0, 0))


class MovementCommand(KobukiCommand):
    def __init__(self, linear, angular):
        super().__init__()
        if abs(linear) > MAX_LINEAR_SPEED:
            raise ValueError(
                'La vitesse fournie est trop grande. La vitesse maximale du robot est {}'.format(MAX_LINEAR_SPEED))
        if abs(angular) > MAX_ANGULAR_SPEED:
            raise ValueError(
                'La vitesse linéaire fournie est trop grande. La vitesse de rotation maximale du robot est {}'.format(
                    MAX_ANGULAR_SPEED))

        self._set_message(RosTwistMessage(linear, angular))


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
