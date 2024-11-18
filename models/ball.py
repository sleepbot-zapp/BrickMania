from helpers.constants import (
    ball_radius, ball_speed_x, ball_speed_y, trail_length
)
from models import Color
import pygame

class Ball:
    def __init__(self, *, screen, ball_radius=ball_radius, ball_speed_x=ball_speed_x, ball_speed_y=ball_speed_y, trail_length=trail_length, trail_color=Color.GREEN) -> None:
        self.screen = screen
        self.ball_radius = ball_radius
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.trail_color = trail_color
        self.trail_length = trail_length
        self.max_alpha = 50
        self.ball_trails = []

    def draw_ball(self, x, y, ball_id, ball_radius, ball_trails):
        if ball_id not in self.ball_trails:
            self.ball_trails[ball_id] = []
        trail = ball_trails[ball_id]
        trail.append((x, y))
        if len(trail) > self.trail_length:
            trail.pop(0)
        for i, (tx, ty) in enumerate(trail):
            alpha = self.max_alpha - int(self.max_alpha * (i / self.trail_length))
            trail_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*self.color, alpha), (ball_radius, ball_radius), ball_radius)
            self.screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))
        pygame.draw.circle(self.screen, self.trail_color, (x, y), ball_radius)
