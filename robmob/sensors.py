import collections
import time
from abc import ABC, abstractmethod

import numpy as np


class Sensor(ABC):
    # Overwrite in implementations
    TOPIC = ''
    MESSAGE_TYPE = ''
    SAMPLE_RATE = 0

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = collections.deque([], maxlen=buffer_size)
        self.continuous_buffer = None
        self.subscription_message = {'op': 'subscribe',
                                     'type': self.MESSAGE_TYPE,
                                     'topic': self.TOPIC}
        self.unsubscribe_message = {'op': 'unsubscribe',
                                    'topic': self.TOPIC}

    @abstractmethod
    def parse_message(self, message):
        ...

    def on_message(self, message):
        parsed_message = self.parse_message(message)
        self.buffer.append(parsed_message)
        if self.continuous_buffer is not None:
            self.continuous_buffer.append(parsed_message)

    def read_data(self):
        try:
            return self.buffer.popleft()
        except IndexError:
            raise IndexError('Le buffeur du capteur est vide')

    def peek_data(self):
        try:
            return self.buffer[-1]
        except IndexError:
            raise IndexError('Le buffeur du capteur est vide')

    def read_buffer(self):
        old_buffer = self.buffer
        self.buffer = collections.deque([], maxlen=self.buffer_size)
        return self.format_buffer_numpy(old_buffer)

    def peek_buffer(self):
        return self.format_buffer_numpy(self.buffer)

    def sample_data_for_x_sec(self, x):
        self.continuous_buffer = []
        time.sleep(x)
        samples, self.continuous_buffer = self.continuous_buffer, None
        return self.format_buffer_numpy(samples)

    def format_buffer_numpy(self, buf):
        return np.asarray(buf)
