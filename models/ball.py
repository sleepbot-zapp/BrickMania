import random
import pygame
from helpers import ball_radius, ball_speed_x, ball_speed_y
from models import ColorType
from .player import Player
import typing


class Ball:
    def __init__(
        self,
        *,
        screen,
        height: typing.Union[int, float],
        width: typing.Union[int, float],
        scale: typing.Union[int, float],
        ball_radius: typing.Union[int, float]=ball_radius,
        ball_speed_x: typing.Union[int, float]=ball_speed_x,
        ball_speed_y: typing.Union[int, float]=ball_speed_y,
    ) -> None:

        self.screen = screen
        self.height: typing.Union[int, float] = height - 150
        self.width: typing.Union[int, float] = width
        self.scale: typing.Union[int, float] = scale
        self.ball_radius: typing.Union[int, float] = ball_radius
        self.ball_speed_x: typing.Union[int, float] = ball_speed_x
        self.ball_speed_y: typing.Union[int, float] = ball_speed_y

        self.dx: typing.Union[int, float] = random.choice((-1, 1)) * self.ball_speed_x
        self.dy: typing.Union[int, float] = self.ball_speed_y
        self.x: typing.Union[int, float] = random.randrange(self.width)
        self.y: typing.Union[int, float] = self.height
        self.ball_crossed_line: bool = False
        self.trail: typing.List[typing.Tuple[typing.Union[int, float], typing.Union[int, float]]] = []


    def draw_ball(self, screen, color: typing.Tuple[ColorType, ...] , ball_id: int, x: typing.Union[int, float], y: typing.Union[int, float], ball_trails):
        """Draw the ball with a diverging 3D trail effect."""
        max_alpha: typing.Union[int, float] = 50  
        trail_length: typing.Union[int, float] = 10
        max_trail_width: typing.Union[int, float] = self.ball_radius * 1.5  
        min_trail_width: typing.Union[int, float] = self.ball_radius  
        divergence: typing.Union[int, float] = 0.1 
        trail = ball_trails.setdefault(ball_id, [])
        trail.append((x, y))
        if len(trail) > trail_length:
            trail.pop(0)
 
        for i, (tx, ty) in enumerate(trail):
            alpha: typing.Union[int, float] = max_alpha - int(max_alpha * (i / trail_length))
            trail_width: typing.Union[int, float] = max_trail_width - (max_trail_width - min_trail_width) * (i / trail_length)
            dx: typing.Union[int, float] = (i / trail_length) * divergence * self.ball_radius  
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
            screen.blit(
                trail_surface,
                (tx - trail_width + dx, ty - trail_width),
            )

        for depth in range(self.ball_radius, self.ball_radius // 2, -1):  
            shade_factor = depth / self.ball_radius
            shaded_color = (
                int(color[0] * shade_factor),
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
            pygame.draw.circle(screen, shaded_color, (int(x), int(y)), depth)

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

        
        if self.y >= self.height - self.ball_radius - 60:
            if not self.ball_crossed_line:
                self.ball_crossed_line = True  
            else:
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
