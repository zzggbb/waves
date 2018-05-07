import pygame

import util

FONT_SIZE = 18
FONT_PATH = './resources/terminus.ttf'
FONT_COLOR = (255,255,255)
FONT_ANTIALIAS = True
CARD_WIDTH = 200

class Slider(object):
    def __init__(self, surface, rail_rect, handle_width, handle_height, value=0.5):
        self.surface = surface
        self.rail_rect = rail_rect
        self.handle_width = handle_width
        self.handle_height = handle_height
        self.value = value
        self.moving = False

    def set_value(self, x):
        x_max = self.rail_rect.x + self.rail_rect.width - self.handle_width
        x_min = self.rail_rect.x
        if not (x_min < x < x_max):
            return
        self.value = util.iscale(x_min, x_max, x)

    def get_handle_rect(self):
        handle_x = util.scale(self.rail_rect.x,
                              self.rail_rect.x + self.rail_rect.width - self.handle_width,
                              self.value)
        handle_y = self.rail_rect.y + (self.rail_rect.height - self.handle_height) // 2
        return pygame.Rect(handle_x, handle_y, self.handle_width, self.handle_height)

    def draw(self):
        rail_color = pygame.Color("#232323")
        handle_color = pygame.Color("#FFFFFF")
        pygame.draw.rect(self.surface, rail_color, self.rail_rect)
        pygame.draw.rect(self.surface, handle_color, self.get_handle_rect())

class Controls(object):

    def __init__(self, surface):
        pygame.font.init()
        self.surface = surface
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def draw(self, sample_rate, sample_size, gain, smooth, width, bars):
        params = {
            'sample rate': str(sample_rate),
            'sample size': str(sample_size),
            'gain ratio (0-1)': '{0:.2f}'.format(gain),
            'smoothing ratio (0-1)': '{0:.2f}'.format(smooth),
            'window width': str(width),
            'bar count': str(bars),
            'bar width': str(width // bars)
        }
        max_label_width = 0
        for label in params.keys():
            width, _ = self.font.size(label)
            if width > max_label_width:
                max_label_width = width

        i = 0
        for label, value in params.items():
            item_text = label + '  ' + value
            item_width, item_height = self.font.size(item_text)
            label_width, _ = self.font.size(label)
            item_surface = self.font.render(item_text, FONT_ANTIALIAS, FONT_COLOR)
            pos = (max_label_width - label_width, i)
            self.surface.blit(item_surface, pos)
            i = i + item_height
