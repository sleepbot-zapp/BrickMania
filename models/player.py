import time
import pygame
from helpers import WIDTH, player_height, player_speed, player_width
from .color import Color


class Player:
    def __init__(
        self,
        *,
        screen,
        height,
        width,
        scale,
        player_height=player_height,
        player_width=player_width,
        player_speed=player_speed
    ):
        self.screen = screen
        self.width = width
        self.height = height
        self.scale = scale
        self.player_height = player_height
        self.player_width = player_width
        self.player_speed = player_speed

        # Calculate player position at start
        self.x_start = (self.width * self.scale - self.player_width) // 2
        self.y_start = self.height * scale - self.player_height - 70
        self.x_end = self.x_start + self.player_width  # Unused currently
        self.y_end = self.y_start - self.player_height  # Unused currently

    def draw_player(self):
        """Draw the player character as a rectangle."""
        pygame.draw.rect(
            self.screen,
            Color().BLUE,
            (self.x_start, self.y_start, self.player_width, self.player_height),
            border_radius=10,
        )

    def move_player(self, dt, keys, min_limit, max_limit):
        """Move the player based on input keys while respecting screen boundaries."""
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.x_start > min_limit:
            self.x_start -= self.player_speed * dt
        elif (
            keys[pygame.K_d] or keys[pygame.K_RIGHT]
        ) and self.x_start < WIDTH - self.player_width - max_limit:
            self.x_start += self.player_speed * dt

        return time.time()  # Time used for tracking, though this is unused
