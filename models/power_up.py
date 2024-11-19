from .color import Color
from pygame.draw import rect


class PowerUp:
    def __init__(self, x, y, type, scale):
        self.x = x
        self.y = y
        self.width = 40 * scale
        self.height = 20 * scale
        self.type = type
        self.color = {"extra_ball": Color().GREEN}[type]
        self.fall_speed = 120 * scale

    def move(self, dt):
        self.y += self.fall_speed * dt

    def draw(self, screen):
        rect(screen, self.color, (self.x, self.y, self.width, self.height))
