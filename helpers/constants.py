import os
from typing import List

import pygame
from pydantic import BaseModel


class Screen(BaseModel):
    scale: int
    width: int
    height: int


class Inactivity(BaseModel):
    multiplier: int
    threshold: int


class Player(BaseModel):
    width: int
    height: int
    speed: int
    inactivity: Inactivity


class BallSpeed(BaseModel):
    x: int
    y: int
    increment: float


class Ball(BaseModel):
    radius: int
    speed: BallSpeed
    trail_length: int


class Brick(BaseModel):
    width: int
    height: int
    speed: int
    rows: int


class Powerup(BaseModel):
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


class MainMenuFontSize(BaseModel):
    title: int
    menu: int


class FontSize(BaseModel):
    main: int
    game_over: int
    main_menu: MainMenuFontSize


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
    powerup: Powerup
    falling_tile: FallingTile
    game_constants: GameConstants

    @classmethod
    def open(cls) -> "Config":
        return cls.model_validate_json(
            open(os.getenv("BRICKMANIA_CONFIG", "./constants.json")).read()
        )


constants = Config.open()

pygame.init()


SCALE = constants.screen.scale
WIDTH, HEIGHT = (
    int(constants.screen.width * SCALE),
    int(constants.screen.height * SCALE),
)
screen = pygame.display.set_mode((WIDTH, HEIGHT))


player_width = constants.player.width * SCALE
player_height = constants.player.height * SCALE
player_speed = constants.player.speed * SCALE


ball_radius = constants.ball.radius * SCALE
ball_speed_x = constants.ball.speed.x * SCALE
ball_speed_y = constants.ball.speed.y * SCALE
speed_increment = constants.ball.speed.increment


brick_width = int(constants.brick.width * SCALE)
brick_height = constants.brick.height * SCALE
brick_speed = constants.brick.speed * SCALE
brick_rows = constants.brick.rows
brick_cols = WIDTH // brick_width


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, int(constants.game_constants.font_size.main * SCALE))
bottom_font = pygame.font.SysFont(
    None, int(constants.game_constants.font_size.game_over * SCALE)
)


trail_length = constants.ball.trail_length
ball_trails = {}


def get_music_path(constants, n):
    return os.path.join(
        constants.game_constants.tracks.path,
        f"{constants.game_constants.tracks.files[n]}.{constants.game_constants.tracks.extension}",
    )


track_path = get_music_path(constants, 0)
track = pygame.mixer.music.load(get_music_path(constants, 0))
track1 = pygame.mixer.Sound(get_music_path(constants, 1))
track2 = pygame.mixer.Sound(get_music_path(constants, 2))
track3 = pygame.mixer.Sound(get_music_path(constants, 3))
track4 = pygame.mixer.Sound(get_music_path(constants, 4))
