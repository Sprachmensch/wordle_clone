import pygame
from easing_functions import easing
from pygame import font, surface
from itertools import repeat
from dataclasses import dataclass


# @todo split settings into classes import -> settings for lock, game, background... ?


@dataclass
class Settings:
    screen_width = 930
    screen_height = 750
    color_green = "#b9e226"
    color_gray = "#304059"
    color_pink = "#fafafa"
    color_hero = "#f0007d"
    color_hero_sub = "#ebe8da"
    color_yellow = "#ffdd5f"
    alphabet_sorted = "ABCDEFGHIJKLMNOPQRSTVUWXYZ"
    alphabet = ["QWERTZUIOP", "ASDFGHJKL", "YXCVBNM"]  # ger keyboard layout
    usedLetters = []
    guesses = [[], [], [], [], [], []]
    goal_word = ["H", "O", "T", "E", "L"]
    indicator = {}
    currentPosition = 0
    guesses_count = 0
    checkedGuess = False

    win_timer = 0
    won = False

    gamefield_pos_x = 930

    # easing
    easingFunction = easing.CubicEaseOut()
    easing_start_pos = -450
    easing_end_pos = 500

    easing_frame = 0
    indication_easing_start_pos = 0
    indication_easing_end_pos = -450  # diff is end pos?
    indication_easing_amount=0
    indication_y_bounce=0


    game_is_running = True
    clock = pygame.time.Clock()
    showScanlines = False
    scanlinesFlash = False
    scanlineTimer = 0
    scanlineEffectTimer = 0

    offsetShake = repeat((0, 0))
    font_hero: font
    font: font
    font_wave: font
    font_small: font
    font_lose: font

    str_hero_header = "ランダムな単語"
    str_hero_won = "YOU WON"
    str_hero_lose = "YOU LOSE"
    str_title = "Kawaii WORDLE clone"
    str_title_waving = "PRESS ANY KEY TO START"

    def __init__(self):
        self.font_hero = pygame.font.Font("font/MochiyPopOne_jpa.ttf", 72)
        self.font = pygame.font.Font("font/Lato-Black.ttf", 40)
        self.font_lose = pygame.font.Font("font/Lato-Black.ttf", 56)
        self.font_wave = pygame.font.Font("font/Lato-Black.ttf", 40)
        self.font_small = pygame.font.Font("font/Lato-Black.ttf", 25)

    ### HERE BE DRAGONS
    glitch_enabled = False  # performance okay on raspi?
    show_blend_screen = False
    flip = False
    flip_counter = 30
    lose_rect = (540, 552, 160, 42)
    lose_surface = surface
    blink = False
    blink_counter = 0
    degrees = .1
    rotate_left = False
    glitch_flip = True
    hero_replacement_showIntro = False
    hero_replacement_y_offset_indicator = 0

    def init_over_screen(self):
        self.str_hero_lose = ""
        for letter in self.goal_word:
            self.str_hero_lose += letter + "  "

        self.lose_surface = self.font_lose.render(self.str_hero_lose, True, "#5dd8d6")

    def flip_update(self, dt):
        if self.rotate_left:
            self.degrees -= .1
        else:
            self.degrees += .1
        if self.degrees > 5 or self.degrees < -5:
            self.rotate_left = not self.rotate_left

        self.flip_counter -= dt / 4
        if self.flip_counter < 0:
            self.flip_counter = 30
            self.flip = not self.flip

            if self.blink:
                self.blink = False

            self.blink_counter += 1
            if self.blink_counter > 5:
                self.blink = not self.blink
                self.blink_counter = 0
