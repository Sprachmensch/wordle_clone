import random

import pygame


def create_confetti():
    colors = {"#f0007d", "#fbb03b", "#5dd8d6", "#b9e226", "#962bb5"}
    particles_confetti = []

    for i in range(200):
        x = (random.randint(1, 70) * 10) + 100
        y = (random.randint(1, 40) * 10) * -1
        color = random.choice(list(colors))
        grav = random.randint(3, 7) / 10

        movement_x = bool(random.getrandbits(1))
        particles_confetti.append(Confetti(x, y, movement_x,
                                           color=color, gravity=grav))

    return particles_confetti


class Confetti():
    def __init__(self, x, y, dx=False, dy=False, gravity=.5,
                 color=(255, 66, 66)):
        self.x = x
        self.y = y
        self.time_to_live = 30
        self.size = 20
        self.gravity = gravity
        self.speed = .4
        self.color = color
        self.dx = dx
        self.dy = dy
        self.isActive = True

    def update(self, dt):
        self.y += dt * self.gravity
        self.time_to_live -= dt / 3

        if self.y > 950:
            self.isActive = False

        if self.time_to_live < 0:
            self.time_to_live = random.randint(10, 50) * 10
            self.dx = bool(random.getrandbits(1))
            x = random.randint(1, 20) / 100
            self.speed = x

        if self.dx:
            self.x += dt * self.speed
        else:
            self.x -= dt * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, "#304059",
                         (self.x - 5, self.y + 3,
                          self.size / 2, self.size))
        pygame.draw.rect(surface, self.color,
                         (self.x, self.y,
                          self.size / 2, self.size))
