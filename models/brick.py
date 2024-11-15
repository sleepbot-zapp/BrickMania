from .color import Color# RED, BLUE, GREEN, YELLOW, BLACK
from pygame.draw import rect
from random import choice


class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = choice([Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW])

    def draw(self, screen, brick_width, brick_height):
        rect(screen, self.color, (self.x, self.y, brick_width, brick_height))
        rect(screen, Color.BLACK, (self.x, self.y, brick_width, brick_height), 2)
