import pygame
import sys

from pages.pages import Page
from helpers import settings
from helpers.constants import font, brick_height, brick_width
from pages.dark_mode_game_page import DarkModeGame
from pages.loading_screen import loading_screen
from pages.main_game_page import MainGame  # Normal mode game page
# from pages.time_attack_game_page import TimeAttackGamePage


class ModeSelection(Page):
    def __init__(self, screen, height, width, scale, game):
        super().__init__(screen, height, width, scale, game)
        self.fonts = (pygame.font.SysFont(None, int(50 * self.scale)),)
        self.running = True
        self.selected_option = 0  # Track the currently selected option
        self.options = ["Normal Mode", "Dark Mode", "Time Attack Mode", "Quit"]

    def draw_text(self, text, color, y_offset, is_selected=False):
        """Draw a single menu option."""
        if is_selected:
            text = f"> {text} <"  # Add arrows to indicate selection
        label = self.fonts[0].render(text, True, color)
        self.screen.blit(
            label,
            ((self.width - label.get_width()) // 2, (self.height // 2) + y_offset),
        )

    def select_mode(self, color):
        """Display the mode selection menu and navigate using arrow keys."""
        running = True
        while running:
            self.screen.fill(color.BLACK)

            # Draw the options dynamically
            for i, option in enumerate(self.options):
                self.draw_text(
                    option, color.WHITE, i * 50 - 50, is_selected=(i == self.selected_option)
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        # Move selection down
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        # Move selection up
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:  # Confirm selection with ENTER
                        # Return the selected mode
                        return self.options[self.selected_option]
                    elif event.key == pygame.K_q:  # Allow immediate quit with Q
                        pygame.quit()
                        sys.exit()

    def run(self, color, clock, trails):
        """Run the mode selection and start the appropriate game mode."""
        selected_mode = self.select_mode(color)

        if selected_mode == "Normal Mode":
            loading_screen(color)
            game_page = MainGame(self.screen, self.height, self.width, self.scale, self.game, color)
            game_page.runner(brick_height, brick_width, trails, clock)
        elif selected_mode == "Dark Mode":
            loading_screen(color)
            game_page = DarkModeGame(
                self.screen, self.height, self.width, self.scale, self.game, color=settings.Color()
            )
        elif selected_mode == "Time Attack Mode":
            loading_screen(color)
            # Uncomment and implement TimeAttackGamePage if required
            # game_page = TimeAttackGamePage(
            #     self.screen, self.height, self.width, self.scale, self.game
            # )
        elif selected_mode == "Quit":
            pygame.quit()
            sys.exit()
        else:
            return True  # Return to the main menu if no valid selection