from helpers.constants import (
    HEIGHT, WIDTH, SCALE,
    player_height, player_width, player_speed,
)
import time
from models import Color
import pygame

class Player:
    def __init__(self, *, screen, height, width, scale, player_height=player_height, player_width=player_width, player_speed=player_speed,) -> None:
        self.screen = screen
        self.width = width
        self.height = height
        self.scale = scale
        self.player_height = player_height
        self.player_width = player_width
        self.player_speed = player_speed
        self.x_start = (self.width * self.scale - self.player_width) // 2
        self.x_end = self.x_start + self.player_width
        self.y_start = self.height * scale - self.player_height - 70
        self.y_end  = self.y_start - self.player_height
        
        
    def draw_player(self):
        pygame.draw.rect(self.screen, Color().BLUE, (self.x_start, self.y_start, self.player_width, self.player_height), 10)

    def move_player(self, dt, keys, min_limit, max_limit):
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.x_start > min_limit:
            self.x_start -= self.player_speed * dt
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.x_start < WIDTH - self.player_width - max_limit:
            player_x += self.player_speed * dt
        return time.time()
