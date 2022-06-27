from dataclasses import dataclass

from pygame import surface


@dataclass
class Sky:
    sky_scrollX = 0
    tex = surface

    def __init__(self, surface):
        self.tex = surface

    def update(self, dt):
        self.sky_scrollX -= dt / 12
        if self.sky_scrollX < -930:
            self.sky_scrollX = 0

    def draw(self, surface):
        surface.blit(self.tex, (self.sky_scrollX, 0))
        surface.blit(self.tex, (self.sky_scrollX + 930, 0))
