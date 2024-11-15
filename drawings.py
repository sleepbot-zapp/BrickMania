from models import Brick
from models import Color
from pygame.draw import rect, circle
from pygame import Surface, SRCALPHA


def draw_bricks(bricks: Brick):
    for brick in bricks:
        brick.draw()


def draw_player(x, y, screen, player_width, player_height):
    rect(screen, Color.BLUE, (x, y, player_width, player_height), border_radius=10)


def draw_ball(x, y, screen, trail, ball_radius):
    FIXED_TRAIL_LENGTH = 10 
    FIXED_TRAIL_COLOR = (0, 156, 0)
    MAX_ALPHA = 50 
    trail.append((x, y))
    if len(trail) < FIXED_TRAIL_LENGTH:
        trail.pop(0)

    for i, (tx, ty) in enumerate(trail):
        alpha = MAX_ALPHA - int(MAX_ALPHA * (i / FIXED_TRAIL_LENGTH)) 
        color = (FIXED_TRAIL_COLOR[0], FIXED_TRAIL_COLOR[1], FIXED_TRAIL_COLOR[2], alpha)
        trail_surface = Surface((ball_radius * 2, ball_radius * 2), SRCALPHA)
        circle(trail_surface, color, (ball_radius, ball_radius), ball_radius)
        screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))

    circle(screen, FIXED_TRAIL_COLOR, (x, y), ball_radius)