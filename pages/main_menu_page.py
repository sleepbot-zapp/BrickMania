import pygame
from models import Color, FallingTile
from .pages import Page
from helpers import AutoEnum


class NavigationAction(AutoEnum):
    UP: int
    DOWN: int
    SELECT: int
    NONE: int
    EXIT: int


class MainMenu(Page):
    def __init__(self, screen, height, width, scale, game, options=None):
        super().__init__(screen, height, width, scale, game)
        self.font_title = pygame.font.SysFont(None, int(72 * scale))
        self.font_small = pygame.font.SysFont(None, int(25 * scale))
        self.font_option = pygame.font.SysFont(None, int(48 * scale))
        self.selected_option = 0
        self.options = options or ("Play", "Settings", "Info")

    def generate(self, color: Color, brick_width, brick_height):
        tiles = [
            FallingTile(brick_width, brick_height, self.width, self.height, self.scale, color)
            for _ in range(20)
        ]

        while True:
            action = self._handle_input()
            if action == NavigationAction.UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif action == NavigationAction.DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif action == NavigationAction.SELECT:
                return self.selected_option
            self._render(color, tiles)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return NavigationAction.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    return NavigationAction.DOWN
                elif event.key == pygame.K_UP:
                    return NavigationAction.UP
                elif event.key == pygame.K_RETURN:
                    return NavigationAction.SELECT
        return NavigationAction.NONE

    def _render(self, color: Color, tiles: list):
        self.screen.fill(color.BLACK)

        for tile in tiles:
            tile.move(self.height, self.width)
            tile.draw(self.screen)

        self.render_text(
            text="BRICKMANIA",
            font=self.font_title,
            color=color.YELLOW,
            x=(self.width // 2) * self.scale,
            y=(self.height // 2 - 150) * self.scale,
            center=True,
        )
        self.render_text(
            text="Press Q to Quit",
            font=self.font_small,
            color=color.GREY,
            x=10,
            y=(self.height - 10) * self.scale - self.font_small.get_height(),
        )
        self.render_text(
            text="Press Enter to Select",
            font=self.font_small,
            color=color.GREY,
            x=self.width * self.scale - 10,
            y=(self.height - 10) * self.scale - self.font_small.get_height(),
            right_align=True,
        )
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_option
            self.render_text(
                text=option,
                font=self.font_option,
                color=color.GREEN if is_selected else color.WHITE,
                x=(self.width // 2) * self.scale,
                y=(self.height // 2 + i * 60) * self.scale,
                center=True,
            )

        pygame.display.flip()
