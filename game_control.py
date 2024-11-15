from models import Color, PowerUp, Brick
from random import random
from pygame import QUIT, quit, K_q, K_RETURN, KEYDOWN, event, font, mixer
from pygame.display import flip
from sys import exit


def game_over(
    score,
    screen,
    track2,
    track3,
    HEIGHT,
    WIDTH,
    scale,
    type_=0,
):
    mixer.music.pause()
    track3.play()
    screen.fill(Color.BLACK)
    font_for_game_over = font.SysFont(None, int(42 * scale))
    text = font_for_game_over.render(
        "Game Over! Press ENTER to restart", True, Color.RED
    )
    if type_ == 0:
        highscore = int(open("./highscore.txt").read())
        text2 = font_for_game_over.render(
            f"High Score = {[score, highscore][highscore>score]}",
            True,
            [Color.GREEN, Color.YELLOW][highscore > score],
        )
        text3 = font_for_game_over.render(f"Your Score = {score}", True, Color.BLUE)
        if highscore < score and type_ == 0:
            with open("./highscore.txt", "w") as f:
                f.write(str(score))
        screen.blit(
            text2, ((WIDTH // 2 - text2.get_width() / 2) * scale, (HEIGHT // 2) * scale)
        )
    screen.blit(
        text, ((WIDTH // 2 - text.get_width() / 2) * scale, (HEIGHT // 2 - 40) * scale)
    )
    screen.blit(
        font_for_game_over.render(
            f"{['Your', "Model"][type_]} Score = {score}", True, Color.BLUE
        ),
        ((WIDTH // 2 - text3.get_width() / 2) * scale, (HEIGHT // 2 + 40) * scale),
    )
    flip()

    while True:
        for eve in event.get():
            if eve.type == QUIT:
                game_quit()
            if eve.type == KEYDOWN:
                if event.key == K_RETURN:
                    track2.stop()
                    mixer.music.unpause()
                    return
                if eve.key == K_q:
                    game_quit()


def game_quit():
    quit()
    exit()


def drop_powerup(brick_x, brick_y, powerups):
    powerup_type = random(
        [
            "extra_ball",
        ]
    )
    if len(powerups) < 2 and random() < 0.2:
        return PowerUp(brick_x, brick_y, powerup_type)
    return None


def create_new_bricks(brick_cols, brick_rows, brick_width, brick_height):
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks


def show_score(score, screen, WIDTH, HEIGHT, scale):
    text = font.render(f"Score: {score}", True, Color.RED)
    screen.blit(
        text, ((WIDTH // 2 - text.get_width() / 2) * scale, (HEIGHT - 40) * scale)
    )
