"""
    utility.py
    independent functions for use in waves.py
"""

import math

def normalize(value, width):
    offset = 2.0 ** (width - 1)
    scale = (2.0 ** width) - 1
    return (value + offset) / scale

def gradient(ratio, color1, color2):
    red = int(color1.r + ratio * (color2.r - color1.r))
    green = int(color1.g + ratio * (color2.g - color1.g))
    blue = int(color1.b + ratio * (color2.b - color1.b))
    return (red, green, blue)

def bias(b, x):
    return x ** (math.log(b)/math.log(0.5))

def gain(g, x):
    if x < 0.5:
        return bias(1-g, 2 * x) / 2
    return 1 - bias(1-g, 2 - 2 * x) / 2
