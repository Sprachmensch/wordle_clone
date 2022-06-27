#
#
# Font Lato https://fonts.google.com/specimen/Lato
# https://opengameart.org/content/4-chiptunes-adventure
#
# scanlines less mem
## https://www.reddit.com/r/pygame/comments/6yk6zk/least_memory_intensive_way_to_implement_scanlines/
# Not used:
# Audio Voices by MadamVicious (https://freesound.org/people/MadamVicious/sounds/238641)
#
# @todo turn this into "kawaii clock" game for github?
# @todo refactor 'em all ...
# @todo spritesheet
# @todo create the wordle game -> no words, winning/losing
# @todo scope of the game -> intro/menu/options/languages?
#
#
#   OMG refactor me
#   Particles List-> got better :)
#   ✔   Lock -> Class
#   Typing sounds?
#   easingFunc
#   naming conventions
#   moving in update, for exp. "scrollX"
#   ✔   handleInput
#   ✔   fix assets colors -> indicator
#   ✔   Window Icon
#   ✔   Delete/Replace Letters
#   init methode
#   ✔   gameOver -> Transition back to the startscreen
#   check "glitch" performance on raspi
#   intro with "fake" loading screen or fade in effect for the main menu
#   compare diff screens to find design errors - like missing shadows
#   create a short docu
#       - show the "drawn" hierarchy
#   clean up the assets and upload them
#   escape key back to menu and on the second press exit the game
#   turn debug on/off -> log printing
#   create /utils/ folder for texture atlas and effect editor
#   juicify the effects/animations -> intro? "special effects" on the first start?
#
#
#   'BUGS'
#   ✔   word to short -> index out of bounds
#   ✔   Lock on the title screen is not bouncing after winning
#   ✔   overlapping background
#   multiple letters are displayed wrong -> "lllll" four orange and one green -> correct -> one green
#
#
#   Unclear:
#   Easings -why "wrong" values
#
#
#
#
import itertools
import random

import pygame
from easing_functions import easing

from background import Background
from gamestate_manager import GamestateManager
from letter import Letter
from lock import Lock
from part_confetti import create_confetti
from particle import Particle
from phrase import Phrase
from screen_game import ScreenGame
from screen_menu import ScreenMenu
from screen_over import ScreenOver
from screen_transition import ScreenTransitions
from settings import Settings
from sky import Sky
from scanline import Scanline
from glitch import Glitch
from dataclasses import dataclass


@dataclass
class WordleGame:
    # init
    # Setup Pygame / Display
    pygame.init()
    manager = GamestateManager()
    settings = Settings()
    pygame.display.set_caption(settings.str_title)

    particles_new = []
    particles_confetti = []

    # surfaceOrg = pygame.display.set_mode((927, 750), pygame.HWSURFACE)
    surfaceOrg = pygame.display.set_mode((settings.screen_width, settings.screen_height), pygame.HWSURFACE)
    lock = Lock()
    pygame_icon = pygame.image.load('tex/icon.png')
    pygame.display.set_icon(pygame_icon)

    # surfaceOrg = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    surfaceOrg.fill(color=(255, 66, 112))
    surface = surfaceOrg.copy()
    surface.fill(color=(255, 66, 112))

    TexBg = pygame.image.load('tex/tiles/bg_fields.png').convert_alpha()
    TexBgSky = pygame.image.load('tex/bg_sky.png').convert_alpha()
    TexBgScroll = pygame.image.load('tex/bg2.png').convert_alpha()
    TexLock2 = pygame.image.load('tex/lock/lock2.png').convert_alpha()
    TexLockShine = pygame.image.load('tex/tiles/lock_shine.png').convert_alpha()
    TexLockShine2 = pygame.image.load('tex/tiles/lock_shine_2.png').convert_alpha()
    TexScanline = pygame.image.load('tex/scanline.png').convert_alpha()
    TexScanline2 = pygame.image.load('tex/scanline2.png').convert_alpha()
    TexScanlineOverlaySkull = pygame.image.load('tex/scanline_overlay_skull.png').convert_alpha()
    TexStartscreen = pygame.image.load('tex/startscreen.png').convert_alpha()
    TexStartscreenLock = pygame.image.load('tex/lock/startscreen_lock.png').convert_alpha()

    TexWordTileYellow = pygame.image.load('tex/tiles/tile_yellow.png').convert_alpha()
    TexWordTileGreen = pygame.image.load('tex/tiles/tile_green.png').convert_alpha()
    TexWordTileGrey = pygame.image.load('tex/tiles/tile_grey.png').convert_alpha()
    TexWordTileGrey2 = pygame.image.load('tex/tiles/tile_grey2.png').convert_alpha()
    TexWordTileDefault = pygame.image.load('tex/tiles/tile_default.png').convert_alpha()

    TexTileIndicatorGreen = pygame.image.load('tex/tiles/indicator_green.png').convert_alpha()
    TexTileIndicatorGrey = pygame.image.load('tex/tiles/indicator_grey.png').convert_alpha()
    TexTileIndicatorYellow = pygame.image.load('tex/tiles/indicator_yellow.png').convert_alpha()
    TexTileIndicatorDefault = pygame.image.load('tex/tiles/indicator_default.png').convert_alpha()

    TexTileFlash1 = pygame.image.load('tex/tiles/tile_flash_1.png').convert_alpha()

    background = Background(TexBgScroll)
    skies = Sky(TexBgSky)
    phrase = Phrase(settings.str_title_waving)
    screen_menu = ScreenMenu(TexStartscreen, TexStartscreenLock)
    # screen_game = ScreenGame()
    screen_over = ScreenOver()
    screen_transition = ScreenTransitions()
    dt=0

    # SOUNDS
    sound_enabled = False
    if sound_enabled:
        snd_hit_1 = pygame.mixer.Sound('../snd/1.mp3')
        snd_hit_2 = pygame.mixer.Sound('../snd/2.mp3')
        snd_hit_3 = pygame.mixer.Sound('../snd/3.mp3')
        snd_hit_4 = pygame.mixer.Sound('../snd/4.mp3')
        snd_hit_5 = pygame.mixer.Sound('../snd/5.mp3')
        hit_sounds = [snd_hit_1, snd_hit_2, snd_hit_3, snd_hit_4, snd_hit_5]

    def gen_smoke(self, x, y):
        self.particles_new.extend(Particle.generate_smoke_list_white(
            x, y, 60, color="#fafafa"))

    def show_hit_screen(self):
        self.settings.offsetShake = self.shake()

        self.settings.showScanlines = not self.settings.showScanlines
        self.settings.scanlineTimer = 10
        self.settings.scanlineEffectTimer = 450
        self.settings.glitch_enabled = True

    def shoot_confetti(self):
        self.particles_confetti.extend(create_confetti())

    def show_lose_screen(self):
        print("show lose")
        self.settings.init_over_screen()
        self.screen_over = ScreenOver(4)
        self.manager.set_gamestate(4)

    def show_win_screen(self):
        self.settings.hero_replacement_showIntro = True
        self.lock.bar_popup = True
        self.settings.won = True
        self.settings.win_timer = 1900

        # confetti
        # shoot_confetti()

        # self.settings.show_blend_screen = True
        if self.lock.bar_popup:
            self.lock.eyes_flash_timer = 150

    #
    # Seperate the gameLogic into its own class
    #
    def checkGuess(self, current_guess):
        print(f"guesses_count: {self.settings.guesses_count}")
        print(f"currentPosition: {self.settings.currentPosition}")
        tmpLen = len(self.settings.guesses)
        print(f"tmpLen: {tmpLen}")
        self.settings.checkedGuess = True
        GOAL = self.settings.goal_word  # useless variable :)

        if self.sound_enabled:
            self.snd_hit_2.play()
        check_won = True
        for i in range(5):
            # lock the letter
            current_guess[i].locked = True

            # gen smoke
            self.gen_smoke(current_guess[i].x, current_guess[i].y)

            lower = current_guess[i].key
            if current_guess[i].key in GOAL:
                if lower == GOAL[i]:
                    current_guess[i].flash = i * -1
                    current_guess[i].flash_timer = 0
                    current_guess[i].tile = self.TexWordTileGreen
                    self.settings.indicator[lower] = self.TexTileIndicatorGreen
                else:
                    current_guess[i].tile = self.TexWordTileYellow
                    self.settings.indicator[lower] = self.TexTileIndicatorYellow
                    check_won = False
            else:
                current_guess[i].fontcolor = "#ebe8da"
                current_guess[i].tile = self.TexWordTileGrey
                self.settings.indicator[lower] = self.TexTileIndicatorGrey
                check_won = False

        if check_won:
            self.show_win_screen()
        else:
            if self.settings.guesses_count >= 3:
                self.show_lose_screen()
            self.show_hit_screen()

        self.settings.glitch_flip = not self.settings.glitch_flip
        self.settings.currentPosition = 0
        self.settings.guesses_count += 1

    # LINE += 1

    # https://stackoverflow.com/questions/23633339/pygame-shaking-window-when-loosing-lifes
    # slightly modified
    #
    def shake(self, hori=False, times=5, power=10):
        s = -1
        for _ in range(0, times):
            for x in range(power, 0, 2):
                if hori:
                    yield x * s, x * s
                else:
                    yield 0, x * s
            for x in range(0, power, 2):
                if hori:
                    yield x * s, x * s
                else:
                    yield 0, x * s
            s *= -1
        while True:
            yield 0, 0

    def change_indicators(self, guess):
        self.settings.usedLetters.append(guess)

    def init_indicators(self, settings):
        for i in range(3):
            for let in settings.alphabet[i]:
                settings.indicator.update({let: self.TexTileIndicatorDefault})

    scanline = Scanline(settings.screen_width, settings.screen_height)
    glitch = Glitch(settings.screen_width, settings.screen_height, TexScanlineOverlaySkull)

    def add_new_letter(self, key_pressed):
        x = 465 + (self.settings.currentPosition * 67)
        y = 47 + (self.settings.guesses_count * 79)
        letter = Letter(key_pressed, (x, y), self.TexWordTileDefault)
        self.settings.guesses[self.settings.guesses_count].append(letter)
        self.settings.currentPosition += 1

    def add_new_letter_effects(self):
        self.settings.offsetShake = self.shake()
        self.lock.eyes_blink_timer = 60
        self.lock.flash = True
        self.lock.eyes_flash_timer = 20

        x = 455 + (self.settings.currentPosition * 67)
        y = 100 + (self.settings.guesses_count * 80)
        self.particles_new.extend(Particle.generate_smoke_list(
            x, y, 80,
        ))

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.manager.gamestate == 1:
                    if self.sound_enabled:
                        # snd_typing.play()
                        pass
                    key_pressed = event.unicode.upper()
                    if key_pressed in self.settings.alphabet_sorted:
                        if len(self.settings.guesses[self.settings.guesses_count]) <= 4:
                            self.add_new_letter(key_pressed)
                            self.add_new_letter_effects()

                    elif event.key == pygame.K_BACKSPACE:
                        print("Please dont crash")
                        if len(self.settings.guesses[self.settings.guesses_count]) >= 1:
                            print(len(self.settings.guesses[self.settings.guesses_count]))
                            self.settings.guesses[self.settings.guesses_count].pop()
                            self.settings.currentPosition -= 1
                    elif event.key == pygame.K_RETURN:
                        self.settings.offsetShake = self.shake(power=8, times=5)
                        if len(self.settings.guesses[self.settings.guesses_count]) == 5:
                            print("over 5!")
                        if len(self.settings.guesses[self.settings.guesses_count]) == 5:
                            self.checkGuess(self.settings.guesses[self.settings.guesses_count])
                    elif event.key == pygame.K_ESCAPE:
                        # running = False
                        self.manager.set_gamestate(0)
                        self.screen_menu = ScreenMenu(self.TexStartscreen, self.TexStartscreenLock)
                else:
                    if event.key == pygame.K_SPACE:
                        print("Space")
                        # shoot_confetti()

                        self.manager.set_gamestate(2)
                        screen_game = ScreenGame()
                        # if sound_enabled:
                        #    pygame.mixer.music.load('music/stage.mp3')
                        #    pygame.mixer.music.play(-1, 0.0)

                    elif event.key == pygame.K_ESCAPE:
                        self.settings.game_is_running = False
                        # gamestate_mgr.gamestate = 0

            if event.type == pygame.QUIT:
                self.settings.game_is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"Mouse   x: {x}  y:{y}")

    def draw_letters(self):
        for guess in self.settings.guesses:
            for letter in guess:
                letter.update(self.dt, self.settings.easing_frame)
                letter.draw(self.surface, self.settings, self.TexTileFlash1)

    def draw_indicators(self):  # own class !
        y_offset = 0
        if self.settings.hero_replacement_showIntro:
            self.settings.hero_replacement_y_offset_indicator += self.dt * 2
            y_offset = self.settings.hero_replacement_y_offset_indicator

        offset = 0

        self.settings.indication_easing_amount = self.settings.easingFunction(self.settings.easing_frame * 0.01)
        self.settings.indication_easing_amount = min(1, self.settings.indication_easing_amount)
        self.settings.indication_y_bounce = (
                                                    self.settings.indication_easing_end_pos - self.settings.indication_easing_start_pos) * self.settings.indication_easing_amount

        for i in range(3):
            spacer = 0

            y_offset += 5
            if i == 1:
                offset = 23
            elif i == 2:
                offset = 73
            for letter in self.settings.alphabet[i]:
                x = 222 + offset + (spacer * 49)
                y = 1000 + y_offset + (i * 50)  # + 545
                spacer += 1
                tempRect = (x, y + self.settings.indication_y_bounce, 42, 42)

                if not self.settings.indicator[letter] == self.TexTileIndicatorDefault:
                    text_surface = self.settings.font_small.render(letter, True, "#ebe8da")
                else:
                    text_surface = self.settings.font_small.render(letter, True, "#304059")
                textRect = text_surface.get_rect(center=(x + 21, self.settings.indication_y_bounce + y + 18))

                self.surface.blit(self.settings.indicator[letter], tempRect)
                self.surface.blit(text_surface, textRect)

    def update_particles(self, dt):
        for part in itertools.chain(self.particles_new, self.particles_confetti):
            if part.isActive:
                part.update(dt)

        self.remove_particles()

    # how to refactor me? itertools chain?
    def remove_particles(self):
        for part in self.particles_new:
            if not part.isActive:
                self.particles_new.remove(part)

        for part in self.particles_confetti:
            if not part.isActive:
                self.particles_confetti.remove(part)

    # move me into screen_game
    def update_scanlines(self, dt):
        if self.settings.showScanlines:
            self.settings.scanlineTimer -= dt / 2
            self.settings.scanlineEffectTimer -= dt / 2
            if self.settings.scanlineEffectTimer < 0:
                self.settings.showScanlines = False
                self.settings.glitch_enabled = False
            if self.settings.scanlineTimer < 0:
                self.settings.scanlinesFlash = not self.settings.scanlinesFlash
                self.settings.scanlineTimer = 10

    def update_movement(self, dt):

        self.background.update(dt)
        self.skies.update(dt)
        self.update_particles(dt)
        self.update_scanlines(dt)
        self.screen_transition.update(dt, self.settings, self.manager.gamestate)
        self.screen_menu.update(dt, self.manager.gamestate)

        if self.settings.won:  # rename me -> wait for screen_to_end ?
            self.settings.win_timer -= dt
            self.settings.show_blend_screen = True
            if self.screen_transition.radius > 1050:
                self.settings.won = False
                # reset 'em all
                self.lock = Lock()
                self.phrase.x_pos = 150
                self.screen_menu = ScreenMenu(self.TexStartscreen, self.TexStartscreenLock)
                self.manager.set_gamestate(3)
                self.screen_over = ScreenOver(3)
                self.particles_confetti.extend(create_confetti())

        if self.settings.currentPosition <= 4:
            self.lock.update_lock_shine_pos(self.settings.currentPosition * 67,
                                            self.settings.guesses_count * 80)

    def draw_background(self):
        self.background.draw(self.surface)
        self.skies.draw(self.surface)
        self.surface.blit(self.scanline.surface, (0, 0))

    def draw_gamefield(self):
        self.surface.blit(self.TexBg, (self.settings.gamefield_pos_x, 0))

    def draw_particles(self):
        for part in itertools.chain(self.particles_new, self.particles_confetti):
            if part.isActive:
                part.draw(self.surface)

    def draw_scanlines(self):
        if self.settings.showScanlines:
            if self.settings.scanlinesFlash:
                self.surface.blit(self.TexScanline, (0, 0))
            else:
                self.surface.blit(self.TexScanline2, (0, 0))

    def update_easing_game_screen(self):
        # mixture of lock & gamefield easing :(
        easing_amount = self.settings.easingFunction(self.settings.easing_frame * 0.01)
        easing_amount = min(1, easing_amount)
        self.settings.easing_frame += 1

        # end - start pos
        gamefield_easing_x = (930 - 0) * easing_amount
        self.settings.gamefield_pos_x = 930 - gamefield_easing_x

    def show_highlight_current_field(self):
        if self.settings.currentPosition <= 4:
            if self.lock.shineTime and self.settings.gamefield_pos_x == 0:
                self.surface.blit(self.TexLockShine, (self.lock.TexLockShine_x, self.lock.TexLockShine_y))

    def load_sounds(self):
        if self.sound_enabled:
            snd_hit_1 = pygame.mixer.Sound('sounds/hit_1.mp3')
            snd_hit_2 = pygame.mixer.Sound('sounds/hit_2.mp3')
            snd_typing = pygame.mixer.Sound('sounds/typing.mp3')

            pygame.mixer.music.load('music/menu.mp3')
            pygame.mixer.music.play(-1, 0.0)

    def draw_screen_game(self):
        self.draw_gamefield()
        # confetti behind the hero banner
        for con in self.particles_confetti:
            con.draw(self.surface)
        self.lock.draw(self.surface, self.lock.bar_popup_offset)

        self.draw_indicators()  # optimize me
        self.draw_letters()

    def draw_screen_win_lose(self, dt):
        self.screen_over.update(dt)
        self.settings.flip_update(dt)
        self.screen_over.draw(self.surface, self.settings.blink, self.settings.flip)
        if self.manager.gamestate == 4:
            # don't like the way the offsetting is handled
            self.surface.blit(self.settings.lose_surface, (540, 554 + (self.screen_over.y * -1)))

        for con in self.particles_confetti:
            con.draw(self.surface)

    def create_new_game(self):
        self.init_indicators(self.settings)

        self.manager.new_game(self.settings)

    # refactor me!
    def reset_game(self):
        # called when ever menu is loaded, resets all objects

        self.manager.set_gamestate(0)

        self.lock = Lock()
        self.settings.hero_replacement_showIntro = False
        self.settings.hero_replacement_y_offset_indicator = 0
        self.settings.gamefield_pos_x = 930  # gamefield reset to spawn outside of the viewport
        self.settings.easing_frame = 0

        self.screen_menu = ScreenMenu(self.TexStartscreen, self.TexStartscreenLock)

    def start_game(self):
        self.init_indicators(self.settings)

        print("starting game")
        while self.settings.game_is_running:
            dt = self.settings.clock.tick(60)
            # print(clock.get_fps())

            # START UPDATE
            self.update_movement(dt)

            if self.manager.gamestate == 1:
                self.update_easing_game_screen()
                self.lock.update(dt)

            elif self.manager.gamestate == 2:
                if self.screen_menu.startscreen_y_lock < -1000:
                    self.create_new_game()

            # START DRAWING
            self.draw_background()

            if self.manager.gamestate == 1:
                self.draw_screen_game()
                self.show_highlight_current_field()
            elif self.manager.gamestate == 3 or self.manager.gamestate == 4:
                self.draw_screen_win_lose(dt)

                if not self.screen_over.change_to_next_screen:
                    self.reset_game()

            else:
                # if gamestate is menu or transition
                self.screen_menu.draw(self.surface)
                self.phrase.draw(self.surface, self.screen_menu.startscreen_y, self.settings)

            self.draw_particles()
            self.draw_scanlines()

            self.surfaceOrg.blit(self.surface, next(self.settings.offsetShake))

            self.glitch.draw(self.surfaceOrg, self.settings.glitch_enabled, self.settings.glitch_flip)

            self.screen_transition.draw(self.surfaceOrg, self.settings)

            pygame.display.update()
            self.handle_input(pygame.event.get())

        pygame.quit()
        print("DONE")


# easy todo
# the colors - correct names -> put them in inkscape on the color scheme


# next try
# global are killing it
if __name__ == '__main__':
    wordle = WordleGame()
    wordle.start_game()
