import sys
import typing

import pygame

from models import Color, FallingTile

from .pages import Page


class MainMenu(Page):
    def __init__(
        self,
        screen,
        height: typing.Union[int, float],
        width: typing.Union[int, float],
        scale: typing.Union[int, float],
        game,
        fonts=None,
        options: typing.Tuple[str] = None,
    ) -> None:
        super().__init__(screen, height, width, scale, game)
        self.fonts = fonts or (
            pygame.font.SysFont(None, int(72 * self.scale)),
            pygame.font.SysFont(None, int(25 * self.scale)),
            pygame.font.SysFont(None, int(48 * self.scale)),
        )
        self.selected_option: int = 0
        self.options = options or ("Play", "Settings", "Info")
        self.texts = ("BRICKMANIA", "Press Q to Quit", "Press Enter to Select")

    def generate(
        self,
        color: Color,
        brick_width: typing.Union[int, float],
        brick_height: typing.Union[int, float],
        clock,
    ) -> int:
        tiles = [
            FallingTile(
                brick_width, brick_height, self.width, self.height, self.scale, color
            )
            for _ in range(20)
        ]
        while True:
            self.screen.fill(color.BLACK)
            for tile in tiles:
                tile.move(self.height, self.width)
                tile.draw(self.screen)

            title_text = self.fonts[0].render(self.texts[0], True, color.YELLOW)
            self.screen.blit(
                title_text,
                (
                    (self.width // 2 - title_text.get_width() // 2) * self.scale,
                    (self.height // 2 - 150) * self.scale,
                ),
            )

            quit_text = self.fonts[1].render(self.texts[1], True, color.GREY)
            bottom_text = self.fonts[1].render(self.texts[2], True, color.GREY)
            self.screen.blit(
                quit_text,
                (10, (self.height - quit_text.get_height() - 10) * self.scale),
            )
            self.screen.blit(
                bottom_text,
                (
                    self.width - bottom_text.get_width() - 10,
                    self.width - bottom_text.get_height() - 10,
                ),
            )

            self.screen.blit(
                bottom_text,
                (
                    self.width - bottom_text.get_width() - 10,
                    self.height - bottom_text.get_height() - 10,
                ),
            )

            for i, option in enumerate(self.options):
                c = [color.WHITE, Color.GREEN][i == self.selected_option]
                option_text = self.fonts[2].render(option, True, c)
                self.screen.blit(
                    option_text,
                    (
                        (self.width // 2 - option_text.get_width() // 2) * self.scale,
                        (self.height // 2 + i * 60) * self.scale,
                    ),
                )

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(
                            self.options
                        )
                    elif e.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(
                            self.options
                        )
                    elif e.key == pygame.K_RETURN:
                        return self.selected_option
                    elif e.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            clock.tick(60)
