import math
import random
from random import choice, uniform
from sys import exit
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
    time = 0
    move_speed = 2

    tip_font = SysFont("Arial", 24)
    tips = [
        "Use the paddle to deflect the ball!",
        "Hit bricks for power-ups!",
        "Press UP to launch a special ball!",
        "Stay active to avoid the paddle drifting!",
        "Press DOWN to destroy 5 random bricks!",
    ]
    tip = choice(tips)

    rotation_angle_x = 30
    rotation_angle_y = 30

    while True:
        screen.fill(color.BLACK)
        clock.tick(60)

        loading_text = tip_font.render("BrickMania", True, color.WHITE)
        screen.blit(
            loading_text,
            (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - 123),
        )

        tip_text = tip_font.render("Tip: " + tip, True, color.WHITE)
        screen.blit(
            tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT // 2 + 123)
        )

        spinner_center[0] = WIDTH // 2 + 100 * math.sin(time * 0.02) + uniform(-2, 2)
        spinner_center[1] = HEIGHT // 2 + 50 * math.cos(time * 0.03) + uniform(-2, 2)

        scale_factor_x = 1 + (spinner_center[0] - WIDTH // 2) / WIDTH
        scale_factor_y = 1 - (spinner_center[1] - HEIGHT // 2) / HEIGHT
        scale_factor = max(0.5, min(2, scale_factor_x * scale_factor_y))

        def rotate_3d(x, y, z, angle_x, angle_y):
            """Rotate a point in 3D space around X and Y axes."""

            new_y = y * math.cos(math.radians(angle_x)) - z * math.sin(
                math.radians(angle_x)
            )
            new_z = y * math.sin(math.radians(angle_x)) + z * math.cos(
                math.radians(angle_x)
            )
            y, z = new_y, new_z

            new_x = x * math.cos(math.radians(angle_y)) + z * math.sin(
                math.radians(angle_y)
            )
            new_z = -x * math.sin(math.radians(angle_y)) + z * math.cos(
                math.radians(angle_y)
            )
            x, z = new_x, new_z

            return x, y, z

        for i in range(spinner_segments):
            segment_angle_start = angle + (i * angle_per_segment)
            segment_angle_end = segment_angle_start + angle_per_segment

            x1 = (
                radius
                * scale_factor
                * func1(math.cos(math.radians(segment_angle_start)))
            )
            y1 = (
                radius
                * scale_factor
                * func1(math.sin(math.radians(segment_angle_start)))
            )
            z1 = 0

            x2 = (
                radius * scale_factor * func2(math.cos(math.radians(segment_angle_end)))
            )
            y2 = (
                radius * scale_factor * func2(math.sin(math.radians(segment_angle_end)))
            )
            z2 = 0

            start_x1, start_y1, _ = rotate_3d(
                x1, y1, z1, rotation_angle_x, rotation_angle_y
            )
            end_x1, end_y1, _ = rotate_3d(
                -x1, -y1, z1, rotation_angle_x, rotation_angle_y
            )
            start_x2, start_y2, _ = rotate_3d(
                x2, y2, z2, rotation_angle_x, rotation_angle_y
            )
            end_x2, end_y2, _ = rotate_3d(
                -x2, -y2, z2, rotation_angle_x, rotation_angle_y
            )

            start_x1 += spinner_center[0]
            start_y1 += spinner_center[1]
            end_x1 += spinner_center[0]
            end_y1 += spinner_center[1]
            start_x2 += spinner_center[0]
            start_y2 += spinner_center[1]
            end_x2 += spinner_center[0]
            end_y2 += spinner_center[1]

            line(screen, color.BLUE, (end_x1, end_y1), (end_x2, end_y2), 3)
            line(screen, color.RED, (start_x1, start_y1), (start_x2, start_y2), 3)

        angle += spinner_speed
        time += move_speed

        bottom_text = bottom_font.render("Press Enter to Continue", True, (92, 95, 119))
        screen.blit(
            bottom_text,
            (
                WIDTH - bottom_text.get_width() - 10,
                HEIGHT - bottom_text.get_height() - 10,
            ),
        )
        bottom_text = bottom_font.render("Press Shift to go back", True, (92, 95, 119))
        screen.blit(bottom_text, (10, HEIGHT - bottom_text.get_height() - 10))

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    return
                if e.key in (K_RSHIFT, K_LSHIFT):
                    return True
            if e.type == MOUSEMOTION and e.buttons[0]:
                rotation_angle_x = max(0, min(90, rotation_angle_x + e.rel[1] * 0.5))
                rotation_angle_y += e.rel[0] * 0.5
            if e.type == MOUSEWHEEL:
                spinner_speed = 2 if e.y > 0 else -2

        flip()
