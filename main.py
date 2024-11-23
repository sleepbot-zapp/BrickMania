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
from pages import Info, MainGame, MainMenu, Settings
from pages import loading_screen


class Game:
    def __init__(
        self,
        *,
        height=HEIGHT,
        width=WIDTH,
        scale=SCALE,
    ) -> None:
        pygame.init()
        # window
        self.height = height
        self.width = width
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width, self.height))
        # colors
        self.colors = Color()
        # game variables
        self.clock = pygame.time.Clock()
        self._music_files = track_path, track1, track2, track3
        self.music_is_playing = False
        self.is_main_menu = True
        self.volume = 0.0
        # entity variables
        self.trails = {}
        # pages
        self.main_menu = MainMenu(self.screen, self.height, self.width, self.scale)
        self.settings_page = Settings(
            self.screen,
            self,
            self.height,
            self.width,
            self.scale,
        )
        self.info_page = Info(
            self.screen, self, self.height, self.width, self.scale, self.colors
        )
        self.game_page = MainGame(
            self.screen, self.height, self.width, self.scale, self
        )

    @property
    def music_files(self):
        music_files = []
        for music_file in self._music_files[1:]:
            music_files.append(music_file)
            music_file.set_volume(self.volume)
        return music_files

    def run_loading_screen(self):
        """Call the dynamic loading screen function."""
        result = (
            loading_screen()
        )  # The loading screen runs until user presses Enter or Shift
        return result  # Return value determines the next action (e.g., continue or go back)

    def gameloop(self):
        while True:
            if self.music_is_playing:
                pygame.mixer.music.load(self._music_files[0])
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

            self.screen.fill(self.colors.BLACK)

            # Handle main menu and get selected option
            if self.is_main_menu:
                selected_option = self.main_menu.generate(
                    self.colors, brick_width, brick_height, self.clock
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Process selected option
            if selected_option == 0:  # Start the game
                self.is_main_menu = False
                back_to_main_menu = (
                    self.run_loading_screen()
                )  # Show the animated loading screen
                if not back_to_main_menu:  # User pressed Enter to continue
                    self.is_main_menu = self.game_page.runner(
                        self.colors,
                        brick_height,
                        brick_width,
                        self.trails,
                        self.clock,
                    )
                else:  # User pressed Shift to return to the main menu
                    self.is_main_menu = True
            elif selected_option == 1:  # Settings
                self.is_main_menu = False
                self.is_main_menu = self.settings_page.display(self.colors)
            elif selected_option == 2:  # Info
                self.is_main_menu = False
                self.is_main_menu = self.info_page.scroll(self.colors)


if __name__ == "__main__":
    game = Game()
    game.gameloop()
