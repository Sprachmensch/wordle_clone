import pygame


class Scanline:
    def __init__(self, width, height):
        self.size = width, height
        self.surface = pygame.Surface(self.size).convert_alpha()
        self.surface.fill((48, 64, 89, 0))
        for j in range(0, self.size[1], 2):
            self.surface.fill((0, 0, 0, 25), (0, j, self.size[0], 1))  # or slightly transparent if desired.
