import math
from dataclasses import dataclass

import pygame
from pygame import surface


# fade in

@dataclass
class ScreenOver:
    y_pos_lock = 0
    step = 0
    pos_y = 0
    y = 0
    gamestate = 0
    screen_timer = 0
    change_to_next_screen = True

    TexLosescreen = surface
    TexLosescreen2 = surface
    TexLosescreen3 = surface
    TexLosescreenBG = surface
    TexLosescreenLight = surface

    TexWinscreenLight = surface
    TexWinscreenBG = surface
    TexWinscreen1 = surface
    TexWinscreen2 = surface
    TexWinscreen3 = surface

    tex_screen_1 = surface
    tex_screen_2 = surface
    tex_screen_3 = surface
    tex_screen_bg = surface
    tex_screen_light = surface

    ## AHHH time for better asset management
    def __init__(self, won=3):
        self.TexLosescreen = pygame.image.load('tex/lock/lose_screen.png').convert_alpha()
        self.TexLosescreen2 = pygame.image.load('tex/lock/lose_screen2.png').convert_alpha()
        self.TexLosescreen3 = pygame.image.load('tex/lock/lose_screen3.png').convert_alpha()
        self.TexLosescreenBG = pygame.image.load('tex/lose_screen_bg.png').convert_alpha()
        self.TexLosescreenLight = pygame.image.load('tex/lose_screen_light.png').convert_alpha()

        self.TexWinscreenLight = pygame.image.load('tex/win_screen_light.png').convert_alpha()
        self.TexWinscreenBG = pygame.image.load('tex/win_screen_bg.png').convert_alpha()
        self.TexWinscreen1 = pygame.image.load('tex/lock/win_screen_1.png').convert_alpha()
        self.TexWinscreen2 = pygame.image.load('tex/lock/win_screen_2.png').convert_alpha()
        self.TexWinscreen3 = pygame.image.load('tex/lock/win_screen_3.png').convert_alpha()

        if won == 3:
            self.gamestate = 3
            self.tex_screen_1 = self.TexWinscreen1
            self.tex_screen_2 = self.TexWinscreen2
            self.tex_screen_3 = self.TexWinscreen3
            self.tex_screen_bg = self.TexWinscreenBG
            self.tex_screen_light = self.TexWinscreenLight
        else:
            self.gamestate = 4
            self.tex_screen_1 = self.TexLosescreen
            self.tex_screen_2 = self.TexLosescreen2
            self.tex_screen_3 = self.TexLosescreen3
            self.tex_screen_bg = self.TexLosescreenBG
            self.tex_screen_light = self.TexLosescreenLight

    def update(self, dt):
        self.screen_timer += dt
        if self.screen_timer > 3000:
            self.y += dt * 2
        if self.screen_timer > 4000:
            self.change_to_next_screen = False

        if self.gamestate == 4:
            self.step -= 0.04
            sin = -1 * math.sin(self.step + (10 * .5)) * 15
        else:
            self.step -= 0.09
            sin = -1 * math.sin(self.step + (10 * .01)) * 15
        self.pos_y = 0 + sin

    def draw(self, surface, blink, flip):
        # happy overlay
        surface.blit(self.tex_screen_light, (0, self.y))

        # hero lose
        surface.blit(self.tex_screen_bg, (0, self.y*-1))

        if blink:
            surface.blit(self.tex_screen_3, (0, self.y + self.pos_y))
        else:
            if flip:
                surface.blit(self.tex_screen_1, (0, self.y + self.pos_y))
            else:
                surface.blit(self.tex_screen_2, (0, self.y + self.pos_y))
