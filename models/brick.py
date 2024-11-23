import random
import pygame
from helpers import brick_cols, brick_height, brick_rows, brick_speed, brick_width
from .color import Color


class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.speed = brick_speed
        self.height = brick_height
        self.width = brick_width
        self.color = random.choice([color.RED, color.BLUE, color.GREEN, color.YELLOW])
        self.black = color.BLACK

    def draw(self, screen):
        """Draw the brick with a gradient color."""
        gradient_surface = self._create_gradient_surface()
        screen.blit(gradient_surface, (self.x, self.y))
        pygame.draw.rect(
            screen, self.black, (self.x, self.y, self.width, self.height), 2
        )

    def _create_gradient_surface(self):
        """Create the gradient surface for brick."""
        gradient_surface = pygame.Surface((self.width, self.height))

        light_color = self._adjust_color(self.color, 50)
        dark_color = self._adjust_color(self.color, -50)

        for y in range(self.height):
            ratio = y / self.height
            r, g, b = self._calculate_gradient_color(dark_color, light_color, ratio)
            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (self.width, y))

        return gradient_surface

    @staticmethod
    def _adjust_color(color, delta):
        """Adjust the color by a delta value."""
        return (
            max(0, min(color[0] + delta, 255)),
            max(0, min(color[1] + delta, 255)),
            max(0, min(color[2] + delta, 255)),
        )

    @staticmethod
    def _calculate_gradient_color(dark_color, light_color, ratio):
        """Calculate the gradient color based on the ratio."""
        r = int(dark_color[0] * (1 - ratio) + light_color[0] * ratio)
        g = int(dark_color[1] * (1 - ratio) + light_color[1] * ratio)
        b = int(dark_color[2] * (1 - ratio) + light_color[2] * ratio)
        return r, g, b


def create_new_bricks(color):
    """Create a list of new bricks based on the grid size."""
    return [
        Brick(col * brick_width, row * brick_height, color)
        for col in range(brick_cols)
        for row in range(brick_rows)
    ]


def draw_bricks(bricks, screen):
    """Draw all bricks on the screen."""
    for brick in bricks:
        brick.draw(screen)
