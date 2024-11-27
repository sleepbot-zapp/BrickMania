import typing
import pygame
from helpers import AutoEnum
from .pages import Page
from models import Color


class SettingsOption(AutoEnum):
    MUSIC = 0
    COLORS = 1


class ColorComponent(AutoEnum):
    RED = 0
    GREEN = 1
    BLUE = 2


class EditingMode(AutoEnum):
    NONE = 0
    EDITING = 1


class Settings(Page):
    def __init__(
        self,
        screen,
        height: typing.Union[int, float],
        width: typing.Union[int, float],
        scale: typing.Union[int, float],
        game,
        settings_options: typing.Tuple[str] = None,
    ) -> None:
        super().__init__(screen, height, width, scale, game)

        self.fonts = (
            pygame.font.SysFont(None, int(72 * self.scale)),
            pygame.font.SysFont(None, int(32 * self.scale)),
        )
        self.selected_option: SettingsOption = SettingsOption.MUSIC
        self.settings_options = settings_options or ["Music", "Colors"]
        self.color_keys = list(self.game.colors.__dict__.keys())
        self.selected_color_index = 0
        self.color_edit_component: ColorComponent = ColorComponent.RED
        self.editing_mode: EditingMode = EditingMode.NONE
        self.numeric_input = ""

    def display(self) -> bool:
        """Main settings menu where options are displayed."""
        while True:
            self.screen.fill(self.game.colors.BLACK)
            header_font = self.fonts[0]
            header_text = header_font.render("Settings", True, self.game.colors.WHITE)
            header_rect = header_text.get_rect(
                center=(self.width // 2, int(50 * self.scale))
            )
            self.screen.blit(header_text, header_rect)
            options_font = self.fonts[0]
            for i, option in enumerate(self.settings_options):
                c = (
                    self.game.colors.GREEN
                    if i == self.selected_option.value
                    else self.game.colors.WHITE
                )
                option_text = options_font.render(option, True, c)
                option_rect = option_text.get_rect(
                    center=(self.width // 2, int(150 * self.scale) + (i + 1) * 100)
                )
                self.screen.blit(option_text, option_rect)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.selected_option = SettingsOption(
                            (self.selected_option.value + 1) % len(self.settings_options)
                        )
                    elif e.key == pygame.K_UP:
                        self.selected_option = SettingsOption(
                            (self.selected_option.value - 1) % len(self.settings_options)
                        )
                    elif e.key == pygame.K_RETURN:
                        if self.selected_option == SettingsOption.MUSIC:
                            self.display_music_settings()
                        elif self.selected_option == SettingsOption.COLORS:
                            self.display_color_settings()
                    elif e.key == pygame.K_RSHIFT:
                        return True

            pygame.display.flip()

    def display_music_settings(self) -> None:
        """Display the Music settings screen."""
        bar_width = int(300 * self.scale)
        bar_height = int(20 * self.scale)
        bar_x = self.width // 2
        bar_y = self.height // 2
        while True:
            self.screen.fill(self.game.colors.BLACK)
            header_font = self.fonts[0]
            header_text = header_font.render(
                "Music Settings", True, self.game.colors.WHITE
            )
            header_rect = header_text.get_rect(
                center=(self.width // 2, int(50 * self.scale))
            )
            self.screen.blit(header_text, header_rect)
            options_font = self.fonts[1]
            volume_label_text = options_font.render(
                "Volume:", True, self.game.colors.WHITE
            )
            volume_label_rect = volume_label_text.get_rect(
                center=(bar_x - bar_width // 2 - 60, bar_y + bar_height // 2)
            )
            self.screen.blit(volume_label_text, volume_label_rect)
            pygame.draw.rect(
                self.screen,
                self.game.colors.GREY,
                (bar_x - bar_width // 2, bar_y, bar_width, bar_height),
            )
            filled_width = int(bar_width * self.game.volume)
            pygame.draw.rect(
                self.screen,
                self.game.colors.GREEN,
                (bar_x - bar_width // 2, bar_y, filled_width, bar_height),
            )

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RSHIFT:
                        return
                    elif e.key == pygame.K_RIGHT:
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

    def display_color_settings(self) -> None:
        """Display the Color settings screen with RGB values and editing functionality."""
        while True:
            self.screen.fill(self.game.colors.BLACK)
            header_font = self.fonts[0]
            header_text = header_font.render(
                "Color Settings", True, self.game.colors.WHITE
            )
            header_rect = header_text.get_rect(
                center=(self.width // 2, int(50 * self.scale))
            )
            self.screen.blit(header_text, header_rect)
            options_font = self.fonts[1]

            for i, color_name in enumerate(self.color_keys):
                color_value = getattr(self.game.colors, color_name)
                highlight = (
                    self.game.colors.GREEN
                    if i == self.selected_color_index
                    else self.game.colors.WHITE
                )
                color_label_text = options_font.render(
                    f"{color_name} (R: {color_value[0]}, G: {color_value[1]}, B: {color_value[2]})",
                    True,
                    highlight,
                )
                color_label_rect = color_label_text.get_rect(
                    center=(self.width // 2 - 100, 150 + i * 50)
                )
                self.screen.blit(color_label_text, color_label_rect)
                pygame.draw.rect(
                    self.screen,
                    color_value,
                    (self.width // 2 + 200, 130 + i * 50, 40, 40),
                )
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    (self.width // 2 + 200, 130 + i * 50, 40, 40),
                    2,
                )
                if i == self.selected_color_index:
                    arrow_text = options_font.render("*", True, self.game.colors.GREEN)
                    arrow_rect = arrow_text.get_rect(
                        center=(self.width // 2 - 300, 150 + i * 50)
                    )
                    self.screen.blit(arrow_text, arrow_rect)

            if self.editing_mode == EditingMode.EDITING:
                selected_color_name = self.color_keys[self.selected_color_index]
                selected_color = list(getattr(self.game.colors, selected_color_name))
                for j, component in enumerate([ColorComponent.RED, ColorComponent.GREEN, ColorComponent.BLUE]):
                    highlight = (
                        self.game.colors.GREEN
                        if component == self.color_edit_component
                        else self.game.colors.WHITE
                    )
                    component_text = options_font.render(
                        f"{component.name}: {selected_color[component.value]}", True, highlight
                    )
                    component_rect = component_text.get_rect(
                        center=(self.width // 2 + (j - 1) * 100, 525)
                    )
                    self.screen.blit(component_text, component_rect)

                if self.numeric_input:
                    numeric_input_text = options_font.render(
                        f"Input: {self.numeric_input}", True, self.game.colors.RED
                    )
                    numeric_input_rect = numeric_input_text.get_rect(
                        center=(self.width // 2, 575)
                    )
                    self.screen.blit(numeric_input_text, numeric_input_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                        if self.editing_mode == EditingMode.EDITING:
                            self.editing_mode = EditingMode.NONE
                            self.numeric_input = ""
                        else:
                            return
                    elif self.editing_mode == EditingMode.NONE:
                        if event.key == pygame.K_r:
                            self.game.colors = Color()
                        if event.key == pygame.K_DOWN:
                            self.selected_color_index = (
                                self.selected_color_index + 1
                            ) % len(self.color_keys)
                        elif event.key == pygame.K_UP:
                            self.selected_color_index = (
                                self.selected_color_index - 1
                            ) % len(self.color_keys)
                        elif event.key == pygame.K_RETURN:
                            self.editing_mode = EditingMode.EDITING
                    elif self.editing_mode == EditingMode.EDITING:
                        selected_color_name = self.color_keys[self.selected_color_index]
                        selected_color = list(
                            getattr(self.game.colors, selected_color_name)
                        )
                        if event.key == pygame.K_r:
                            self.game.colors.__dict__[selected_color_name] = (
                                Color.__dict__[selected_color_name]
                            )
                        if event.key == pygame.K_RIGHT:
                            self.color_edit_component = ColorComponent(
                                (self.color_edit_component.value + 1) % 3
                            )
                        elif event.key == pygame.K_LEFT:
                            self.color_edit_component = ColorComponent(
                                (self.color_edit_component.value - 1) % 3
                            )
                        elif event.key == pygame.K_UP:
                            selected_color[self.color_edit_component.value] = min(
                                255, selected_color[self.color_edit_component.value] + 1
                            )
                            setattr(
                                self.game.colors,
                                selected_color_name,
                                tuple(selected_color),
                            )
                        elif event.key == pygame.K_DOWN:
                            selected_color[self.color_edit_component.value] = max(
                                0, selected_color[self.color_edit_component.value] - 1
                            )
                            setattr(
                                self.game.colors,
                                selected_color_name,
                                tuple(selected_color),
                            )
                        elif event.key == pygame.K_RETURN:
                            if self.numeric_input:
                                value = min(255, max(0, int(self.numeric_input)))
                                selected_color[self.color_edit_component.value] = value
                                setattr(
                                    self.game.colors,
                                    selected_color_name,
                                    tuple(selected_color),
                                )
                                self.numeric_input = ""
                            else:
                                self.editing_mode = EditingMode.NONE
                        elif event.key == pygame.K_BACKSPACE:
                            self.numeric_input = self.numeric_input[:-1]
                        elif event.unicode.isdigit():
                            self.numeric_input += event.unicode
                            if int(self.numeric_input) > 255:
                                self.numeric_input = "255"

            pygame.display.flip()
