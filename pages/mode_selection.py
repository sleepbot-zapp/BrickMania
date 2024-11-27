import pygame
import sys
from helpers import AutoEnum
from functools import wraps
from pages.pages import Page
from helpers.constants import brick_height, brick_width
from pages.dark_mode_game_page import DarkModeGame
from pages.loading_screen import loading_screen
from pages.main_game_page import MainGame
from pages.time_attack_page import TimeAttack


class GameMode(AutoEnum):
    """Enum to represent game modes."""

    CLASSIC: int
    DARK_MODE: int
    TIME_ATTACK: int


def handle_mode(mode):
    """Decorator to handle logic for a specific game mode."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.selected_mode == mode:
                return func(self, *args, **kwargs)
            return None

        return wrapper

    return decorator


class ModeSelection(Page):
    def __init__(self, screen, height, width, scale, game):
        super().__init__(screen, height, width, scale, game)
        self.fonts = (pygame.font.SysFont(None, int(50 * self.scale)),)
        self.running = True
        self.selected_option = 0
        self.options = {
            GameMode.CLASSIC: "Classic",
            GameMode.DARK_MODE: "Dark Mode",
            GameMode.TIME_ATTACK: "Time Attack",
        }
        self.selected_mode = None  

    def draw_text(self, text, color, y_offset, is_selected=False):
        """Draw a single menu option."""
        label = self.fonts[0].render(
            text, True, color.GREEN if is_selected else color.WHITE
        )
        self.screen.blit(
            label,
            ((self.width - label.get_width()) // 2, (self.height // 2) + y_offset),
        )

    def select_mode(self, color):
        """Handle menu navigation and mode selection."""
        running = True
        mode_keys = list(self.options.keys())  
        while running:
            self.screen.fill(color.BLACK)
            for i, (mode, option) in enumerate(self.options.items()):
                self.draw_text(
                    option, color, i * 50 - 50, is_selected=(i == self.selected_option)
                )
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(
                            self.options
                        )
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(
                            self.options
                        )
                    elif event.key == pygame.K_RETURN:
                        self.selected_mode = mode_keys[self.selected_option]
                        return self.selected_mode
                    elif event.key == pygame.K_RSHIFT:
                        return None

    @handle_mode(GameMode.CLASSIC)
    def run_classic_mode(self, color, clock, trails):
        """Run the Classic game mode."""
        loading_screen(color)
        game_page = MainGame(
            self.screen, self.height, self.width, self.scale, self.game, color
        )
        game_page.runner(brick_height, brick_width, trails, clock)

    @handle_mode(GameMode.DARK_MODE)
    def run_dark_mode(self, color, clock, trails):
        """Run the Dark Mode game mode."""
        loading_screen(color)
        game_page = DarkModeGame(
            self.screen, self.height, self.width, self.scale, self.game
        )
        game_page.runner(brick_height, brick_width, trails, clock)

    @handle_mode(GameMode.TIME_ATTACK)
    def run_time_attack_mode(self, color, clock, trails):
        """Run the Time Attack game mode."""
        loading_screen(color)
        game_page = TimeAttack(
            self.screen, self.height, self.width, self.scale, self.game, color
        )
        game_page.runner(brick_height, brick_width, trails, clock)

    def run(self, color, clock, trails):
        """Run the mode selection and handle transitions."""
        selected_mode = self.select_mode(color)
        if selected_mode:
            self.run_classic_mode(color, clock, trails)
            self.run_dark_mode(color, clock, trails)
            self.run_time_attack_mode(color, clock, trails)
        else:
            return True
