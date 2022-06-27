import pygame


class ScreenTransitions:
    def __init__(self):
        self.radius = 10

    # color_hero_sub
    def draw(self, sur,settings):
        if settings.show_blend_screen:
            pygame.draw.circle(sur, settings.color_hero,
                               (settings.screen_width / 2, settings.screen_height / 2),
                               self.radius)

    def update(self, dt,settings,gamestate):
        if settings.show_blend_screen:
            if gamestate == 1:
                self.radius += dt * 3
            else:
                self.radius -= dt * 3
                if self.radius < 0:
                    settings.show_blend_screen = False