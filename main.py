from os import chdir
from os.path import dirname
import pygame
import random
import sys
import time
import helpers.settings as settings
from models import SpecialBall, Color
from helpers.drawings import draw_player, draw_bricks, draw_ball
from helpers.game_control import pause_game, show_score, game_over, drop_powerup, create_new_bricks
from helpers.runner import runner
from helpers.main_menu import main_menu
from helpers.loading_screen import loading_screen
from helpers.constants import *
from helpers.main_game import main_game


chdir(dirname(__file__))

pygame.init()


if __name__ == "__main__":
    pygame.mixer.music.load("./assets/music.mp3")
    is_paused=True
    runner(main_menu, loading_screen, main_game, is_paused, 1)
