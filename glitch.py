import random

import pygame
from pygame import surface


class Glitch:
    def __init__(self, width, height, tex_skull):
        self.width = width
        self.height = height
        self.surface_org = pygame.Surface((width, height)).convert_alpha()
        self.surface = self.surface_org.copy()
        self.tex_skull = tex_skull
        self.tex_temp = surface

    def draw(self, surfaceOrg, enabled, flip):
        if enabled:
            self.surface = pygame.Surface((self.width, self.height)).convert_alpha()

            self.tex_temp = pygame.transform.flip(self.tex_skull, flip, False)
            for i in range(75):
                glitch_offset = random.randint(0, 30) - 15
                self.surface.blit(self.tex_temp, (0 + glitch_offset, i * 10),
                                  (0, i * 10, 930, 10), special_flags=pygame.BLEND_RGBA_MULT)

            surfaceOrg.blit(self.surface, (0, 0))
