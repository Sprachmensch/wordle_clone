from dataclasses import dataclass

from pygame import surface


@dataclass
class Background:
    scroll_x = 0.0
    tex = surface

    def __init__(self, surface):
        self.tex = surface

    def update(self, dt):
        self.scroll_x -= dt / 18

        if self.scroll_x < 0:
            self.scroll_x = 930

    def draw(self, surface):
        surface.blit(self.tex, (self.scroll_x, 0))
        surface.blit(self.tex, (self.scroll_x - 930, 0))
