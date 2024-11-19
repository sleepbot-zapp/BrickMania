from helpers.constants import (
    HEIGHT, WIDTH, SCALE,
    track, track1, track2, track3
)
from models import Player, Ball
import pygame

class Game:
    def __init__(self, *,height=HEIGHT, width=WIDTH, scale=SCALE,) -> None:
        pygame.init()
        # window
        self.height = height
        self.width = width
        self.scale = scale
        self.screen = pygame.display.set_mode((self.height, self.width))
        # entities
        self.player = Player()
        self.balls = [Ball()]
        # game costants
        self.clock = pygame.time.Clock()
        self.music_files = track, track1, track2, track3
        self.music_is_playing = False
        self.keys = pygame.key.get_pressed()

