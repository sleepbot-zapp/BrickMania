import typing
import pygame
from pages.pages import Page
from models import Color
import sys


class Settings(Page):
    def __init__(
        self, 
        screen, 
        game,
        height: typing.Union[int, float], 
        width: typing.Union[int, float],
        scale: typing.Union[int, float],
        fonts: typing.Tuple[pygame.font.SysFont] = None, 
        settings_options: typing.Tuple[str] = None
    ) -> None:
        super().__init__(screen, height, width, scale, fonts)
        
        self.fonts = fonts or (
            pygame.font.SysFont(None, int(72 * self.scale)),  # Header
            pygame.font.SysFont(None, int(32 * self.scale)),  # Options
        )
        self.selected_option: int = 0
        self.game = game
        self.settings_options = settings_options or (
            ["Unmute Music", "Mute Music"], 
            "Back to Main Menu"
        )
    
    def display(self, color) -> typing.Tuple[bool, bool]:
        self.selected_option = 0
        while True:
            self.screen.fill(color.BLACK)
            header_font = self.fonts[0]
            header_text = header_font.render("Settings", True, color.WHITE)
            header_rect = header_text.get_rect(center=(self.width // 2, int(50 * self.scale)))
            self.screen.blit(header_text, header_rect)
            
            options_font = self.fonts[1]
            for i, option in enumerate(self.settings_options):
                c = color.BLUE if i != self.selected_option else color.YELLOW
                if i == 0:
                    option_text = options_font.render(option[self.game.music_is_playing], True, c)
                else:
                    option_text = options_font.render(option, True, c)
                option_rect = option_text.get_rect(center=(self.width // 2, int(150 * self.scale) + i * 50))
                self.screen.blit(option_text, option_rect)
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.settings_options)
                    elif e.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.settings_options)
                    elif e.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            self.game.music_is_playing = not self.game.music_is_playing
                            return False
                        if self.selected_option == 1:
                            return True
                    elif e.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
        