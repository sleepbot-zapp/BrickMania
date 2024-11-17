import pygame

from pydantic import BaseModel
from typing import List, Optional
import os


class Screen(BaseModel):
    scale: float
    width: int
    height: int


class PlayerInactivity(BaseModel):
    multiplier: int
    threshold: int


class Player(BaseModel):
    width: int
    height: int
    speed: int
    inactivity: PlayerInactivity


class Ball(BaseModel):
    radius: int
    speed_x: int
    speed_y: int
    speed_increment: float


class Brick(BaseModel):
    width: int
    height: int
    speed: int
    rows: int
    move_speed: int


class PowerUp(BaseModel):
    width: int
    height: int
    fall_speed: int
    probability: float
    max_length: int


class FallingTile(BaseModel):
    x_min: int
    y_max: int
    speed_upper: int
    speed_lower: int
    count: int


class Interval(BaseModel):
    special_ball: int
    random_destruction: int


class Duration(BaseModel):
    special_ball: int
    random_destruction: int


class FontSize(BaseModel):
    main: int
    game_over: int

    class MainMenu(BaseModel):
        title: int
        menu: int

    main_menu: MainMenu


class Tracks(BaseModel):
    path: str
    files: List[str]
    extension: str


class GameConstants(BaseModel):
    title: str
    inactivity_threshold: int
    interval: Interval
    duration: Duration
    font_size: FontSize
    game_modes: List[str]
    frames_per_second: int
    tracks: Tracks


class Config(BaseModel):
    screen: Screen
    player: Player
    ball: Ball
    brick: Brick
    powerup: PowerUp
    falling_tile: FallingTile
    game_constants: GameConstants

    @classmethod
    def open(cls) -> Optional['Config']:
        cls.model_validate_json(open(os.getenv("BRICKMANIA_CONFIGURATION", "./constants.json"), 'r').read())


pygame.init()
SCALE = 1
WIDTH, HEIGHT = int(800 * SCALE), int(600 * SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player_width = 100 * SCALE
player_height = 20 * SCALE
player_speed = 900 * SCALE

ball_radius = 10 * SCALE
ball_speed_x, ball_speed_y = 300 * SCALE, -300 * SCALE

brick_width = int(80 * SCALE)
brick_height = 20 * SCALE
brick_speed = 100 * SCALE
brick_rows = 6
brick_cols = WIDTH // brick_width

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, int(25 * SCALE))
bottom_font = pygame.font.SysFont(None, int(20 * SCALE))
trail_length = 10
ball_trails = {}

speed_increment = 1.0001

track1 = pygame.mixer.Sound("./assets/music1.mp3")
track2 = pygame.mixer.Sound("./assets/music2.mp3")
track3 = pygame.mixer.Sound("./assets/music3.mp3")
