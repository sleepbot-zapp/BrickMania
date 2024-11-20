import typing
import pygame
import sys
from models import FallingTile, Color

class Page:
    def __init__(self, screen, height, width, scale, fonts: typing.Dict[str, pygame.font.SysFont]) -> None:
        self.screen = screen
        self.height = height
        self.width = width
        self.scale = scale
        self.fonts = fonts
