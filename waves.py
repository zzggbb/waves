#!/bin/env python3
import sys
import time
import struct

import numpy
import pygame
import pyaudio

import util
import controls
from stream import Stream
from outputs import Outputs

class Waves(object):
    def __init__(self):
        pygame.init()

        self.outputs = Outputs()
        self.stream = Stream(channels=1,
                             sample_rate=44100,
                             sample_size=2048)
        # visual params
        self.background_color = pygame.Color(50, 50, 50)
        self.colorA = pygame.Color("#ff0000")
        self.colorB = pygame.Color("#0000ff")
        self.gain = 0.5
        self.num_bars = self.outputs.get_divisor()
        self.shift_function = util.shift_parabola

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

        self.controls = controls.Controls(self.control_surface)
        smooth_slider_rect = pygame.Rect(300, 65, 100, 10)
        self.smooth_slider = controls.Slider(self.control_surface,
                                      smooth_slider_rect, 10, 20, value=0.5)

        # smoothing history arrays
        self.t_history = numpy.full(self.num_bars, 0.5)
        self.f_history = numpy.full(self.num_bars, 0.0)

    def get_samples(self):
        format = '<{}h'.format(self.stream.sample_size)
        byte_string = self.stream.read(self.stream.sample_size)
        return list(map(util.normalize, struct.unpack(format, byte_string)))

    def draw_time_bars(self, samples, surface):
        width, height = surface.get_size()
        bar_width = width / self.num_bars

        for i in range(self.num_bars):
            power_i = samples[i]
            # smooth between current and last power
            s = self.smooth_slider.value
            power_s = self.t_history[i]*s + power_i*(1-s)
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
        y_max = self.stream.sample_size // 2
        bar_width = width / self.num_bars

        yf = numpy.log(numpy.abs(numpy.fft.fft(samples))+1)/numpy.log(y_max)

        x_max = self.num_bars - 1
        for x in range(self.num_bars):
            y = self.shift_function(x, x_max, y_max)
            s = self.smooth_slider.value
            power_i = yf[int(y)]
            power_s = self.f_history[x]*s + power_i*(1-s)
            power = self.f_history[x] = power_s
            bar_height = power * height
            top = height - bar_height
            left = x * bar_width
            rect = (left, top, bar_width, bar_height)
            color = util.gradient(x/self.num_bars, self.colorA, self.colorB)
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

    def process_key(self, key):
        GAIN_DELTA = 0.01
        GAIN_MAX = 1 - GAIN_DELTA
        GAIN_MIN = 0
        RATE_DELTA = 2500
        RATE_MIN = 0
        SIZE_MIN = 1

        mods = pygame.key.get_mods()
        shift = mods & pygame.KMOD_SHIFT

        if key == ord('p'):
            self.shift_function = util.shift_parabola

        if key == ord('e'):
            self.shift_function = util.shift_ellipse

        if key == ord('l'):
            self.shift_function = util.shift_linear

        if key == ord('b'):
            if shift:
                self.outputs.next_divisor()
            else:
                self.outputs.prev_divisor()
            self.resize_bars()

        if key == ord('g'):
            k = 1 if shift else -1
            if GAIN_MIN < self.gain < GAIN_MAX :
                self.gain += (k * GAIN_DELTA)

        if key == ord('n'):
            k = 2 if shift else 0.5
            if self.stream.sample_size > SIZE_MIN:
                self.stream.sample_size *= k

        if key == ord('r'):
            k = 1 if shift else -1
            if self.stream.sample_rate > RATE_MIN:
                self.stream.sample_rate += k * 2500

        if key == ord('w'):
            if shift:
                self.outputs.next_width()
            else:
                self.outputs.prev_width()
            self.resize_width()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

            if event.type == pygame.KEYDOWN:
                self.process_key(event.key)

            if event.type == pygame.MOUSEMOTION:
                if self.smooth_slider.moving:
                    self.smooth_slider.set_value(event.pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.smooth_slider.get_handle_rect().collidepoint(event.pos):
                    self.smooth_slider.moving = True

            if event.type == pygame.MOUSEBUTTONUP and self.smooth_slider.moving:
                self.smooth_slider.moving = False

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
                           self.smooth_slider.value,
                           self.width,
                           self.num_bars)

        self.smooth_slider.draw()

        self.draw_time_bars(samples, self.time_surface)
        self.draw_freq_bars(samples, self.freq_surface)

        self.surface.blit(self.time_surface, (0,0))
        self.surface.blit(self.freq_surface, (0,540))
        self.surface.blit(self.control_surface, (0,0))

        pygame.display.flip()

if __name__ == '__main__':
    waves = Waves()
    clock = pygame.time.Clock()
    while True:
        try:
            waves.loop()
            clock.tick(400)
        except KeyboardInterrupt:
            waves.exit()
