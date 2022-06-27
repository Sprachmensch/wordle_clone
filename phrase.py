import math
from dataclasses import dataclass

import pygame


@dataclass
class Phrase:
    phrase_str = ""
    x_pos = 150
    y_pos = 555
    step = 1

    text_rect = pygame.Rect(1, 1, 1, 1)
    text_surface = pygame.Surface((10, 10))
    text_x = 0
    text_y = 0

    def __init__(self, phrase):
        self.phrase_str = phrase

    def draw(self, surface, startscreen_y, settings):
        for i in range(len(self.phrase_str)):
            self.step -= 0.004
            sin = -1 * math.sin(self.step + (i * .5)) * 20
            self.y_pos = 555 + sin
            self.text_x = self.x_pos + (i * 30)
            self.text_y = startscreen_y + self.y_pos
            self.draw_text(settings, self.text_x, self.text_y, "#304059",
                           surface, self.phrase_str[i])
            self.draw_text(settings, self.text_x - 3, self.text_y - 5, "#ebe8da",
                           surface, self.phrase_str[i])

    def draw_text(self, settings, x, y, color, surface, letter):
        self.text_rect = (x, y, 60, 60)
        self.text_surface = settings.font_wave.render(letter,
                                                      True, color)
        surface.blit(self.text_surface, self.text_rect)
