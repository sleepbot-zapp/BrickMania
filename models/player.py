import time
import pygame
from helpers import WIDTH, player_height, player_speed, player_width


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

        
        self.x_start = (self.width * self.scale - self.player_width) // 2
        self.y_start = self.height * scale - self.player_height - 70
        self.x_end = self.x_start + self.player_width  
        self.y_end = self.y_start - self.player_height  


    def draw_player(self, color):
        """Draw the player character as a rectangle with a 3D-like gradient effect."""
        gradient_steps = 10  
        base_color = color.BLUE
        for i in range(gradient_steps):
            
            
            shade_factor = i / gradient_steps
            r = int(base_color[0] * (1 - shade_factor))
            g = int(base_color[1] * (1 - shade_factor))
            b = int(base_color[2] * (1 - shade_factor))

            
            pygame.draw.rect(
                self.screen,
                (r, g, b),
                (
                    self.x_start + i, 
                    self.y_start + i, 
                    self.player_width - 2 * i, 
                    self.player_height - 2 * i
                ),
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

        return time.time()  
