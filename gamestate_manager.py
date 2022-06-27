from pygame import font

from settings import Settings
from dataclasses import dataclass


@dataclass
class GamestateManager():
    gamestate = 0
    GS_MENU = 0
    GS_GAME = 1
    GS_TRANSITION = 2
    GS_WIN = 3
    GS_LOSE = 4
    # menu 0
    # game 1
    # transition 2
    # win 3 ->
    # lose 4

    gamestate_loaded = False

    def set_gamestate(self, state_num):
        self.gamestate = state_num
        self.gamestate_loaded = False

        # handle screen resets

    ## init lose/win screen
    #
    # how to handle the screens, their loading?
    #

    # why the fuck no new class called "game"
    def new_game(self, settings):
        settings.usedLetters = []
        settings.guesses = [[], [], [], [], [], []]
        settings.currentPosition = 0
        settings.guesses_count = 0

        self.gamestate = 1
        self.gamestate_loaded = False
