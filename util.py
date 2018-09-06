import math
import time

# map value between a and b to ratio p
def iscale(a, b, x):
    return (x - a) / (b - a)

# map ratio p to value between a and b
def scale(a, b, p):
    return a + (b - a) * p

# map ib [0, nb) -> [0, ns/2)
def log_scale(rs, ib, nb, ns):
    return ((ns-2) * (rs/2)**((ib+2)/(nb+1)))/rs

def normalize(value):
    offset = 2.0 ** 15
    scale = (2.0 ** 16) - 1
    return (value + offset) / scale

def gradient(ratio, color1, color2):
    red = int(color1.r + ratio * (color2.r - color1.r))
    green = int(color1.g + ratio * (color2.g - color1.g))
    blue = int(color1.b + ratio * (color2.b - color1.b))
    return (red, green, blue)

def bias(b, x):
    return x ** (math.log(b)/math.log(0.5))

def gain(x, g):
    if x < 0.5:
        return bias(1-g, 2 * x) / 2
    return 1 - bias(1-g, 2 - 2 * x) / 2

def shift_parabola(x, x_max, y_max):
    return x**2 * (y_max - 1)/(x_max**2) + 1

def shift_ellipse(x, x_max, y_max):
    return -1 * math.sqrt(
                (1 - (x**2)/(x_max**2)) * y_max**2
            ) + y_max + 1

def shift_linear(x, x_min, y_min, x_max, y_max):
  return (x - x_max) * (y_max - y_min) / (x_max - x_min) + y_max

def shift_inverse_consts(x1, y1, x2, y2, g):
  a = -1*math.sqrt(y2-y1)*math.sqrt(4*g+x2*y2-x2*y1-x1*y2+x1*y2)
  b = (y1+y2)*math.sqrt(x2-x1)
  c = 2*math.sqrt(x2-x1)
  v = (a + b)/c
  h = (x2*y2-x1*y1+v*(x1-x2))/(y2-y1)
  return (v,h)

def shift_inverse(x, g, v, h):
  return -1 * g / (x - h) + v

def show_period(f):
    def wrapper(self):
        start = time.time()
        f(self)
        end = time.time()
        print(end - start)
    return wrapper


