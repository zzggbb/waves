#!/bin/env python3
import sys
import time
import struct

import numpy
import pygame
import pyaudio

import util
from stream import Stream
from outputs import Outputs
from controls import Controls

class Waves(object):
    def __init__(self):
        pygame.init()

        self.outputs = Outputs()
        self.stream = Stream(channels=1,
                             sample_rate=40 * 10**3,
                             sample_size=2048)
        # visual params
        self.background_color = pygame.Color(50, 50, 50)
        self.colorA = pygame.Color(255, 0, 255)
        self.colorB = pygame.Color(0, 255, 255)
        self.smooth = 0.5
        self.gain = 0.5
        self.num_bars = self.outputs.get_divisor()

        # surface params
        self.width, self.height = self.outputs.get_width(), 1080
        self.surface_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.surface = pygame.display.set_mode(
            (self.width, self.height), self.surface_flags
        )
        self.time_surface = pygame.Surface((self.width, self.height // 2))
        self.freq_surface = pygame.Surface((self.width, self.height // 2))
        self.control_surface = pygame.Surface((self.width // 2, self.height // 2))
        self.control_surface.set_colorkey(self.background_color)

        self.controls = Controls(self.control_surface)

        # smoothing history arrays
        self.t_history = numpy.full(self.num_bars, 0.5)
        self.f_history = numpy.full(self.num_bars, 0.0)

    def get_samples(self):
        format = '<{}h'.format(self.stream.sample_size)
        byte_string = self.stream.read(self.stream.sample_size)
        return struct.unpack(format, byte_string)

    def draw_time_bars(self, samples, surface):
        width, height = surface.get_size()
        bar_width = width / self.num_bars

        for i in range(self.num_bars):
            power_i = util.normalize(samples[i])
            # smooth between current and last power
            power_s = self.t_history[i]*self.smooth + power_i*(1-self.smooth)
            # finally, smoothed and gain adjusted
            power = self.t_history[i] = util.gain(power_s, self.gain)

            bar_height = power * height
            top = height - bar_height
            left = i * bar_width
            rect = (left, top, bar_width, bar_height)

            color = util.gradient(power, self.colorA, self.colorB)
            pygame.draw.rect(surface, color, rect)

    def draw_freq_bars(self, samples, surface):
        width, height = surface.get_size()
        length = self.stream.sample_size // 2
        bar_width = width / self.num_bars

        normalized = list(map(util.normalize, samples))

        yf = numpy.log(numpy.abs(numpy.fft.fft(normalized))+1)/numpy.log(length)

        x_max = self.num_bars - 1
        for i in range(self.num_bars):
            y = -1 * numpy.sqrt(
                    (1 - (i**2)/(x_max**2)) * length**2
                ) + length + 1
            bar_height = yf[int(y)] * height
            top = height - bar_height
            left = i * bar_width
            rect = (left, top, bar_width, bar_height)
            color = util.gradient(i/self.num_bars, self.colorA, self.colorB)
            pygame.draw.rect(surface, color, rect)

    def resize_bars(self):
        self.num_bars = self.outputs.get_divisor()
        self.t_history.resize(self.num_bars)
        self.f_history.resize(self.num_bars)

    def resize_width(self):
        self.width = self.outputs.get_width()
        self.time_surface = pygame.Surface((self.width, self.height // 2))
        self.freq_surface = pygame.Surface((self.width, self.height // 2))
        self.surface = pygame.display.set_mode(
            (self.width, self.height), self.surface_flags
        )
        self.resize_bars()

    def process_events(self):
        GAIN_DELTA = 0.01
        GAIN_MAX = 1 - GAIN_DELTA
        GAIN_MIN = 0
        SMOOTH_DELTA = 0.01
        SMOOTH_MAX = 1
        SMOOTH_MIN = 0 + GAIN_DELTA
        RATE_DELTA = 2500
        RATE_MIN = 0
        SIZE_MIN = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                shift = mods & pygame.KMOD_SHIFT

                if event.key == ord('b'):
                    if shift:
                        self.outputs.next_divisor()
                    else:
                        self.outputs.prev_divisor()
                    self.resize_bars()

                if event.key == ord('g'):
                    k = 1 if shift else -1
                    if GAIN_MIN < self.gain < GAIN_MAX :
                        self.gain += (k * GAIN_DELTA)

                if event.key == ord('n'):
                    k = 2 if shift else 0.5
                    if self.stream.sample_size > SIZE_MIN:
                        self.stream.sample_size *= k

                if event.key == ord('r'):
                    k = 1 if shift else -1
                    if self.stream.sample_rate > RATE_MIN:
                        self.stream.sample_rate += k * 2500

                if event.key == ord('s'):
                    if shift and self.smooth < SMOOTH_MAX:
                        self.smooth += SMOOTH_DELTA
                    if not shift and self.smooth > SMOOTH_MIN:
                        self.smooth -= SMOOTH_DELTA

                if event.key == ord('w'):
                    if shift:
                        self.outputs.next_width()
                    else:
                        self.outputs.prev_width()
                    self.resize_width()

    def exit(self):
        self.stream.close()
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)

    def loop(self):
        self.process_events()

        surfaces = [self.time_surface, self.freq_surface, self.control_surface]
        for surface in surfaces:
            surface.fill(self.background_color)

        samples = self.get_samples()

        self.controls.draw(self.stream.sample_rate,
                           self.stream.sample_size,
                           self.gain,
                           self.smooth,
                           self.width,
                           self.num_bars)
        self.draw_time_bars(samples, self.time_surface)
        self.draw_freq_bars(samples, self.freq_surface)

        self.surface.blit(self.time_surface, (0,0))
        self.surface.blit(self.freq_surface, (0,540))
        self.surface.blit(self.control_surface, (0,0))

        pygame.display.flip()

if __name__ == '__main__':
    waves = Waves()
    while True:
        try:
            waves.loop()
        except KeyboardInterrupt:
            waves.exit()
