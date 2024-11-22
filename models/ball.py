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
        self.ball_radius = ball_radius
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.dx = random.choice((1, -1)) * self.ball_speed_x
        self.dy = self.ball_speed_y
        self.ball_crossed_line = False
        self.trail = []

        # Ensure the ball spawns above the paddle, not over the bricks
        self.reset_ball_position()

    def reset_ball_position(self):
        # Start the ball near the paddle's position
        self.x = self.width // 2
        self.y = self.height - 100  # 100 pixels above the paddle


    def draw_ball(self, screen, color, ball_id, x, y, ball_trails):
        max_alpha = 50  # For trail fading
        if ball_id not in ball_trails:
            ball_trails[ball_id] = []

        # Get the trail for the current ball
        trail = ball_trails[ball_id]
        trail.append((x, y))  # Append the current position to the trail

        # Limit the trail length
        if len(trail) > trail_length:
            trail.pop(0)

        # Draw the trail with slight divergence
        for i, (tx, ty) in enumerate(trail):
            alpha = max_alpha - int(max_alpha * (i / trail_length))  # Fade effect

            # Add a small random offset to the trail for divergence
            divergence_factor = 1 + (random.uniform(-0.5, 0.5))  # Slight random divergence
            tx += divergence_factor * (i / trail_length)  # Diverge the trail along the X axis
            ty += divergence_factor * (i / trail_length)  # Diverge the trail along the Y axis

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

        # Draw the 3D filled sphere
        for depth in range(ball_radius, 0, -1):  # From outer edge to center
            shade_factor = depth / ball_radius  # Adjust shade based on depth
            shaded_color = (
                int(color[0] * shade_factor),  # Darker on the edges
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
            pygame.draw.circle(
                screen,
                shaded_color,
                (int(x), int(y)),
                depth,  # The current radius for the filled circle
            )

        # Add the highlight for a light source
        highlight_radius = ball_radius // 4
        highlight_color = (
            min(color[0] + 80, 255),
            min(color[1] + 80, 255),
            min(color[2] + 80, 255),
        )
        pygame.draw.circle(
            screen,
            highlight_color,
            (int(x - ball_radius // 3), int(y - ball_radius // 3)),  # Offset for light source
            highlight_radius,
        )


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
