from random import choice, randint
from pygame.draw import rect


class FallingTile:
    def __init__(
        self,
        brick_width: int,
        brick_height: int,
        width: int,
        height: int,
        scale: int,
        color,
    ) -> None:
        """Initializes a falling tile with random position, speed, and color."""
        self.width = brick_width
        self.height = brick_height
        self.x = randint(0, width * scale - self.width)
        self.y = randint(-height * scale, 0)
        self.speed = randint(2, 7) * scale
        self.color = choice([color.RED, color.BLUE, color.GREEN])

    def move(self, height: int, width: int) -> None:
        """Moves the tile down and resets its position if it moves off-screen."""
        self.y += self.speed
        if self.y > height:
            self.y = randint(-height, 0)
            self.x = randint(0, width - self.width)

    def draw(self, screen) -> None:
        """Draws the tile on the given screen."""
        rect(screen, self.color, (self.x, self.y, self.width, self.height))
