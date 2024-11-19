from helpers.constants import (
    HEIGHT, WIDTH, SCALE,
    track, track1, track2, track3
)
from models import Player, Ball, Color
import pygame

class Game:
    def __init__(self, *, height=HEIGHT, width=WIDTH, scale=SCALE,) -> None:
        pygame.init()
        # window
        self.height = height
        self.width = width
        self.scale = scale
        self.screen = pygame.display.set_mode((self.height, self.width))
        # colors
        self.colors = Color()
        # entities
        self.player = Player(screen=self.screen, height=self.height, width=self.width, scale=self.scale)
        self.balls = [Ball(screen=self.screen, height=self.height, width=self.width, scale=self.scale)]
        # game variables
        self.clock = pygame.time.Clock()
        self.music_files = track, track1, track2, track3
        self.music_is_playing = False
        self.keys = pygame.key.get_pressed()
        # entity variables
        self.trails = []


    def gameloop(self):...

