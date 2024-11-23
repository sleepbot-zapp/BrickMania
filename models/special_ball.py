from pygame.draw import circle
from .color import Color


class SpecialBall:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, ball_radius, width, dt):
        """Move the ball and handle bouncing off the edges."""
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.x <= ball_radius or self.x >= width - ball_radius:
            self.dx = -self.dx

        if self.y <= ball_radius:
            self.dy = -self.dy

    def draw(self, screen, ball_radius):
        """Draw the ball on the screen."""
        circle(screen, Color().RED, (self.x, self.y), ball_radius)
