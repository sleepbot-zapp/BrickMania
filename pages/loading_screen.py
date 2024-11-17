import pygame
import math
from random import choice
from pygame.font import SysFont
from pygame import KEYDOWN, K_q, K_LSHIFT, K_RSHIFT, K_RETURN, quit, QUIT, event, MOUSEMOTION
from pygame.draw import line
from pygame.display import flip
from sys import exit

# Ensure these are correctly imported from the right files
from helpers.constants import screen, WIDTH, HEIGHT, font, bottom_font, clock  # Check helpers/constants.py
from models import Color  # Check models.py

def loading_screen(func1, func2):
    # Spinner parameters
    radius = 30
    spinner_segments = 12
    angle_per_segment = 360 / spinner_segments
    spinner_speed = 2  # Default rotation speed
    angle = 0  # Initial rotation angle

    # Dynamic movement parameters
    spinner_center = [WIDTH // 2, HEIGHT // 2]  # Spinner starts at the center
    time = 0  # Time counter for dynamic movement
    move_speed = 2  # Speed of spinner movement

    tip_font = SysFont("Arial", 24)
    tips = [
        "Use the paddle to deflect the ball!",
        "Hit bricks for power-ups!",
        "Press UP to launch a special ball!",
        "Stay active to avoid the paddle drifting!",
        "Press DOWN to destroy 5 random bricks!"
    ]
    tip = choice(tips)

    # Rotation angles for 3D effect
    rotation_angle_x = 30  # Tilt angle (up-down)
    rotation_angle_y = 45  # Spin angle (left-right)

    while True:
        screen.fill(Color.BLACK)
        clock.tick(60)

        # Display loading text
        loading_text = font.render("BrickMania", True, Color.WHITE)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - 123))

        # Display tip
        tip_text = tip_font.render("Tip: " + tip, True, Color.WHITE)
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT // 2 + 123))

        # Update spinner position (weird projectile motion)
        spinner_center[0] = WIDTH // 2 + 100 * math.sin(time * 0.02)  # X position follows a sine wave
        spinner_center[1] = HEIGHT // 2 + 50 * math.cos(time * 0.03)  # Y position follows a cosine wave

        # Scale spinner size based on position
        scale_factor_x = 1 + (spinner_center[0] - WIDTH // 2) / WIDTH  # Grow along X-axis
        scale_factor_y = 1 - (spinner_center[1] - HEIGHT // 2) / HEIGHT  # Shrink along Y-axis
        scale_factor = max(0.5, min(2, scale_factor_x * scale_factor_y))  # Clamp scale factor

        # Spinner center for current frame
        current_center = spinner_center

        # 3D Rotation Transformations
        def rotate_3d(x, y, z, angle_x, angle_y):
            """Rotate a 2D spinner in 3D space."""
            # Rotate around X-axis (up-down tilt)
            new_y = y * math.cos(math.radians(angle_x)) - z * math.sin(math.radians(angle_x))
            new_z = y * math.sin(math.radians(angle_x)) + z * math.cos(math.radians(angle_x))
            y, z = new_y, new_z

            # Rotate around Y-axis (left-right spin)
            new_x = x * math.cos(math.radians(angle_y)) + z * math.sin(math.radians(angle_y))
            new_z = -x * math.sin(math.radians(angle_y)) + z * math.cos(math.radians(angle_y))
            x, z = new_x, new_z

            return x, y, z

        # Draw spinner
        for i in range(spinner_segments):
            segment_angle_start = angle + (i * angle_per_segment)
            segment_angle_end = segment_angle_start + angle_per_segment

            # Compute original spinner coordinates
            x1 = radius * scale_factor * func1(math.cos(math.radians(segment_angle_start)))
            y1 = radius * scale_factor * func1(math.sin(math.radians(segment_angle_start)))
            z1 = 0  # Spinner lies in the XY plane (z = 0)

            x2 = radius * scale_factor * func2(math.cos(math.radians(segment_angle_end)))
            y2 = radius * scale_factor * func2(math.sin(math.radians(segment_angle_end)))
            z2 = 0  # Spinner lies in the XY plane (z = 0)

            # Apply 3D rotation
            start_x1, start_y1, start_z1 = rotate_3d(x1, y1, z1, rotation_angle_x, rotation_angle_y)
            end_x1, end_y1, end_z1 = rotate_3d(-x1, -y1, z1, rotation_angle_x, rotation_angle_y)
            start_x2, start_y2, start_z2 = rotate_3d(x2, y2, z2, rotation_angle_x, rotation_angle_y)
            end_x2, end_y2, end_z2 = rotate_3d(-x2, -y2, z2, rotation_angle_x, rotation_angle_y)

            # Project the 3D coordinates into 2D screen space
            start_x1 += current_center[0]
            start_y1 += current_center[1]
            end_x1 += current_center[0]
            end_y1 += current_center[1]
            start_x2 += current_center[0]
            start_y2 += current_center[1]
            end_x2 += current_center[0]
            end_y2 += current_center[1]

            # Draw lines
            line(screen, Color.BLUE, (end_x1, end_y1), (end_x2, end_y2), 3)
            line(screen, Color.RED, (start_x1, start_y1), (start_x2, start_y2), 3)

        # Update spinner angle and time
        angle += spinner_speed
        time += move_speed

        # Display bottom text
        bottom_text = bottom_font.render("Press Enter to Continue", True, (92, 95, 119))
        screen.blit(bottom_text, (WIDTH - bottom_text.get_width() - 10, HEIGHT - bottom_text.get_height() - 10))
        bottom_text = bottom_font.render("Press Shift to go back ", True, (92, 95, 119))
        screen.blit(bottom_text, (10, HEIGHT - bottom_text.get_height() - 10))

        # Handle events
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    return
                if e.key == K_q:
                    quit()
                    exit()
                if e.key in (K_RSHIFT, K_LSHIFT):
                    return
            if e.type == MOUSEMOTION:
                if e.buttons[0]:  # Left mouse button held down
                    rotation_angle_x = max(0, min(90, rotation_angle_x + e.rel[1] * 0.5))  # Tilt (up-down)
                    rotation_angle_y += e.rel[0] * 0.5  # Spin (left-right)

        # Update display
        flip()
