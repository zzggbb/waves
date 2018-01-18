#!/bin/env python3

import sys
import time
import struct
from multiprocessing import Process

import numpy
import pygame
import pyaudio

from stream import Stream
from controls import Controls
import utility

# audio parameters
SAMPLE_WIDTH = 16
SAMPLE_RATE = 20 * 10**3
SAMPLE_SIZE = 960
CHANNELS = 1

# visual parameters
SURFACE_SIZE = (SURFACE_WIDTH, SURFACE_HEIGHT) = (1920, 1080)
BACKGROUND_COLOR = pygame.Color('white')
color1 = pygame.Color('red')
color2 = pygame.Color('black')
SMOOTHING = 0.6
GAIN = 0.5

SURFACE = pygame.display.set_mode(SURFACE_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)
CLOCK = pygame.time.Clock()
LAST_POWER = numpy.full(SAMPLE_SIZE, 0.5)

stream = Stream(CHANNELS, SAMPLE_RATE, SAMPLE_SIZE)
controls = Controls(SURFACE)

def draw_bars(bytes, sample_rate, sample_size, smoothing, gain):
    # little endian, signed SAMPLE_WIDTH bit ints
    format = '<{}h'.format(sample_size)
    samples = struct.unpack(format, bytes)

    for i in range(sample_size):
        power_instant = utility.normalize(samples[i], SAMPLE_WIDTH)
        LAST_POWER[i] = LAST_POWER[i] * smoothing + power_instant * (1 - smoothing)

        power = utility.gain(gain, LAST_POWER[i])

        # determine column position
        width = SURFACE_WIDTH / sample_size
        height = power * SURFACE_HEIGHT
        top = SURFACE_HEIGHT - height
        left = i * width
        rect = (left, top, width, height)

        color = utility.gradient(power, color1, color2)
        pygame.draw.rect(SURFACE, color, rect)

def processEvents():
    global GAIN
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                stream.sample_size //= 2
                numpy.resize(LAST_POWER, stream.sample_size)

            if event.key == pygame.K_l:
                stream.sample_size *= 2
                numpy.resize(LAST_POWER, stream.sample_size)

            if event.key == pygame.K_j:
                stream.sample_rate -= 2500

            if event.key == pygame.K_k:
                stream.sample_rate += 2500

            if event.key == pygame.K_w:
                GAIN += 0.01

            if event.key == pygame.K_s:
                GAIN -= 0.01

if __name__ == '__main__':
    pygame.init()
    stream.open()

    while True:
        try:
            processEvents()
            SURFACE.fill(BACKGROUND_COLOR)
            controls.draw(stream.sample_rate, stream.sample_size, SMOOTHING, GAIN)
            bytes = stream.read(stream.sample_size)
            draw_bars(bytes, stream.sample_rate, stream.sample_size, SMOOTHING, GAIN)
            pygame.display.flip()

        except KeyboardInterrupt:
            stream.close()
            pygame.quit()
