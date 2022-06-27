import math
import pygame
from easing_functions import easing
from dataclasses import dataclass

from pygame import surface


@dataclass
class Lock:
    x = 105
    y = -430
    eyes_offset = -470
    eyes = 220
    eye_pos_y = -200
    eyes_flash_timer = 4
    eyes_timer = 300
    eyes_state_1 = True
    eyes_blink_timer = 1
    flash = False
    TexLock = surface
    TexLockBlend = surface
    TexLockBar = surface
    TexEyes = surface
    TexEyes2 = surface
    TexEyesBlink = surface
    TexEyesCurrent = surface
    call_count = 0
    shineTimer = 0
    shineTime = False

    TexLockShine_x = 0
    TexLockShine_y = 0

    easingFunction = easing.CubicEaseOut()
    easing_start_pos = -450
    easing_end_pos = 500
    easing_frame = 0
    easing_pos_y = 0

    bar_popup = False
    bar_popup_up = False
    bar_popup_offset = 0

    def __init__(self):
        self.TexLock = pygame.image.load('tex/lock/lock.png').convert_alpha()
        self.TexLockBlend = pygame.image.load('tex/lock/lock_blend.png').convert_alpha()
        self.TexLockBar = pygame.image.load('tex/lock/lock_bar.png').convert_alpha()
        self.TexEyes = pygame.image.load('tex/lock/eyes.png').convert_alpha()
        self.TexEyes2 = pygame.image.load('tex/lock/eyes_2.png').convert_alpha()
        self.TexEyesBlink = pygame.image.load('tex/lock/eye_blink.png').convert_alpha()
        self.TexEyesCurrent = pygame.image.load('tex/lock/eye_blink.png').convert_alpha()

    def draw(self, surface, bar_popup_offset):
        surface.blit(self.TexLockBar, (self.x, self.y + bar_popup_offset))
        surface.blit(self.TexLock, (self.x, self.y))
        surface.blit(self.TexEyesCurrent, (190, self.eye_pos_y))

        # get the logic out of here :)
        # split blend into two part bar&lock
        # use currentLockBar
        # use currentLock

        if self.flash:
            surface.blit(self.TexLockBlend, (self.x, self.y))

    def update(self, dt):
        self.update_easing(dt)
        self.update_positions()
        self.update_eyes(dt)
        self.update_eye_blinking(dt)
        self.update_bar_popup(dt)
        self.update_shine_timer(dt)
        self.update_flash(dt)
        self.update_eyes_textures()

    def update_easing(self, dt):
        self.easing_amount = self.easingFunction(self.easing_frame * 0.01)
        self.easing_amount = min(1, self.easing_amount)

        self.easing_pos_y = (self.easing_end_pos - self.easing_start_pos) * self.easing_amount
        self.easing_frame += 1

    def update_lock_shine_pos(self, current_pos, guesses_count):
        self.TexLockShine_x = 467 + current_pos
        self.TexLockShine_y = 48 + guesses_count

    def update_eyes(self, dt):
        self.eyes += dt * .125
        self.eyes_offset = math.cos(self.eyes / 20) * 10
        self.eyes_offset -= 150

    def update_positions(self):
        self.y = -870 + self.easing_pos_y + (math.cos(self.eyes / 20) * 5)
        self.eye_pos_y = self.easing_pos_y + -450 + self.eyes_offset + (math.cos(self.eyes / 20) * 5)

    def update_eye_blinking(self, dt):
        if self.eyes_state_1:
            self.eyes_flash_timer += dt / 40
        else:
            self.eyes_flash_timer += dt / 5

        if self.eyes_flash_timer > 30:
            self.eyes_flash_timer = 0
            self.eyes_state_1 = not self.eyes_state_1

        if self.eyes_blink_timer > 0:
            self.eyes_blink_timer -= dt / 5

    def update_bar_popup(self, dt):
        if self.bar_popup:
            self.bar_popup_offset += dt / 8
            if self.bar_popup_offset > 50:
                self.bar_popup_offset = 50
                self.bar_popup_up = True
                self.bar_popup = False

        if self.bar_popup_up:
            self.bar_popup_offset -= dt / 2
            if self.bar_popup_offset <= -75:
                self.bar_popup_offset = -75

    def update_shine_timer(self, dt):
        if self.shineTimer > 540:
            self.shineTime = not self.shineTime
            self.shineTimer = 0
        self.shineTimer += dt

    def update_flash(self, dt):
        if self.flash:
            self.eyes_flash_timer -= dt / 2
            if self.eyes_flash_timer < 0:
                self.flash = False

    def update_eyes_textures(self):
        if self.eyes_blink_timer < 0:
            if self.eyes_state_1:
                self.TexEyesCurrent = self.TexEyes
            else:
                self.TexEyesCurrent = self.TexEyes2
        else:
            self.TexEyesCurrent = self.TexEyesBlink
