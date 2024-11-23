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

    def draw(self, screen, ball_radius, color):
        """Draw the ball on the screen with a 3D-like gradient effect."""
        gradient_steps = 10  # Number of gradient steps to create the depth effect
        base_color = color.RED
        
        # Create the gradient effect by drawing multiple circles
        for i in range(gradient_steps):
            # Calculate the shading for each circle, giving the effect of light direction
            shade_factor = i / gradient_steps
            r = int(base_color[0] * (1 - shade_factor))
            g = int(base_color[1] * (1 - shade_factor))
            b = int(base_color[2] * (1 - shade_factor))

            # Draw each circle slightly smaller and with darker color for the 3D effect
            circle(
                screen,
                (r, g, b),  # Adjusted color for each layer
                (self.x, self.y),
                ball_radius - i  # Each layer gets progressively smaller
            )
