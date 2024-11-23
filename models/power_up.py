import random
import pygame
from .color import Color


class PowerUp:
    def __init__(self, x, y, type, scale):
        self.x = x
        self.y = y
        self.width = 40 * scale
        self.height = 20 * scale
        self.type = type
        self.color = [Color().GREEN, Color().RED]
        self.fall_speed = 120 * scale

    def move(self, dt):
        """Move the power-up down the screen based on time delta."""
        self.y += self.fall_speed * dt

    def draw(self, screen):
        """Draw the power-up as a rectangle with a circle inside it."""
        self._draw_rectangle(screen)
        self._draw_circle(screen)

    def _draw_rectangle(self, screen):
        """Draw the rectangle for the power-up."""
        pygame.draw.rect(
            screen, self.color[0], (self.x, self.y, self.width, self.height)
        )

    def _draw_circle(self, screen):
        """Draw a circle inside the power-up rectangle."""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        circle_radius = min(self.width, self.height) // 3
        pygame.draw.circle(screen, self.color[1], (center_x, center_y), circle_radius)


def drop_powerup(brick_x, brick_y, powerups, scale):
    """Drop a power-up with a 10% chance when there are fewer than 2 active power-ups."""
    if len(powerups) < 2 and random.random() < 0.1:
        powerup_type = "extra_ball"
        return PowerUp(brick_x, brick_y, powerup_type, scale)
    return None
