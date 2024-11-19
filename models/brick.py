from .color import Color
import pygame
import random
from helpers.constants import (
    brick_cols, brick_rows, brick_width, brick_height
)


class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice([Color().RED, Color().BLUE, Color().GREEN, Color().YELLOW])

    def draw(self, screen, brick_width, brick_height):
        pygame.draw.rect(screen, self.color, (self.x, self.y, brick_width, brick_height))
        pygame.draw.rect(screen, Color().BLACK, (self.x, self.y, brick_width, brick_height), 2)


def create_new_bricks():
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks