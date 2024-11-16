from .color import Color
from pygame.draw import circle


class SpecialBall:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, ball_radius, WIDTH):
        self.x += self.dx
        self.y += self.dy

        if self.x <= ball_radius or self.x >= WIDTH - ball_radius:
            self.dx = -self.dx

        if self.y <= ball_radius:
            self.dy = -self.dy

    def draw(self, screen, ball_radius):
        circle(screen, Color.RED, (self.x, self.y), ball_radius)
