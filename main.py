import sys
import pygame

from helpers import (
    HEIGHT,
    SCALE,
    WIDTH,
    brick_height,
    brick_width,
    track1,
    track2,
    track3,
    track_path,
)
from models import Color
from pages import Info, MainMenu, Settings, ModeSelection
from pages import loading_screen


import pygame
import sys


class Game:
    def __init__(
        self,
        *,
        height=HEIGHT,
        width=WIDTH,
        scale=SCALE,
    ) -> None:

        self.height = height
        self.width = width
        self.scale = scale

        self.colors = Color()

        self.clock = pygame.time.Clock()
        self._music_files = track_path, track1, track2, track3
        self.music_is_playing = False
        self.is_main_menu = True
        self.volume = 0.0

        self.trails = {}

        self.main_menu = None
        self.settings_page = None
        self.info_page = None
        self.game_page = None

    def pre_load_music(self):
        for music_file in self._music_files[1:]:
            music_file.set_volume(self.volume)

    def initialize_pages(self):
        self.mode_selection = ModeSelection(
            self.screen, self.height, self.width, self.scale, self
        )
        self.main_menu = MainMenu(
            self.screen, self.height, self.width, self.scale, self
        )
        self.settings_page = Settings(
            self.screen, self.height, self.width, self.scale, self
        )
        self.info_page = Info(self.screen, self.height, self.width, self.scale, self)

    @property
    def music_files(self):
        return self._music_files[1:]

    def run_loading_screen(self):
        """Call the dynamic loading screen function."""
        return loading_screen(self.colors)

    def gameloop(self):
        self.pre_load_music()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.colors.BLACK)
        while True:
            if self.is_main_menu:
                if not self.main_menu:
                    self.initialize_pages()
                selected_option = self.main_menu.generate(
                    self.colors, brick_width, brick_height, self.clock
                )

            if self.music_is_playing:
                pygame.mixer.music.load(self._music_files[0])
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if selected_option == 0:
                self.is_main_menu = False
                back_to_main_menu = self.mode_selection.run(self.colors, self.clock, self.trails)
                if not back_to_main_menu:
                    self.is_main_menu = self.mode_selection.run(self.colors, self.clock, self.trails)
                else:
                    self.is_main_menu = True
            elif selected_option == 1:
                self.is_main_menu = False
                self.is_main_menu = self.settings_page.display()
            elif selected_option == 2:
                self.is_main_menu = False
                self.is_main_menu = self.info_page.scroll(self.colors)


if __name__ == "__main__":
    game = Game()
    game.gameloop()
