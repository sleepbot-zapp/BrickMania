import math
import random
from pygame import (
    K_LSHIFT,
    K_RETURN,
    K_RSHIFT,
    KEYDOWN,
    MOUSEMOTION,
    MOUSEWHEEL,
    QUIT,
    event,
    quit,
)
from pygame.display import flip
from pygame.draw import line
from pygame.font import SysFont

from helpers.constants import HEIGHT, WIDTH, bottom_font, clock, screen
from helpers.loading_combinations import combs


def loading_screen(color):
    """Display a dynamic loading screen with animations and tips."""

    func1, func2 = random.choice(combs)
    radius = 30
    spinner_segments = 12
    angle_per_segment = 360 / spinner_segments
    spinner_speed = 2
    angle = 0

    spinner_center = [WIDTH // 2, HEIGHT // 2]
    frame_count = 0

    tip_font = SysFont("Arial", 24)
    tips = [
        "Use the paddle to deflect the ball!",
        "Hit bricks for power-ups!",
        "Press UP to launch a special ball!",
        "Stay active to avoid the paddle drifting!",
        "Press DOWN to destroy 5 random bricks!",
    ]
    tip = random.choice(tips)

    rotation_angle_x = 30
    rotation_angle_y = 30

    def rotate_3d(x, y, z, angle_x, angle_y):
        """Rotate a point in 3D space around X and Y axes."""
        y, z = (
            y * math.cos(math.radians(angle_x)) - z * math.sin(math.radians(angle_x)),
            y * math.sin(math.radians(angle_x)) + z * math.cos(math.radians(angle_x)),
        )
        x, z = (
            x * math.cos(math.radians(angle_y)) + z * math.sin(math.radians(angle_y)),
            -x * math.sin(math.radians(angle_y)) + z * math.cos(math.radians(angle_y)),
        )
        return x, y

    while True:
        screen.fill(color.BLACK)
        clock.tick(60)

        # Header
        loading_text = tip_font.render("BrickMania", True, color.WHITE)
        screen.blit(
            loading_text,
            (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - 123),
        )

        tip_text = tip_font.render("Tip: " + tip, True, color.WHITE)
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT // 2 + 123))

        # Animate spinner center
        spinner_center[0] = WIDTH // 2 + 100 * math.sin(frame_count * 0.02) + random.uniform(-2, 2)
        spinner_center[1] = HEIGHT // 2 + 50 * math.cos(frame_count * 0.03) + random.uniform(-2, 2)

        scale_factor_x = 1 + (spinner_center[0] - WIDTH // 2) / WIDTH
        scale_factor_y = 1 - (spinner_center[1] - HEIGHT // 2) / HEIGHT
        scale_factor = max(0.5, min(2, scale_factor_x * scale_factor_y))

        for i in range(spinner_segments):
            seg_start = angle + (i * angle_per_segment)
            seg_end = seg_start + angle_per_segment

            x1 = radius * scale_factor * func1(math.cos(math.radians(seg_start)))
            y1 = radius * scale_factor * func1(math.sin(math.radians(seg_start)))
            x2 = radius * scale_factor * func2(math.cos(math.radians(seg_end)))
            y2 = radius * scale_factor * func2(math.sin(math.radians(seg_end)))

            sx1, sy1 = rotate_3d(x1, y1, 0, rotation_angle_x, rotation_angle_y)
            ex1, ey1 = rotate_3d(-x1, -y1, 0, rotation_angle_x, rotation_angle_y)
            sx2, sy2 = rotate_3d(x2, y2, 0, rotation_angle_x, rotation_angle_y)
            ex2, ey2 = rotate_3d(-x2, -y2, 0, rotation_angle_x, rotation_angle_y)

            line(screen, color.BLUE, (ex1 + spinner_center[0], ey1 + spinner_center[1]),
                 (ex2 + spinner_center[0], ey2 + spinner_center[1]), 3)
            line(screen, color.RED, (sx1 + spinner_center[0], sy1 + spinner_center[1]),
                 (sx2 + spinner_center[0], sy2 + spinner_center[1]), 3)

        angle += spinner_speed
        frame_count += 1

        # Bottom prompts
        shift_text = bottom_font.render("Press Shift to go back", True, (92, 95, 119))
        screen.blit(shift_text, (10, HEIGHT - shift_text.get_height() - 10))

        enter_text = bottom_font.render("Press Enter to Continue", True, (92, 95, 119))
        screen.blit(enter_text, (WIDTH - enter_text.get_width() - 10, HEIGHT - enter_text.get_height() - 10))

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    return
                if e.key in (K_LSHIFT, K_RSHIFT):
                    return True
            if e.type == MOUSEMOTION and e.buttons[0]:
                rotation_angle_x = max(0, min(90, rotation_angle_x + e.rel[1] * 0.5))
                rotation_angle_y += e.rel[0] * 0.5
            if e.type == MOUSEWHEEL:
                spinner_speed = 2 if e.y > 0 else -2

        flip()
