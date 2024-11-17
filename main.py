from os import chdir
from os.path import dirname
from pygame import init, display
# from pygame.mixer import music
from helpers.runner import runner
from pages.main_menu import main_menu
from pages.loading_screen import loading_screen
from pages.main_game import main_game


chdir(dirname(__file__))

init()

display.set_caption("BrickMania")

if __name__ == "__main__":
    # music.load("./assets/music.mp3")
    # is_paused=True
    type_ = 1
    runner(main_menu, loading_screen, main_game, type_)
