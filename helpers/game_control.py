import helpers.settings as settings
from helpers.constants import (
    screen,
    SCALE,
    WIDTH,
    HEIGHT,
    clock,
    brick_cols,
    brick_height,
    brick_width,
    brick_rows,
    bottom_font,
)
from models import Color, PowerUp, Brick
from random import random, choice
from pygame import (
    Surface,
    SRCALPHA,
    QUIT,
    quit,
    K_q,
    K_RETURN,
    K_p,
    K_SPACE,
    KEYDOWN,
    event,
    font,
    K_RSHIFT,
    K_RCTRL,
    K_LCTRL,
)
from pygame.display import flip
import sys


def pause_game(font):
    paused = True
    pause_text = font.render("Game Paused. Press 'P' to Resume.", True, Color().WHITE)
    dim_surface = Surface((WIDTH, HEIGHT), SRCALPHA)
    dim_surface.fill((0, 0, 0, 180))
    while paused:
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key in (K_p, K_SPACE, K_RCTRL):
                    paused = False
                if e.key == K_q:
                    quit()
                    sys.exit()

        screen.blit(dim_surface, (0, 0))
        screen.blit(pause_text, ((WIDTH - pause_text.get_width()) // 2, HEIGHT // 2))
        flip()

        clock.tick(10)


def game_over(score, settings: settings.Settings):
    # if not mode:
    #     music.pause()
    #     track3.play()
    #     curr = time.time()
    screen.fill(Color().BLACK)
    font_for_game_over = font.SysFont(None, int(42 * SCALE))
    text = font_for_game_over.render(
        "Game Over! Press ENTER to restart", True, Color().RED
    )
    highscore = settings.highscore
    text2 = font_for_game_over.render(
        f"High Score = {[score, highscore][highscore>score]}",
        True,
        [Color().GREEN, Color().YELLOW][highscore > score],
    )
    text3 = font_for_game_over.render(f"Your Score = {score}", True, Color().BLUE)
    if highscore < score:
        settings.highscore = score
        settings.flush()
    screen.blit(
        text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT // 2 - 40) * SCALE)
    )
    screen.blit(
        text2, ((WIDTH // 2 - text2.get_width() / 2) * SCALE, (HEIGHT // 2) * SCALE)
    )
    screen.blit(
        text3,
        ((WIDTH // 2 - text3.get_width() / 2) * SCALE, (HEIGHT // 2 + 40) * SCALE),
    )

    quit_text = bottom_font.render(
        "Press Shift to go to Main Window", True, Color().GREY
    )
    screen.blit(quit_text, (10, (HEIGHT - quit_text.get_height() - 10) * SCALE))
    flip()

    while True:
        # if not mode and time.time() - curr > 2:
        #     if not mode:
        #         track3.stop()
        #         music.unpause()
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    return False
                if e.key in (K_RSHIFT, K_LCTRL):
                    return True


def drop_powerup(brick_x, brick_y, powerups):
    powerup_type = choice(
        [
            "extra_ball",
        ]
    )
    if len(powerups) < 2 and random() < 0.1:
        return PowerUp(brick_x, brick_y, powerup_type, SCALE)
    return None


def create_new_bricks():
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks


def show_score(score, font):
    text = font.render(f"Score: {score}", True, Color().RED)
    screen.blit(
        text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT - 30) * SCALE)
    )
