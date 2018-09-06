import pygame

import util

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
