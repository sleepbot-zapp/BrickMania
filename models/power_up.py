from .color import Color
import pygame
import random


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
        self.y += self.fall_speed * dt

    def draw(self, screen):
        # Draw the rectangle
        pygame.draw.rect(screen, self.color[0], (self.x, self.y, self.width, self.height))

        # Calculate the center of the rectangle
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # Calculate the radius of the circle (slightly smaller than the rectangle)
        circle_radius = min(self.width, self.height) // 3

        # Draw the circle in the center of the rectangle
        pygame.draw.circle(screen, self.color[1], (center_x, center_y), circle_radius)



def drop_powerup(brick_x, brick_y, powerups, scale):
    powerup_type = random.choice(
        [
            "extra_ball",
        ]
    )
    if len(powerups) < 2 and random.random() < 0.1:
        return PowerUp(brick_x, brick_y, powerup_type, scale)
    return None
