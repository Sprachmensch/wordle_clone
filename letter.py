import math


class Letter:
    def __init__(self, key, position, tile):
        self.tile = tile
        self.text_color = "black"
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.key = key
        self.fontcolor = "#304059"
        self.flash_timer = 0
        self.flash = 2
        self.locked = False
        self.s = 3
        self.y_text = self.y

    def draw(self, surface, settings, TexTileFlash1):
        text_surface = settings.font.render(self.key, True, self.fontcolor)
        # surface.blit(TexWordTileGrey2, (self.x + 1, self.y + 1))
        surface.blit(self.tile, (self.x, self.y))
        if self.flash == 1:
            surface.blit(TexTileFlash1, (self.x, self.y))
        textRect = text_surface.get_rect(center=(self.x + 31, self.y_text + 30))
        surface.blit(text_surface, textRect)

    def update(self, dt, easing_frame):
        self.flash_timer += dt
        if self.flash_timer > 250:
            self.flash_timer = 0
            self.flash += 1
        if not self.locked:
            self.s = math.sin(easing_frame / 8) / 8  # slow pulsing
            self.y_text += self.s
