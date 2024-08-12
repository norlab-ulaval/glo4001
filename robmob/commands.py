import _thread
import json
import time


class CommandPublisher:
    def __init__(self):
        self.stop = False

    def start_publishing(self, send_fn, command):
        command_json = json.dumps(command.message_to_publish)
        frequency_hz = command.publish_frequency_hz

        if frequency_hz is Command.SEND_ONCE:
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
    SEND_ONCE = None
    # Overwrite this in implementations if required
    COMMAND_TOPIC = ''

    def __init__(self, send_frequency_hz=10):
        self.publish_frequency_hz = send_frequency_hz
        self.message_to_publish = {
            'op': 'publish',
            'topic': self.COMMAND_TOPIC
        }

    def _set_message(self, msg):
        self.message_to_publish['msg'] = msg.message
