import pygame
import settings
from constants import track3, screen, SCALE, WIDTH, HEIGHT, clock, brick_cols, brick_height, brick_width, brick_rows
import time
from models import Color, PowerUp, Brick
from random import random
from pygame import QUIT, quit, K_q, K_RETURN, KEYDOWN, event, font, mixer
from pygame.display import flip
import sys

def pause_game():
    paused = True
    pause_text = font.render("Game Paused. Press 'P' to Resume.", True, Color.WHITE)
    dim_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim_surface.fill((0, 0, 0, 180))
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_SPACE, pygame.K_0):
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()                    
        
        screen.blit(dim_surface, (0, 0))
        screen.blit(pause_text, ((WIDTH - pause_text.get_width()) // 2, HEIGHT // 2))
        pygame.display.flip()

        clock.tick(10)



def game_over(score, settings: settings.Settings, type_=0, mode=0):
    if not mode:
        pygame.mixer.music.pause()
        track3.play()
        curr = time.time()
    screen.fill(Color.BLACK)
    font_for_game_over = pygame.font.SysFont(None, int(42 * SCALE))
    text = font_for_game_over.render("Game Over! Press ENTER to restart", True, Color.RED)
    highscore = settings.highscore
    text2 = font_for_game_over.render(f"High Score = {[score, highscore][highscore>score]}", True, [Color.GREEN, Color.YELLOW][highscore>score])
    text3 = font_for_game_over.render(f"Your Score = {score}", True, Color.BLUE)
    if highscore < score and type_==0:
        settings.highscore = score
        settings.flush()
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT // 2 - 40) * SCALE))
    screen.blit(text2, ((WIDTH // 2 - text2.get_width() / 2) * SCALE, (HEIGHT // 2) * SCALE))
    screen.blit(text3, ((WIDTH // 2 - text3.get_width() / 2) * SCALE, (HEIGHT // 2 + 40) * SCALE))
    pygame.display.flip()

    while True:
        if not mode and time.time() - curr > 2:
            if not mode:
                track3.stop()
                pygame.mixer.music.unpause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()



def drop_powerup(brick_x, brick_y, powerups):
    powerup_type = random.choice(["extra_ball",])
    if len(powerups) < 2 and random.random() < 0.1:
        return PowerUp(brick_x, brick_y, powerup_type, SCALE)
    return None

def create_new_bricks():
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks


def show_score(score):
    text = font.render(f"Score: {score}", True, Color.RED)
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT - 30) * SCALE))