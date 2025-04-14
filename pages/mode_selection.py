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
    CLASSIC: int
    DARK_MODE: int
    TIME_ATTACK: int


def handle_mode(mode):
    """Decorator to run a method only if the selected mode matches."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.selected_mode == mode:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator


class ModeSelection(Page):
    def __init__(self, screen, height, width, scale, game):
        super().__init__(screen, height, width, scale, game)
        self.font = pygame.font.SysFont(None, int(50 * scale))
        self.selected_option = 0
        self.selected_mode = None
        self.options = {
            GameMode.CLASSIC: "Classic",
            GameMode.DARK_MODE: "Dark Mode",
            GameMode.TIME_ATTACK: "Time Attack",
        }

    def draw_option(self, text, color, y_offset, selected=False):
        rendered = self.font.render(text, True, color.GREEN if selected else color.WHITE)
        x = (self.width - rendered.get_width()) // 2
        y = (self.height // 2) + y_offset
        self.screen.blit(rendered, (x, y))

    def select_mode(self, color):
        mode_keys = list(self.options.keys())
        while True:
            self.screen.fill(color.BLACK)
            for i, (_, label) in enumerate(self.options.items()):
                self.draw_option(label, color, i * 50 - 50, selected=(i == self.selected_option))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.selected_mode = mode_keys[self.selected_option]
                        return self.selected_mode
                    elif event.key == pygame.K_RSHIFT:
                        return None

    @handle_mode(GameMode.CLASSIC)
    def run_classic_mode(self, color, clock, trails):
        loading_screen(color)
        MainGame(self.screen, self.height, self.width, self.scale, self.game, color).runner(
            brick_height, brick_width, trails, clock
        )

    @handle_mode(GameMode.DARK_MODE)
    def run_dark_mode(self, color, clock, trails):
        loading_screen(color)
        DarkModeGame(self.screen, self.height, self.width, self.scale, self.game).runner(
            brick_height, brick_width, trails, clock
        )

    @handle_mode(GameMode.TIME_ATTACK)
    def run_time_attack_mode(self, color, clock, trails):
        loading_screen(color)
        TimeAttack(self.screen, self.height, self.width, self.scale, self.game, color).runner(
            brick_height, brick_width, trails, clock
        )

    def run(self, color, clock, trails):
        """Launch selected mode after choosing from menu."""
        if self.select_mode(color):
            self.run_classic_mode(color, clock, trails)
            self.run_dark_mode(color, clock, trails)
            self.run_time_attack_mode(color, clock, trails)
        else:
            return True
