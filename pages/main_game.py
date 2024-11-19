from helpers import settings
import pygame
import time
from pages.loading_screen import loading_screen
from helpers.runner import runner
from helpers.constants import screen, WIDTH, HEIGHT, SCALE, brick_height, brick_width, clock, ball_speed_x, ball_speed_y, player_height, player_width, player_speed, ball_radius, track1, speed_increment, brick_speed, ball_trails, track2
from models import Color, SpecialBall
from pages.main_menu import main_menu
from helpers.game_control import create_new_bricks, pause_game, game_over, drop_powerup, show_score
from helpers.drawings import draw_ball, draw_bricks, draw_player
from random import randint, choice
from sys import exit

def main_game(font):#, mode=False
    data = settings.Settings.open()
    balls = [(randint(200, WIDTH // 2), randint(400, 500), choice((1, -1)) * ball_speed_x, ball_speed_y)]
    balls_crossed_line = [False]
    player_x = (WIDTH * SCALE - player_width) // 2
    player_y = HEIGHT * SCALE - player_height - 70
    score = 0
    bricks = create_new_bricks()
    powerups = []
    special_balls = []
    running = True
    last_move_time = time.time()
    inactivity_threshold = 5
    last_brick_move_time = time.time()
    last_special_ball_time = time.time()
    special_ball_time = 20
    last_x_key_time = time.time()
    random_destruction_interval = 60
    last_x_time = time.time()
    last_x_value = None

    while running:
        screen.fill(Color.BLACK)
        dt = clock.tick(60) / 1000
        current_time = time.time()

        if len(bricks) == 0:
            bricks = create_new_bricks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if current_time - last_move_time > inactivity_threshold:
            if player_x <= WIDTH // 2:
                player_x += 5 * player_speed * dt
            elif player_x > WIDTH // 2:
                player_x -= 5 * player_speed * dt
            last_move_time = current_time
        if (keys[pygame.K_p]) or (keys[pygame.K_p]) or (keys[pygame.K_SPACE]) or keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
            pause_game(font)

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x > 10:
            player_x -= player_speed * dt
            last_move_time = current_time
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < WIDTH - player_width - 10:
            player_x += player_speed * dt
            last_move_time = current_time

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and current_time - last_special_ball_time > 19:
            dx = choice([-500, 500]) 
            dy = randint(-300, -120)
            special_balls.append(SpecialBall(player_x + player_width // 2, player_y - ball_radius, dx, dy))
            # if not mode:
            #     pygame.mixer.music.pause()
            #     track1.play()
            last_special_ball_time = current_time

        if keys[pygame.K_RSHIFT]:
            runner(main_menu, loading_screen, main_game, 1)

        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls):
            
            ball_x += ball_dx * dt
            ball_y += ball_dy * dt

            if last_x_value == ball_x:
                if current_time - last_x_time > 3:  
                    ball_dx = -ball_dx  
                    ball_x += ball_dx * dt
                    last_x_time = current_time  
            else:
                last_x_value = ball_x
                last_x_time = current_time  

            if ball_x <= ball_radius:
                ball_x = ball_radius + 1
                ball_dx = abs(ball_dx)
            elif ball_x >= WIDTH - ball_radius:
                ball_x = WIDTH - ball_radius - 1
                ball_dx = -abs(ball_dx)

            if ball_y <= ball_radius:
                ball_y = ball_radius + 1
                ball_dy = abs(ball_dy)


            if ball_y >= HEIGHT - 60 - ball_radius and not balls_crossed_line[i]:
                balls_crossed_line[i] = True

            paddle_center_x = player_x + player_width / 2
            dx_from_center = (ball_x - paddle_center_x) / (player_width / 2)
            if player_x - ball_radius < ball_x < player_x + player_width + ball_radius and player_y < ball_y + ball_radius < player_y + player_height:
                ball_dx = ball_speed_x * dx_from_center * 1.2
                if ball_dx > 0:
                    ball_dx += 50
                else:
                    ball_dx -= 50
                ball_dy = -abs(ball_dy)
                ball_y = player_y - ball_radius

            balls[i] = (ball_x, ball_y, ball_dx, ball_dy)

        if all(balls_crossed_line):
            game_over(score, settings=data) #mode=mode
            return

        if current_time - last_brick_move_time > 1:
            for brick in bricks:
                brick.y += brick_speed * dt
                if brick.y + brick_height >= HEIGHT:
                    game_over(score, settings=data) #mode=mode
                    return
            last_brick_move_time = current_time

        bricks_to_remove = []
        for brick in bricks:
            for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls):
                if brick.x < ball_x < brick.x + brick_width and brick.y < ball_y < brick.y + brick_height:
                    bricks_to_remove.append(brick)
                    score += 10
                    powerup = drop_powerup(brick.x, brick.y, powerups)
                    if powerup:
                        powerups.append(powerup)
                    balls[i] = (ball_x, ball_y, ball_dx, -ball_dy)

            for special_ball in special_balls:
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
                # if not mode:
                #     pygame.mixer.music.pause()
                #     track2.play()
                for _ in range(5):
                    if bricks:
                        random_brick = choice(bricks)
                        bricks.remove(random_brick)
                        score += 20
                last_x_key_time = current_time

        for powerup in powerups:
            if powerup.y < HEIGHT - 70:
                powerup.move(dt)
                powerup.draw(screen)

            if player_x < powerup.x + powerup.width and player_x + player_width > powerup.x and player_y < powerup.y + powerup.height and player_y + player_height > powerup.y:
                powerups.remove(powerup)
                if powerup.type == "extra_ball":
                    balls.append((WIDTH // 2, HEIGHT // 2, choice((1, -1)) * ball_speed_x, ball_speed_y))
                    balls_crossed_line.append(False)

        for special_ball in special_balls:
            if special_ball.y < HEIGHT - 70:  
                special_ball.move(ball_radius, WIDTH, dt)
                special_ball.draw(screen, ball_radius)

            if special_ball.x < 0 or special_ball.x > WIDTH or special_ball.y < 0 or special_ball.y > HEIGHT:
                special_balls.remove(special_ball)

        draw_bricks([brick for brick in bricks], screen, brick_width, brick_height)  
        draw_player(player_x, player_y, screen, player_width, player_height)

        for i, (ball_x, ball_y, _, _) in enumerate(balls):
            if ball_y < HEIGHT - 60:  
                draw_ball(ball_x, ball_y, i, ball_radius, ball_trails, screen)

        show_score(score, font)


        if current_time - last_special_ball_time > special_ball_time - 1:
            special_ball_text = font.render("Special Ball Ready (UP)", True, Color.GREEN)
        else:
            remaining_time = max(0, special_ball_time - (current_time - last_special_ball_time))
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

        pygame.draw.line(screen, Color.WHITE, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 2)

        pygame.display.flip()

        # if not mode:
        #     if not special_balls or current_time - last_special_ball_time >= 2:
        #         track1.stop()
        #         pygame.mixer.music.unpause()
        #     if current_time - last_x_key_time >= 3:
        #         track2.stop()
        #         pygame.mixer.music.unpause()