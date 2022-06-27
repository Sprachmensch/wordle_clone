import random

import pygame
from easing_functions import easing
from dataclasses import dataclass


@dataclass
class Particle:
    x = 0
    y = 0
    size = 7
    livetime = 1.2
    frame = 0
    movement_x = True
    movement_y = True
    speed = 20
    colorHex = "#3c43ad"
    livetime_decrease = 50
    size_decrease = 20
    has_movement = False
    color = (100, 100, 100)
    particleEasingndPost = 700
    easing_start_pos = -250
    isActive = True

    def __init__(self, x, y, size, livetime, color, livetime_decrease, size_decrease,
                 movement_x=False, movement_y=False, has_movement=True, speed=20):
        self.x = x
        self.y = y
        self.size = size
        self.livetime = livetime
        self.color = color
        self.livetime_decrease = livetime_decrease
        self.size_decrease = size_decrease
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.speed = speed
        self.has_movement = has_movement
        self.easingFunction = easing.CubicEaseOut()
        self.easingAmount = self.easingFunction(self.frame * 0.01)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)

    #
    # refactor me into one function!
    #
    def generate_smoke_list_white(x, y, range_count, color="#304059"):
        temp = []
        for j in range(0, range_count):
            x_offset = random.randint(-30, 30)
            temp.append(Particle(x - x_offset + j, y + j,
                                 size=20, livetime=20,
                                 has_movement=False,
                                 color=color, livetime_decrease=500,
                                 size_decrease=20))
        return temp

    def generate_smoke_list(x, y, range_count, color="#304059"):
        temp = []
        for smoke in range(0, range_count):
            x_offset = random.randint(1, 120)
            y_offset = random.randint(1, 120)
            temp.append(Particle(x - x_offset / 2, y - y_offset / 2,
                                 size=random.randint(15, 35), livetime=40,
                                 has_movement=False,
                                 color=color, livetime_decrease=600,
                                 size_decrease=10))
        return temp

    def update(self, dt):
        self.livetime -= dt / self.livetime_decrease
        self.size -= dt / self.size_decrease
        # self.easingAmount = self.easingFunction(self.frame * 0.01)
        # self.easingAmount = min(1, self.easingAmount)
        # self.y = (self.particleEasingndPost - self.easing_start_pos) * self.easingAmount
        # self.frame += 1

        if self.has_movement:
            self.speed -= dt / self.speed
            if self.movement_x:
                self.x += dt / self.speed
            else:
                self.x -= dt / self.speed

            if self.movement_y:
                self.y += dt / self.speed
            else:
                self.y -= dt / self.speed

        if self.size <= 0 or self.livetime <= 0:
            self.isActive = False
