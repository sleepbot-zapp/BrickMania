from helpers.constants import (
    player_height, player_width, player_speed,
)
from models import Color
import pygame

class Player:
    def __init__(self, *, screen, player_height=player_height, player_width=player_width, player_speed=player_speed,) -> None:
        self.screen = screen
        self.player_height = player_height
        self.player_width = player_width
        self.player_speed = player_speed

    def draw_player(self, x, y):
        pygame.draw.rect(self.screen, Color.BLUE, (x, y, self.player_width, self.player_height), 10)