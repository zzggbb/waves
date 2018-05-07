"""
    stream.py
    Provide audio to waves.py
    Handle device and host api enumeration
    Handle stream parameter changes such as sampling rate and sample size
"""

import pyaudio

class Stream(object):
    def __init__(self, channels, sample_rate, sample_size):
        self._pa = pyaudio.PyAudio()
        self._stream = None
        self._channels = channels
        self._sample_rate = sample_rate
        self._sample_size = sample_size
        self.open()

    def read(self, sample_size):
        return self._stream.read(sample_size)

    def open(self):
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                   channels=self._channels,
                                   rate=self._sample_rate,
                                   frames_per_buffer=self._sample_size,
                                   input=True)

    def close(self):
        self._stream.close()
        self._pa.terminate()

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        self._stream.close()
        self._sample_rate = sample_rate
        self.open()

    @property
    def sample_size(self):
        return self._sample_size

    @sample_size.setter
    def sample_size(self, sample_size):
        self._stream.close()
        self._sample_size = int(sample_size)
        self.open()
