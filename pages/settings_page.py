import typing

import pygame

from .pages import Page


class Settings(Page):
    def __init__(
        self,
        screen,
        game,
        height: typing.Union[int, float],
        width: typing.Union[int, float],
        scale: typing.Union[int, float],
        fonts=None,
        settings_options: typing.Tuple[str] = None,
    ) -> None:
        super().__init__(screen, height, width, scale, fonts)

        self.fonts = fonts or (
            pygame.font.SysFont(None, int(72 * self.scale)),
            pygame.font.SysFont(None, int(32 * self.scale)),
        )
        self.selected_option: int = 0
        self.game = game
        self.expanded_option = -1
        self.settings_options = settings_options or ["Music"]

    def display(self, color) -> bool:
        bar_width = int(300 * self.scale)
        bar_height = int(20 * self.scale)
        bar_x = self.width // 2
        bar_y = self.height // 2

        while True:
            self.screen.fill(color.BLACK)
            header_font = self.fonts[0]
            header_text = header_font.render("Settings", True, color.WHITE)
            header_rect = header_text.get_rect(
                center=(self.width // 2, int(50 * self.scale))
            )
            self.screen.blit(header_text, header_rect)

            options_font = self.fonts[1]
            for i, option in enumerate(self.settings_options):
                c = color.YELLOW if i == self.selected_option else color.WHITE
                option_text = options_font.render(option, True, c)
                option_rect = option_text.get_rect(
                    center=(self.width // 2, int(150 * self.scale) + i * 50)
                )
                self.screen.blit(option_text, option_rect)

                if i == self.expanded_option and option == "Music":
                    bar_y = option_rect.bottom + 20

                    volume_label_text = options_font.render(
                        "Volume:", True, color.WHITE
                    )
                    volume_label_rect = volume_label_text.get_rect(
                        center=(bar_x - bar_width // 2 - 60, bar_y + bar_height // 2)
                    )
                    self.screen.blit(volume_label_text, volume_label_rect)

                    pygame.draw.rect(
                        self.screen,
                        color.GREY,
                        (bar_x - bar_width // 2, bar_y, bar_width, bar_height),
                    )

                    filled_width = int(bar_width * self.game.volume)
                    pygame.draw.rect(
                        self.screen,
                        color.GREEN,
                        (bar_x - bar_width // 2, bar_y, filled_width, bar_height),
                    )

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RSHIFT:
                        if self.expanded_option == -1:
                            return True
                        else:
                            self.expanded_option = -1
                    elif e.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(
                            self.settings_options
                        )
                    elif e.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(
                            self.settings_options
                        )
                    elif e.key == pygame.K_RETURN:
                        if self.selected_option == 0 and self.expanded_option == -1:
                            self.expanded_option = 0
                        else:
                            self.expanded_option = -1

                    elif self.expanded_option == 0:
                        if e.key == pygame.K_RIGHT:
                            self.game.volume = min(self.game.volume + 0.1, 1.0)
                            pygame.mixer.music.set_volume(self.game.volume)
                            if not self.game.music_is_playing and self.game.volume > 0:
                                self.game.music_is_playing = True
                                pygame.mixer.music.play(-1)
                        elif e.key == pygame.K_LEFT:
                            self.game.volume = max(self.game.volume - 0.1, 0.0)
                            pygame.mixer.music.set_volume(self.game.volume)
                            if self.game.volume == 0 and self.game.music_is_playing:
                                self.game.music_is_playing = False
                                pygame.mixer.music.stop()

            pygame.display.flip()