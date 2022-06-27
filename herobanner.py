## HERO Splash
# "black"    #304059
# "white"    #ebe8da
# "blue"     #5dd8d6
# "yellow"   #ffdd5f
import pygame
from pygame import font

from settings import Settings
from dataclasses import dataclass


@dataclass
class HeroBanner:
    hero_x = 0
    hero_pos = 0
    hero_pos_text = 1150
    hero_height = 5
    glitch_size_x = 930
    glitch_size_y = 755
    showHero = True
    showIntro = False
    y_offset_indicator = 0
    heroColor: str
    heroTextColor: str
    color_gray: str
    text_surface = font
    subtext_surface = font

    black = "#304059"
    white = "#ebe8da"
    blue = "#5dd8d6"
    yellow = "#ffdd5f"
    pink = "#f0007d"
    pink_light = "#ff7196"

    def __init__(self):
        settings = Settings()
        #self.heroColor = settings.color_hero
        #self.heroTextColor = settings.color_pink
        self.heroColor = self.white
        self.heroTextColor = settings.color_pink
        self.color_gray = settings.color_gray
        self.text_surface = settings.font_hero.render(settings.str_hero_header,
                                                      True, self.pink)
        self.subtext_surface = settings.font.render(settings.str_hero_won, True,
                                                    self.white)

    def update(self, dt):
        if self.showHero:
            self.hero_x += dt
            if self.hero_x >= 930:
                self.hero_height += dt
                if self.hero_height > 125:
                    self.hero_height = 125

            if self.hero_height >= 125:
                self.hero_pos_text -= dt * 2

            if self.hero_pos_text < -550:
                self.showHero = not self.showHero
        else:
            self.hero_height -= dt
            if self.hero_height <= 5:
                self.hero_height = 5
                if self.hero_pos <= 930:
                    self.hero_pos += dt * 2

    def draw(self, surface):
        if self.showHero:
            pass
            #pygame.draw.rect(surface, self.black, (0, 525, 5 + self.hero_x,
            #                                           5 + self.hero_height))
            #pygame.draw.rect(surface, self.color_gray, (0, 525, -5 + self.hero_x, 10))
            #pygame.draw.rect(surface, self.heroTextColor, (self.hero_x, 525, 10, 10))

            if self.hero_height >= 125:
                rect_text = self.text_surface.get_rect(center=(450, 570))
                #surface.blit(self.text_surface, rect_text)
                rect_subtext = self.subtext_surface.get_rect(center=(450, 630))
                #surface.blit(self.subtext_surface, rect_subtext)

        else:
            pass
            #pygame.draw.rect(surface, self.heroColor,
            #                 (self.hero_pos, 525, 5 + self.hero_x, 5 + self.hero_height))
            #pygame.draw.rect(surface, self.color_gray, (self.hero_pos, 525, 10, 10))

    def is_intro_shown(self, surface):
        if self.showIntro:
            self.draw(surface)
