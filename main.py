import sys
import pygame
from functools import wraps
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
    AutoEnum,
)
from models import Color, FallingTile
from pages import Info, MainMenu, Settings, ModeSelection
from pages.main_game_page import MainGame
from pages import loading_screen
import pages.loading_screen as loading_screen


class GameState(AutoEnum):
    """Enum to manage game states."""
    MAIN_MENU: int
    MODE_SELECTION: int
    INGAME: int
    SETTINGS: int
    INFO: int
    EXIT: int


def handle_event(state):
    """Decorator to handle state-specific events."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.current_state == state:
                return func(self, *args, **kwargs)
            return None
        return wrapper
    return decorator


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
        self.volume = 0.0
        self.trails = {}

        self.event = None
        self.current_state = GameState.MAIN_MENU
        self.main_menu = None
        self.settings_page = None
        self.info_page = None
        self.mode_selection = None
        self.delay_ms = 20
        self.current_input_time_ms = 0

    def pre_load_music(self):
        """Pre-load music with set volume."""
        for music_file in self.music_files:
            music_file.set_volume(self.volume)

    def initialize_pages(self):
        """Initialize the pages."""
        self.main_menu = MainMenu(
            self.screen, self.height, self.width, self.scale, self
        )
        self.settings_page = Settings(
            self.screen, self.height, self.width, self.scale, self
        )
        self.info_page = Info(self.screen, self.height, self.width, self.scale, self)
        self.mode_selection = ModeSelection(
            self.screen, self.height, self.width, self.scale, self
        )

    @property
    def music_files(self):
        return self._music_files[1:]

    def run_loading_screen(self):
        """Call the dynamic loading screen function."""
        return loading_screen(self.colors)

    @handle_event(GameState.MAIN_MENU)
    def handle_main_menu(self):
        """Handle logic for the main menu."""
        if not self.main_menu:
            self.initialize_pages()
        
        selected_option = self.main_menu.generate(
            self.colors, brick_width, brick_height, self.tiles
        )

        keys = pygame.key.get_pressed()

        # Just a hack, fix later :p
        if self.event != None:
            if keys[pygame.K_DOWN]:
                self.main_menu.selected_option = (self.main_menu.selected_option + 1) % len(
                    self.main_menu.options
                )
            elif keys[pygame.K_UP]:
                self.main_menu.selected_option = (self.main_menu.selected_option - 1) % len(
                    self.main_menu.options
                )
            elif keys[pygame.K_RETURN]:
                selected_option = self.main_menu.selected_option
            self.event = None

        if selected_option == 0:
            self.current_state = GameState.MODE_SELECTION
        elif selected_option == 1:
            self.current_state = GameState.SETTINGS
        elif selected_option == 2:
            self.current_state = GameState.INFO
        elif selected_option == 3:
            self.current_state = GameState.EXIT

    @handle_event(GameState.MODE_SELECTION)
    def handle_mode_selection(self):
        """Handle logic for the mode selection page."""

        mode_keys = list(self.mode_selection.options.values())
        self.mode_selection.select_mode(self.colors)
        keys = pygame.key.get_pressed()

        if self.event != None:
            if keys[pygame.K_DOWN]:
                self.mode_selection.selected_option = (self.mode_selection.selected_option + 1) % len(
                    self.mode_selection.options
                )
            elif keys[pygame.K_UP]:
                self.mode_selection.selected_option = (self.mode_selection.selected_option - 1) % len(
                    self.mode_selection.options
                )
            elif keys[pygame.K_RETURN]:
                self.mode_selection.selected_mode = mode_keys[self.mode_selection.selected_option]
                self.current_state = GameState.INGAME
                self.once = True
            elif keys[pygame.K_ESCAPE]:
                self.current_state = GameState.MAIN_MENU

            self.event = None

    @handle_event(GameState.INGAME)
    def handle_ingame(self):
        if self.mode_selection.selected_mode == 'Classic':
            if self.once == True:
                self.run_loading_screen()
                self.game_page = MainGame(
                    self.screen, self.height, self.width, self.scale, self.mode_selection.game, self.colors
                )
                self.game_page.init_game()
                self.once = False
            else:
                self.mode_selection.run_classic_mode(self.colors, self.clock, self.trails, self.game_page)
        # Do this for the rest
        elif self.mode_selection.selected_mode == 'Time Attack':
            self.mode_selection.run_time_attack_mode(self.colors, self.clock, self.trails)
        elif self.mode_selection.selected_mode == 'Dark Mode':
            self.mode_selection.run_dark_mode(self.colors, self.clock, self.trails)
        pass

    @handle_event(GameState.SETTINGS)
    def handle_settings(self):
        """Handle logic for the settings page."""
        back_to_main_menu = self.settings_page.display()
        if back_to_main_menu:
            self.current_state = GameState.MAIN_MENU

    @handle_event(GameState.INFO)
    def handle_info(self):
        """Handle logic for the info page."""
        back_to_main_menu = self.info_page.scroll(self.colors)
        if back_to_main_menu:
            self.current_state = GameState.MAIN_MENU

    def gameloop(self):
        """Main game loop."""
        self.pre_load_music()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.colors.BLACK)

        self.tiles = [
            FallingTile(
                brick_width, brick_height, self.width, self.height, self.scale, self.colors
            )
            for _ in range(20)
        ]

        self.current_state = GameState.MAIN_MENU
        while self.current_state != GameState.EXIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_state = GameState.EXIT
                elif event.type == pygame.KEYDOWN:
                    self.event = event

            if self.current_state == GameState.MAIN_MENU:
                self.handle_main_menu()
            elif self.current_state == GameState.MODE_SELECTION:
                self.handle_mode_selection()
            elif self.current_state == GameState.INGAME:
                self.handle_ingame()
            self.handle_settings()
            self.handle_info()

            
            if self.music_is_playing:
                pygame.mixer.music.load(self._music_files[0])
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

            pygame.display.update()
            self.current_input_time_ms = pygame.time.get_ticks()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.gameloop()
