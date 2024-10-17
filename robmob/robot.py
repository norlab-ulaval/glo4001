import _thread
import json
import time
import urllib.parse

import numpy as np
import websocket

from robmob.commands import CommandPublisher
from robmob.rover.commands import ResetCommand, MovementFloatCommand


class Robot:
    DISTANCE_CENTER_TO_WHEEL = 12.5 / 200
    BASELINE = 2 * DISTANCE_CENTER_TO_WHEEL
    WHEEL_DIAMETER = 80 / 1000
    WHEEL_RADIUS = WHEEL_DIAMETER / 2

    def __init__(self, robot_ip, port=9090):
        self.ws = None
        self.publisher = None
        self.odom = None
        self.sensors = {}
        self.robot_url = 'ws://' + robot_ip + ':' + str(port)
        self.connection_established = False
        self.connecting = False
        self.inverse_skid = self._inverse_skid_steer_matrix()

        try:
            urllib.parse.urlparse(self.robot_url)
        except ValueError:
            raise ValueError(f"Robot address {robot_ip}:{port} is not valid")

    def __del__(self):
        self.disconnect()

    def _inverse_skid_steer_matrix(self):
        skid_matrix = self.WHEEL_RADIUS * np.array([[0.5, 0.5],
                                                    [-1 / self.BASELINE, 1 / self.BASELINE]])
        inverse_skid_matrix = np.linalg.inv(skid_matrix)
        return inverse_skid_matrix

    def _compute_wheel_speeds(self, linear, angular):
        return self.inverse_skid @ np.array([linear, angular])

    def _map_to_motor_speeds(self, speeds):
        speeds = speeds * self.WHEEL_RADIUS
        return np.clip(speeds, -1, 1)

    def _command_to_motor_speeds(self, linear, angular):
        speeds = self._compute_wheel_speeds(linear, angular)
        return self._map_to_motor_speeds(speeds)

    def connect(self):
        self.ws = websocket.WebSocketApp(self.robot_url,
                                         on_message=self._on_message,
                                         on_error=self._on_error,
                                         on_close=self._on_close,
                                         on_open=self._on_open)

        self.connecting = True

        _thread.start_new_thread(self.ws.run_forever, ())

        # on_error will set self.connecting to false if we timeout.
        while not self.connection_established and self.connecting:
            time.sleep(0.2)

    def add_sensor(self, sensor):
        self.ws.send(json.dumps(sensor.subscription_message))

        if sensor.TOPIC in self.sensors:
            self.sensors[sensor.TOPIC].append(sensor)
        else:
            self.sensors[sensor.TOPIC] = [sensor]

    def send_command(self, command):
        if self.publisher:
            self.publisher.stop_publishing()
        self.publisher = CommandPublisher()
        self.publisher.start_publishing(self.ws.send, command)

    def disconnect(self):
        self.ws.keep_running = False

    def general_movement(self, linear, angular, duration):
        speed_l, speed_r = self._command_to_motor_speeds(linear, angular)
        self.send_command(MovementFloatCommand(speed_l, speed_r))
        time.sleep(duration)
        self.send_command(ResetCommand())

    def linear_movement(self, speed, duration):
        self.general_movement(speed, 0, duration)

    def _moved_distance(self, initial_x, initial_y, x, y):
        return ((x - initial_x) ** 2 + (y - initial_y) ** 2) ** 0.5

    # def linear_movement_precise(self, distance, speed):
    #     if not self.odom:
    #         self.odom = FullOdomSensor()
    #         self.add_sensor(self.odom)
    #         time.sleep(0.4)
    #
    #     breaking_distance = speed / 0.05 * 0.0025  # Very approximative
    #     initial_x, initial_y, _ = self.odom.peek_data()
    #     x, y = initial_x, initial_y
    #     command = LinearMovementCommand(speed)
    #     self.send_command(command)
    #     while self._moved_distance(initial_x, initial_y, x, y) < distance - breaking_distance:
    #         time.sleep(0.5 / self.odom.SAMPLE_RATE)
    #         x, y, _ = self.odom.peek_data()
    #     self.send_command(ResetCommand())

    def angular_movement(self, angular_speed, duration):
        self.general_movement(0, angular_speed, duration)

    def _on_message(self, _, raw_message):
        parsed_message = json.loads(raw_message)
        message_topic = parsed_message['topic']

        if message_topic in self.sensors:
            [s.on_message(parsed_message) for s in self.sensors[message_topic]]

    def _on_open(self, *args, **kargs):
        self.connecting = False
        self.connection_established = True

    def _on_error(self, *args, **kargs):
        self.connecting = False
        raise RuntimeError('Échec de la connexion au robot')

    def _on_close(self, *args, **kargs):
        pass
