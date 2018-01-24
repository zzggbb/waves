#!/bin/env python3
import sys
import time
import struct

import numpy
import pygame
import pyaudio

from stream import Stream
from controls import Controls
import util

class Waves(object):
    def __init__(self):
        pygame.init()

        # surface params
        self.size = (self.width, self.height) = (960, 1080)
        self.surface_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.surface = pygame.display.set_mode(self.size, self.surface_flags)
        self.time_surface = pygame.Surface((self.width, self.height // 2))
        self.freq_surface = pygame.Surface((self.width, self.height // 2))

        # visual params
        self.background_color = pygame.Color(255, 255, 255)
        self.colorA = pygame.Color(255, 0, 0)
        self.colorB = pygame.Color(0, 0, 255)
        self.smooth = 0.5
        self.gain = 0.5

        self.stream = Stream(channels=1,
                             sample_rate=20 * 10**3,
                             sample_size=960)
        self.stream.open()
        self.controls = Controls(self.surface)

        # smoothing history arrays
        self.last_t_power = numpy.full(self.stream.sample_size, 0.5)
        self.last_f_power = numpy.full(self.stream.sample_size // 2, 0.0)

    def get_samples(self):
        format = '<{}h'.format(self.stream.sample_size)
        byte_string = self.stream.read(self.stream.sample_size)
        return struct.unpack(format, byte_string)

    def draw_time_bars(self, samples, surface):
        width, height = surface.get_size()
        bar_width = width / self.stream.sample_size

        for i in range(self.stream.sample_size):
            # current power
            power_i = util.normalize(samples[i])
            # smooth between current and last power
            power_s = self.last_t_power[i]*self.smooth + power_i*(1-self.smooth)
            # finally, smoothed and gain adjusted
            power = self.last_t_power[i] = util.gain(power_s, self.gain)

            bar_height = power * height
            top = height - bar_height
            left = i * bar_width
            rect = (left, top, bar_width, bar_height)

            color = util.gradient(power, self.colorA, self.colorB)
            pygame.draw.rect(surface, color, rect)

    def draw_freq_bars(self, samples, surface):
        length = self.stream.sample_size // 2

        width, height = surface.get_size()
        bar_width = width / length

        normalized = list(map(util.normalize, samples))

        yf = numpy.abs(numpy.fft.fft(normalized)[1:length])
        yf *= (2.0 / numpy.sqrt(self.stream.sample_size))

        for i in range(length - 1):
            bar_height = yf[i] * height
            top = height - bar_height
            left = i * bar_width
            rect = (left, top, bar_width, bar_height)
            pygame.draw.rect(surface, self.colorA, rect)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stream.close()
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.stream.sample_size //= 2
                    self.last_t_power.resize(self.stream.sample_size)
                    self.last_f_power.resize(self.stream.sample_size // 2)

                if event.key == pygame.K_l:
                    self.stream.sample_size *= 2
                    self.last_t_power.resize(self.stream.sample_size)
                    self.last_f_power.resize(self.stream.sample_size // 2)

                if event.key == pygame.K_j:
                    self.stream.sample_rate -= 2500

                if event.key == pygame.K_k:
                    self.stream.sample_rate += 2500

                if event.key == pygame.K_t:
                    self.gain += 0.01

                if event.key == pygame.K_g:
                    self.gain -= 0.01

    def loop(self):
        self.process_events()

        for surface in self.time_surface, self.freq_surface:
            surface.fill(self.background_color)

        samples = self.get_samples()

        self.draw_time_bars(samples, self.time_surface)
        self.draw_freq_bars(samples, self.freq_surface)

        self.surface.blit(self.time_surface, (0,0))
        self.surface.blit(self.freq_surface, (0,540))

        self.controls.draw(self.stream.sample_rate,
                           self.stream.sample_size,
                           self.gain)

        pygame.display.flip()

if __name__ == '__main__':
    waves = Waves()
    while True:
        try:
            waves.loop()
        except KeyboardInterrupt:
            print('please close the window instead of using control-c!')
