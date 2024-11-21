from helpers.constants import ball_radius, ball_speed_x, ball_speed_y, trail_length
from models.player import Player
import random
from models import Color
import pygame


class Ball:
    def __init__(
        self,
        *,
        screen,
        height,
        width,
        scale,
        ball_radius=ball_radius,
        ball_speed_x=ball_speed_x,
        ball_speed_y=ball_speed_y,
    ) -> None:
        self.screen = screen
        self.height = height
        self.width = width
        self.scale = scale
        self.x = random.randint(200, self.width // 2)
        self.y = random.randint(300, 400)
        self.ball_radius = ball_radius
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.dx = random.choice((1, -1)) * self.ball_speed_x
        self.dy = ball_speed_y
        self.ball_crossed_line = False
        self.trail = []

    def draw_ball(self, screen, color, ball_id, x, y, ball_trails):
        max_alpha = 50
        if ball_id not in ball_trails:
            ball_trails[ball_id] = []

        # Get the trail for the current ball
        trail = ball_trails[ball_id]
        trail.append((x, y))  # Append the current position to the trail

        # Limit the trail length
        if len(trail) > trail_length:
            trail.pop(0)

        # Draw the trail
        for i, (tx, ty) in enumerate(trail):
            alpha = max_alpha - int(max_alpha * (i / trail_length))  # Fade effect
            trail_surface = pygame.Surface(
                (ball_radius * 2, ball_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                trail_surface,
                (color[0], color[1], color[2], alpha),
                (ball_radius, ball_radius),
                ball_radius,
            )
            screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))

        # Draw the ball itself
        pygame.draw.circle(screen, color, (int(x), int(y)), ball_radius)

    def move_ball(self, dt, player: Player):
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Ensure ball stays within horizontal bounds
        if self.x <= self.ball_radius:
            self.x = self.ball_radius + 1
            self.dx = abs(self.dx)
        elif self.x >= self.width - self.ball_radius:
            self.x = self.width - self.ball_radius - 1
            self.dx = -abs(self.dx)

        # Ensure ball stays within vertical bounds (y >= 0)
        if self.y <= self.ball_radius:
            self.y = self.ball_radius + 1
            self.dy = abs(self.dy)  # Reflect the ball downwards

        # Mark the ball as crossed if it goes below the line
        if self.y >= self.height - self.ball_radius - 60 and not self.ball_crossed_line:
            self.ball_crossed_line = True

        # Check collision with the player paddle
        player_center = player.x_start + player.player_width / 2
        dx_from_center = (self.x - player_center) / (player.player_width / 2)

        if (
            player.x_start - self.ball_radius
            < self.x
            < player.x_start + player.player_width + self.ball_radius
            and player.y_start
            < self.y + self.ball_radius
            < player.y_start + player.player_height
        ):
            self.dx = self.ball_speed_x * dx_from_center
            self.dx += [50, -50][self.dx < 0]  # Add a small boost to speed
            self.dy = -abs(self.dy)  # Reflect the ball upwards
            self.y = player.y_start - self.ball_radius

        return self.x, self.y, self.dx, self.dy
