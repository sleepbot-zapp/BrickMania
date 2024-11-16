from os import chdir
from os.path import dirname
import pygame
import random
import sys
import time
import settings
from models import PowerUp, Brick, SpecialBall, Color
from drawings import draw_player, draw_bricks, draw_ball
from runner import runner
from main_menu import main_menu
from loading_screen import loading_screen
from constants import *


chdir(dirname(__file__))

pygame.init()

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


def show_score(score):
    text = font.render(f"Score: {score}", True, Color.RED)
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT - 30) * SCALE))

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


def main_game(mode=False):
    player_width = 100 * SCALE
    player_height = 20 * SCALE
    player_speed = 15 * SCALE
    data = settings.Settings.open()
    player_x = (WIDTH * SCALE - player_width) // 2
    player_y = HEIGHT * SCALE - player_height - 70
    balls = [(random.randint(200, WIDTH // 2), random.randint(400, 500), random.choice((1, -1)) * 5 * SCALE, ball_speed_y)]
    balls_crossed_line = [False]

    score = 0
    bricks = create_new_bricks()
    powerups = []
    special_balls = []
    running = True

    last_move_time = time.time()
    inactivity_threshold = 5

    last_brick_move_time = time.time()
    brick_move_speed = 3

    last_special_ball_time = time.time()

    last_x_key_time = time.time()
    random_destruction_interval = 60

    last_x_time = time.time()
    last_x_value = None


    while running:
        screen.fill(Color.BLACK)
        clock.tick(60) / 1000
        current_time = time.time()

        if len(bricks) == 0:
            bricks = create_new_bricks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        keys = pygame.key.get_pressed()
        if current_time - last_move_time > inactivity_threshold:
            if player_x <= WIDTH // 2:
                player_x += 5 * player_speed
            elif player_x > WIDTH // 2:
                player_x -= 5 * player_speed
            last_move_time = current_time
        if (keys[pygame.K_p]) or (keys[pygame.K_p]) or (keys[pygame.K_SPACE]) or (keys[pygame.K_0]):
                pause_game()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x > 10:
            player_x -= player_speed
            last_move_time = current_time
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < WIDTH - player_width - 10:
            player_x += player_speed
            last_move_time = current_time

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and current_time - last_special_ball_time > 19:
            dx = random.choice([-8, 8]) 
            dy = random.randint(-5, -2)
            special_balls.append(SpecialBall(player_x + player_width // 2, player_y - ball_radius, dx, dy))
            if not mode:
                pygame.mixer.music.pause()
                track1.play()
            last_special_ball_time = current_time

        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            runner(main_menu, loading_screen, main_game, 1)

        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            balls[i] = (ball_x, ball_y, ball_dx * speed_increment, ball_dy * speed_increment)

        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            
            ball_x += ball_dx
            ball_y += ball_dy

            if last_x_value == ball_x:
                if current_time - last_x_time > 3:  
                    ball_dx = -ball_dx  
                    ball_x += ball_dx  
                    last_x_time = current_time  
            else:
                last_x_value = ball_x
                last_x_time = current_time  
      
            if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
                ball_dx = -ball_dx  

            if ball_y <= ball_radius:
                ball_dy = -ball_dy

            if ball_y >= HEIGHT - 60 - ball_radius and not balls_crossed_line[i]:
                balls_crossed_line[i] = True

            paddle_center_x = player_x + player_width / 2
            dx_from_center = (ball_x - paddle_center_x) / (player_width / 2)
            if player_x - ball_radius < ball_x < player_x + player_width + ball_radius and player_y < ball_y + ball_radius < player_y + player_height:
                ball_dx = ball_speed_x * dx_from_center
                ball_dy = -abs(ball_dy)
                ball_y = player_y - ball_radius

            balls[i] = (ball_x, ball_y, ball_dx, ball_dy)

        if all(balls_crossed_line):
            game_over(score, mode=mode, settings=data)
            return

        if current_time - last_brick_move_time > 1:
            for brick in bricks[:]:
                brick.y += brick_move_speed
                if brick.y + brick_height >= HEIGHT:
                    game_over(score, mode=mode, settings=data)
                    return
            last_brick_move_time = current_time

        bricks_to_remove = []
        for brick in bricks[:]:
            for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
                if brick.x < ball_x < brick.x + brick_width and brick.y < ball_y < brick.y + brick_height:
                    bricks_to_remove.append(brick)
                    score += 10
                    powerup = drop_powerup(brick.x, brick.y, powerups)
                    if powerup:
                        powerups.append(powerup)
                    balls[i] = (ball_x, ball_y, ball_dx, -ball_dy)

            for special_ball in special_balls[:]:
                if brick.x < special_ball.x < brick.x + brick_width and brick.y < special_ball.y < brick.y + brick_height:
                    bricks_to_remove.append(brick)
                    score += 10
                    powerup = drop_powerup(brick.x, brick.y, powerups)
                    if powerup:
                        powerups.append(powerup)

        for brick in bricks_to_remove:
            if brick in bricks:
                bricks.remove(brick)

        if current_time - last_x_key_time > random_destruction_interval - 1:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if not mode:
                    pygame.mixer.music.pause()
                    track2.play()
                for _ in range(5):
                    if bricks:
                        random_brick = random.choice(bricks)
                        bricks.remove(random_brick)
                        score += 20
                last_x_key_time = current_time

        for powerup in powerups[:]:
            if powerup.y < HEIGHT - 70:
                powerup.move()
                powerup.draw(screen)

            if player_x < powerup.x + powerup.width and player_x + player_width > powerup.x and player_y < powerup.y + powerup.height and player_y + player_height > powerup.y:
                powerups.remove(powerup)
                if powerup.type == "extra_ball":
                    balls.append((WIDTH // 2, HEIGHT // 2, random.choice((1, -1)) * 5 * SCALE, ball_speed_y))
                    balls_crossed_line.append(False)

        for special_ball in special_balls[:]:
            if special_ball.y < HEIGHT - 70:  
                special_ball.move(ball_radius, WIDTH)
                special_ball.draw(screen, ball_radius)

            if special_ball.x < 0 or special_ball.x > WIDTH or special_ball.y < 0 or special_ball.y > HEIGHT:
                special_balls.remove(special_ball)


        
        draw_bricks([brick for brick in bricks], screen, brick_width, brick_height)  
        draw_player(player_x, player_y, screen, player_width, player_height)

        for i, (ball_x, ball_y, _, _) in enumerate(balls):
            if ball_y < HEIGHT - 60:  
                draw_ball(ball_x, ball_y, i, ball_radius, ball_trails, screen)


        show_score(score)

        if current_time - last_special_ball_time > 19:
            special_ball_text = font.render("Special Ball Ready (UP)", True, Color.GREEN)
        else:
            remaining_time = max(0, 20 - (current_time - last_special_ball_time))
            special_ball_text = font.render(f"Special Ball in {int(remaining_time)}s", True, Color.WHITE)

        if current_time - last_x_key_time > random_destruction_interval - 1:
            countdown_text = font.render("Brick Destruction Ready (DOWN)", True, Color.GREEN)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width() - 20) * SCALE, (HEIGHT - 30) * SCALE))
        else:
            time_until_destruction = max(0, random_destruction_interval - (current_time - last_x_key_time))
            countdown_text = font.render(f"Brick Destruction in {int(time_until_destruction)}s", True, Color.WHITE)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width() - 20) * SCALE, (HEIGHT - 30) * SCALE))

        pygame.draw.line(screen, Color.WHITE, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 2)
        screen.blit(special_ball_text, (20 * SCALE, (HEIGHT - 30) * SCALE))

        pygame.display.flip()

        if not special_balls or current_time - last_special_ball_time >= 2:
            if not mode:
                track1.stop()
                pygame.mixer.music.unpause()

        if current_time - last_x_key_time >= 3:
            if not mode:
                track2.stop()
                pygame.mixer.music.unpause()



if __name__ == "__main__":
    pygame.mixer.music.load("./assets/music.mp3")
    is_paused=True
    runner(main_menu, loading_screen, main_game, is_paused, 1)