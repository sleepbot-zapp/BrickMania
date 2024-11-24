import random
import pygame
from helpers import ball_radius, ball_speed_x, ball_speed_y, trail_length
from .player import Player
import math


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
        self.height = height - 150
        self.width = width
        self.scale = scale
        self.ball_radius = ball_radius
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y

        self.dx = random.choice((-1, 1)) * self.ball_speed_x
        self.dy = self.ball_speed_y
        self.x = random.randrange(self.width)
        self.y = self.height
        self.ball_crossed_line = False
        self.trail = []


    def draw_ball(self, screen, color, ball_id, x, y, ball_trails):
        """Draw the ball with a diverging 3D trail effect."""
        max_alpha = 50  # Maximum alpha for the trail
        trail_length = 5  # Length of the trail
        max_trail_width = self.ball_radius * 1.5  # Maximum width for trail segments
        min_trail_width = self.ball_radius  # Minimum width for trail segments
        divergence = 0.1 # Divergence factor for the trail

        # Fetch or create the trail for the given ball ID
        trail = ball_trails.setdefault(ball_id, [])
        trail.append((x, y))

        # Limit the trail length
        if len(trail) > trail_length:
            trail.pop(0)

        # Draw the diverging 3D trail
        for i, (tx, ty) in enumerate(trail):
            # Calculate alpha, width, and divergence for each trail segment
            alpha = max_alpha - int(max_alpha * (i / trail_length))
            trail_width = max_trail_width - (max_trail_width - min_trail_width) * (i / trail_length)
            
            # Horizontal divergence: starting from the middle of the ball
            # Starting point is the ball center (x), divergence spreads horizontally
            dx = (i / trail_length) * divergence * self.ball_radius  # Horizontal divergence
            dy = 0  # No vertical divergence

            # Create a translucent surface for the trail segment
            trail_surface = pygame.Surface(
                (trail_width * 2, trail_width * 2), pygame.SRCALPHA
            )
            trail_color = (
                max(0, color[0] - int((i / trail_length) * 60)),
                max(0, color[1] - int((i / trail_length) * 60)),
                max(0, color[2] - int((i / trail_length) * 60)),
                alpha,
            )
            pygame.draw.circle(
                trail_surface,
                trail_color,
                (int(trail_width), int(trail_width)),
                int(trail_width),
            )
            # Offset trail position to create divergence
            screen.blit(
                trail_surface,
                (tx - trail_width + dx, ty - trail_width),
            )

        # Draw the ball itself with a shaded 3D effect
        for depth in range(self.ball_radius, self.ball_radius // 2, -1):  # Start shading from the midpoint
            shade_factor = depth / self.ball_radius
            shaded_color = (
                int(color[0] * shade_factor),
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
            pygame.draw.circle(screen, shaded_color, (int(x), int(y)), depth)

        # Add a highlight for the ball
        highlight_color = (
            min(color[0] + 80, 255),
            min(color[1] + 80, 255),
            min(color[2] + 80, 255),
        )
        pygame.draw.circle(
            screen,
            highlight_color,
            (int(x - self.ball_radius // 3), int(y - self.ball_radius // 3)),
            self.ball_radius // 4,
        )




    def move_ball(self, dt, player: Player):
        """Move the ball and handle collisions."""
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.x <= self.ball_radius or self.x >= self.width - self.ball_radius:
            self.dx = -self.dx
            self.x = max(self.ball_radius, min(self.x, self.width - self.ball_radius))

        if self.y <= self.ball_radius:
            self.dy = abs(self.dy)
            self.y = self.ball_radius

        if self.y >= self.height - self.ball_radius - 60 and not self.ball_crossed_line:
            self.ball_crossed_line = True

        self._handle_paddle_collision(player)

        return self.x, self.y, self.dx, self.dy

    def _handle_paddle_collision(self, player: Player):
        """Handle collision with the player's paddle."""
        if (
            player.x_start - self.ball_radius
            < self.x
            < player.x_start + player.player_width + self.ball_radius
            and player.y_start
            < self.y + self.ball_radius
            < player.y_start + player.player_height
        ):

            paddle_center = player.x_start + player.player_width / 2
            self.dx = self.ball_speed_x * (
                (self.x - paddle_center) / (player.player_width / 2)
            )
            self.dy = -abs(self.dy)
            self.y = player.y_start - self.ball_radius
