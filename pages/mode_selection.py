import pygame
import sys
from pages.pages import Page
from helpers.constants import brick_height, brick_width
from pages.dark_mode_game_page import DarkModeGame
from pages.loading_screen import loading_screen
from pages.main_game_page import MainGame  
from pages.time_attack_page import TimeAttack


class ModeSelection(Page):
    def __init__(self, screen, height, width, scale, game):
        super().__init__(screen, height, width, scale, game)
        self.fonts = (pygame.font.SysFont(None, int(50 * self.scale)),)
        self.running = True
        self.selected_option = 0  
        self.options = ["Classic", "Dark Mode", "Time Attack",]


    def draw_text(self, text, color, y_offset, is_selected=False):
        """Draw a single menu option."""
        label = self.fonts[0].render(text, True, color.GREEN if is_selected else color.WHITE)
        self.screen.blit(
            label,
            ((self.width - label.get_width()) // 2, (self.height // 2) + y_offset),
        )


    def select_mode(self, color):
        """Display the mode selection menu and navigate using arrow keys."""
        running = True
        while running:
            self.screen.fill(color.BLACK)
            for i, option in enumerate(self.options):
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
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:           
                        return self.options[self.selected_option]
                    elif event.key == pygame.K_RSHIFT:
                        return True


    def run(self, color, clock, trails):
        """Run the mode selection and start the appropriate game mode."""
        selected_mode = self.select_mode(color)
        if selected_mode == self.options[0]:
            loading_screen(color)
            game_page = MainGame(self.screen, self.height, self.width, self.scale, self.game, color)
            game_page.runner(brick_height, brick_width, trails, clock)
        elif selected_mode == self.options[1]:
            loading_screen(color)
            game_page = DarkModeGame(self.screen, self.height, self.width, self.scale, self.game) 
            game_page.runner(brick_height, brick_width, trails, clock)
        elif selected_mode == self.options[2]:
            loading_screen(color)
            game_page = TimeAttack(self.screen, self.height, self.width, self.scale, self.game, color) 
            game_page.runner(brick_height, brick_width, trails, clock)            
        else:
            return True  