import math
from dataclasses import dataclass

from pygame import surface


# fade in

@dataclass
class ScreenMenu:
    y_pos_lock = 0
    startscreen_y = -755
    startscreen_y_lock = 0
    step = 1
    state_loaded = False

    tex_startscreen = surface
    tex_startscreen_lock = surface

    def __init__(self, tex_screen, tex_lock):
        self.tex_startscreen = tex_screen
        self.tex_startscreen_lock = tex_lock

    def update(self, dt, gamestate_num):
        if not self.state_loaded:
            self.startscreen_y += dt
            self.startscreen_y_lock = self.startscreen_y

            if self.startscreen_y >= 0:
                self.startscreen_y = 0
                self.startscreen_y_lock = 0
                self.state_loaded = True
        else:
            if gamestate_num == 0:
                self.step -= 0.04
                sin = -1 * math.sin(self.step + (10 * .5)) * 15
                self.y_pos_lock = 0 + sin

            if gamestate_num == 2:
                self.startscreen_y_lock -= dt
                self.startscreen_y += dt * 2

    def draw(self, surface):
        surface.blit(self.tex_startscreen, (0, self.startscreen_y))
        surface.blit(self.tex_startscreen_lock, (0, self.startscreen_y_lock + self.y_pos_lock))
