import pygame

import util

FONT_SIZE = 18
FONT_PATH = './resources/terminus.ttf'
FONT_COLOR = (255,255,255)
FONT_ANTIALIAS = True
CARD_WIDTH = 200

class Controls(object):

    def __init__(self, surface):
        pygame.font.init()
        self.surface = surface
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def draw(self, sample_rate, sample_size, pull, smooth, width, bars, mouse_frequency):
        params = {
            'sample rate': str(sample_rate),
            'sample size': str(sample_size),
            'pull ratio (0-1)': '{0:.2f}'.format(pull),
            'smoothing ratio (0-1)': '{0:.2f}'.format(smooth),
            'window width': str(width),
            'bar count': str(bars),
            'bar width': str(width // bars),
            'mouse frequency': str(int(mouse_frequency))
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
