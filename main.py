#!/bin/env python3

import sys
import time
import math
import struct

import numpy
import pygame
import pyaudio

import util

from slider import Slider
from controls import Controls
from stream import Stream
from outputs import Outputs

class Waves(object):
  def __init__(self):
    pygame.init()

    self.outputs = Outputs()
    self.stream = Stream(channels=1, sample_rate=60*10**3, sample_size=2**11)

    self.mouse_frequency = 0.0

    # visual params
    self.background_color = pygame.Color(50, 50, 50)
    self.colorA = pygame.Color("#ff0000")
    self.colorB = pygame.Color("#0000ff")
    self.num_bars = self.outputs.get_divisor()

    # surface params
    self.height = 1000
    self.dimensions = numpy.array([self.outputs.get_width(), self.height])
    self.surface_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    self.surface = pygame.display.set_mode(self.dimensions, self.surface_flags)
    self.time_surface = pygame.Surface(self.dimensions // numpy.array([1,2]))
    self.freq_surface = pygame.Surface(self.dimensions // numpy.array([1,2]))
    self.control_surface = pygame.Surface(self.dimensions // 2)
    self.control_surface.set_colorkey(self.background_color)

    self.controls = Controls(self.control_surface)

    self.sliders = {
      'pull': Slider(self.control_surface,
        pygame.Rect(300, 46, 100, 10), 10, 15, value=0.5),

      'smooth': Slider(self.control_surface,
        pygame.Rect(300, 66, 100, 10), 10, 15, value=0.5)
    }

    # smoothing history array
    self.t_history = numpy.full(self.num_bars, 0.5)
    self.f_history = numpy.full(self.num_bars, 0.0)

  def get_samples(self):
    format = '<{}h'.format(self.stream.sample_size)
    byte_string = self.stream.read(self.stream.sample_size)
    return list(map(util.normalize, struct.unpack(format, byte_string)))

  def draw_time_bars(self, samples, surface):
    width, height = surface.get_size()
    bar_width = width / self.num_bars

    s = self.sliders['smooth'].value
    for i in range(self.num_bars):
      power_i = samples[i]
      power_s = self.t_history[i]*s + power_i*(1-s)
      power = self.t_history[i] = power_s

      bar_height = power * height
      top = height - bar_height
      left = i * bar_width
      rect = (left, top, bar_width, 5) #bar_height)

      color = util.gradient(power, self.colorA, self.colorB)
      pygame.draw.rect(surface, color, rect)

  def draw_freq_bars(self, samples, surface):
    width, height = surface.get_size()
    y_max = self.stream.sample_size // 2
    bar_width = width / self.num_bars

    yf = numpy.log(numpy.abs(numpy.fft.fft(samples))+1)/numpy.log(y_max)

    s = self.sliders['smooth'].value

    pull = 1 - self.sliders['pull'].value
    g = (self.num_bars - 1) * (self.stream.sample_size//2 - 1) * pull
    v, h = util.shift_inverse_consts(
        0, 1, self.num_bars-1, self.stream.sample_size//2-1, g
    )

    for x in range(self.num_bars):
      y = util.shift_inverse(x, g, v, h)

      power_i = yf[int(y)]
      power_s = self.f_history[x]*s + power_i*(1-s)
      power = self.f_history[x] = power_s
      if power > 1.0:
        power = 1.0

      bar_height = power * height
      top = height - bar_height
      left = x * bar_width
      rect = (left, top, bar_width, bar_height)
      color = util.gradient(power, self.colorA, self.colorB)
      pygame.draw.rect(surface, color, rect)

  def resize_bars(self):
    self.num_bars = self.outputs.get_divisor()
    self.t_history.resize(self.num_bars)
    self.f_history.resize(self.num_bars)

  def resize(self):
    width = self.outputs.get_width()
    height = self.height
    self.time_surface = pygame.Surface((width, height // 2))
    self.freq_surface = pygame.Surface((width, height // 2))
    self.surface = pygame.display.set_mode(
      (width, height), self.surface_flags
    )
    self.resize_bars()

  def process_key(self, key):
    HEIGHT_DELTA = 100
    HEIGHT_MIN = 300

    SIZE_MIN = 1

    RATE_DELTA = 1000
    RATE_MIN = 0

    mods = pygame.key.get_mods()
    shift = mods & pygame.KMOD_SHIFT

    if key == ord('b'):
      if shift:
        self.outputs.next_divisor()
      else:
        self.outputs.prev_divisor()
      self.resize_bars()

    if key == ord('h'):
      if shift:
        self.height += HEIGHT_DELTA
      elif self.height > HEIGHT_MIN:
        self.height -= HEIGHT_DELTA
      self.resize()

    if key == ord('n'):
      k = 2 if shift else 0.5
      if self.stream.sample_size > SIZE_MIN:
        self.stream.sample_size *= k

    if key == ord('r'):
      k = 1 if shift else -1
      if self.stream.sample_rate > RATE_MIN:
        self.stream.sample_rate += k * RATE_DELTA

    if key == ord('w'):
      if shift:
        self.outputs.next_width()
      else:
        self.outputs.prev_width()
      self.resize()

  def process_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.exit()

      if event.type == pygame.KEYDOWN:
        self.process_key(event.key)

      if event.type == pygame.MOUSEMOTION:
        x = event.pos[0]

        R = self.stream.sample_rate
        N = self.stream.sample_size
        pull = 1 - self.sliders['pull'].value
        g = (self.num_bars - 1) * (N//2 - 1) * pull
        v, h = util.shift_inverse_consts(
            0, 1, self.num_bars-1, N//2-1, g
        )

        bar_width = self.outputs.get_width() / self.num_bars
        bar_index = math.floor(x / bar_width)
        self.mouse_frequency = util.shift_inverse(bar_index, g, v, h) * (R/2) / (N/2 - 1)

        for slider in self.sliders.values():
          if slider.moving:
            slider.set_value(x)

      if event.type == pygame.MOUSEBUTTONDOWN:
        for slider in self.sliders.values():
          if slider.get_handle_rect().collidepoint(event.pos):
            slider.moving = True

      if event.type == pygame.MOUSEBUTTONUP:
        for slider in self.sliders.values():
          slider.moving = False

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
               self.sliders['pull'].value,
               self.sliders['smooth'].value,
               self.outputs.get_width(),
               self.num_bars,
               self.mouse_frequency)

    for slider in self.sliders.values():
      slider.draw()

    self.draw_time_bars(samples, self.time_surface)
    self.draw_freq_bars(samples, self.freq_surface)

    self.surface.blit(self.time_surface, (0,0))
    self.surface.blit(self.freq_surface, (0,self.height // 2))
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
