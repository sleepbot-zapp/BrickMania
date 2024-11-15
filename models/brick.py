from .color import RED, BLUE, GREEN, YELLOW, BLACK
from pygame.draw import rect
from random import choice

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = choice([RED, BLUE, GREEN, YELLOW])

    def draw(self, screen, brick_width, brick_height):
        rect(screen, self.color, (self.x, self.y, brick_width, brick_height))
        rect(screen, BLACK, (self.x, self.y, brick_width, brick_height), 2)