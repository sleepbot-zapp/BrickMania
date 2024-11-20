import typing
import pygame
from pages.pages import Page
import sys


class Settings(Page):
    def __init__(
        self, 
        screen, 
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
        
        self.settings_options = settings_options or (
            "Sound: ON", 
            "Difficulty: NORMAL", 
            "Reset Progress",
            "Back to Main Menu"
        )
        self.selected_option: int = 0
    
    def display(self, color) -> None:
        self.screen.fill(color.BLACK)
        header_font = self.fonts[0]
        header_text = header_font.render("Settings", True, color.WHITE)
        header_rect = header_text.get_rect(center=(self.width // 2, int(50 * self.scale)))
        self.screen.blit(header_text, header_rect)
        
        options_font = self.fonts[1]
        for i, option in enumerate(self.settings_options):
            c = color.BLUE if i != self.selected_option else color.YELLOW
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
                    return self.selected_option
                elif e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
    
    def navigate(self, direction: int) -> None:
        self.selected_option = (self.selected_option + direction) % len(self.settings_options)
    
    def select_option(self) -> str:
        return self.settings_options[self.selected_option]
