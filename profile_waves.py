#!/bin/env python3

import random

import wavx

SAMPLE_WIDTH = 16
SAMPLE_SIZE = 240
N = 20

for i in range(N):
    # generate random samples
    samples = b''
    for i in range(SAMPLE_SIZE):
        bound = 2 ** (SAMPLE_WIDTH - 1)
        sample = random.randrange(-bound, bound)
        sample = sample.to_bytes(2, byteorder='little', signed=True)
        samples += (sample)

    wavx.process(samples)
