import pygame
import random
import sys

pygame.init()

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1) 

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICKMANIA")

WHITE = (255, 255, 255)
RED = (255, 30, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

player_width = 50
player_height = 20
player_speed = 15

brick_width = 5
brick_height = 20
brick_speed = 5

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=50)

def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, RED, (brick[0], brick[1], brick_width, brick_height))

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over(score):
    text = font.render("Game Over! Press SPACE to restart", True, WHITE)
    highscore = int(open("highscore.txt").read())
    text2 = font.render(f"High Score = {[score, highscore][highscore>score]}", True, WHITE)
    if highscore < score:
        with open('highscore.txt', 'w') as f:
            f.write(str(score))
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))
    screen.blit(text2, (WIDTH // 2 - 120, HEIGHT // 2 + 40))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def main_game():
    player_x = (WIDTH - player_width) // 2
    player_y = HEIGHT - player_height - 10
    score = 0
    bricks = []

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        player_x += random.choice((-1, 1)) if 0 < player_x < WIDTH else 0

        if random.randint(1, 20) == 1:
            for _ in range(random.randint(2, 5)):
                brick_x = random.randint(0, WIDTH - brick_width)
                bricks.append([brick_x, 0])

        for brick in bricks[:]:
            brick[1] += brick_speed
            if (
                brick[1] + brick_height >= player_y and
                brick[0] + brick_width >= player_x and
                brick[0] <= player_x + player_width
            ):
                game_over(score)
                return
            if brick[1] > HEIGHT:
                bricks.remove(brick)
                score += 1

        draw_player(player_x, player_y)
        draw_bricks(bricks)
        show_score(score)

        pygame.display.flip()
        clock.tick(30)

while True:
    main_game()
