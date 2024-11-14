import os
import pygame
import random
import sys
import time
import os

os.chdir(os.path.dirname(__file__))

pygame.init()

pygame.mixer.music.load("./music.mp3")
track1 = pygame.mixer.Sound("./music1.mp3")
track2 = pygame.mixer.Sound("./music2.mp3")
track3 = pygame.mixer.Sound("./music3.mp3")
pygame.mixer.music.play(-1)

SCALE = 1
WIDTH, HEIGHT = int(800 * SCALE), int(600 * SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICKMANIA")

WHITE = (255, 255, 255)
RED = (255, 30, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

player_width = 100 * SCALE
player_height = 20 * SCALE
player_speed = 15 * SCALE

ball_radius = 10 * SCALE
ball_speed_x, ball_speed_y = 5 * SCALE, -5 * SCALE

brick_width = int(80 * SCALE)
brick_height = 20 * SCALE
brick_speed = 10 * SCALE
brick_rows = 6
brick_cols = WIDTH // brick_width

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, int(25 * SCALE))

trail = []
trail_length = 10

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.width = 40 * SCALE
        self.height = 20 * SCALE
        self.type = type
        self.color = {"extra_ball": GREEN}[type]
        self.fall_speed = 2 * SCALE

    def move(self):
        self.y += self.fall_speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice([RED, BLUE, GREEN, YELLOW])

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, brick_width, brick_height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, brick_width, brick_height), 2)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=10)

def draw_ball(x, y):
    FIXED_TRAIL_LENGTH = 10 
    FIXED_TRAIL_COLOR = (0, 156, 0)
    MAX_ALPHA = 50 
    trail.append((x, y))
    if len(trail) < FIXED_TRAIL_LENGTH:
        trail.pop(0)

    for i, (tx, ty) in enumerate(trail):
        alpha = MAX_ALPHA - int(MAX_ALPHA * (i / FIXED_TRAIL_LENGTH)) 
        color = (FIXED_TRAIL_COLOR[0], FIXED_TRAIL_COLOR[1], FIXED_TRAIL_COLOR[2], alpha)
        trail_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, color, (ball_radius, ball_radius), ball_radius)
        screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))

    pygame.draw.circle(screen, FIXED_TRAIL_COLOR, (x, y), ball_radius)


def draw_bricks(bricks):
    for brick in bricks:
        brick.draw()

def show_score(score):
    text = font.render(f"Score: {score}", True, RED)
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT - 40) * SCALE))

def game_over(score):
    pygame.mixer.music.pause()
    track3.play()
    font_for_game_over = pygame.font.SysFont(None, int(42 * SCALE))
    text = font_for_game_over.render("Game Over! Press SPACE to restart", True, RED)
    # highscore = int(open("./brickmania/highscore.txt").read())
    highscore = 0
    text2 = font_for_game_over.render(f"High Score = {[score, highscore][highscore>score]}", True, [GREEN, YELLOW][highscore>score])
    text3 = font_for_game_over.render(f"Your Score = {score}", True, BLUE)
    if highscore < score:
        ...
        # with open('./highscore.txt', 'w') as f:
        #     f.write(str(score))
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT // 2 - 40) * SCALE))
    screen.blit(text2, ((WIDTH // 2 - text2.get_width() / 2) * SCALE, (HEIGHT // 2) * SCALE))
    screen.blit(text3, ((WIDTH // 2 - text3.get_width() / 2) * SCALE, (HEIGHT // 2 + 40) * SCALE))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                track2.stop()
                pygame.mixer.music.unpause()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

def drop_powerup(brick_x, brick_y, powerups):
    powerup_type = random.choice(["extra_ball",])
    if len(powerups) < 2 and random.random() < 0.2:
        return PowerUp(brick_x, brick_y, powerup_type)
    return None


def create_new_bricks():
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks

class SpecialBall:
    def __init__(self, x, y, dx, dy, expiration_time):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.expiration_time = expiration_time

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= ball_radius or self.x >= WIDTH - ball_radius:
            self.dx = -self.dx

        if self.y <= ball_radius:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), ball_radius)

speed_increment = 1.0001

def main_game():
    player_width = 100 * SCALE
    player_height = 20 * SCALE
    player_speed = 15 * SCALE

    player_x = (WIDTH * SCALE - player_width) // 2
    player_y = HEIGHT * SCALE - player_height - 70

    balls = [(random.randint(200, WIDTH // 2), random.randint(400, 500), ball_speed_x, ball_speed_y)]
    balls_crossed_line = [False]

    score = 0
    bricks = create_new_bricks()
    powerups = []
    special_balls = []
    running = True

    last_move_time = time.time()
    inactivity_threshold = 2

    last_brick_move_time = time.time()
    brick_move_speed = 3

    last_special_ball_time = time.time()

    last_x_key_time = time.time()
    random_destruction_interval = 60

    while running:
        screen.fill(BLACK)
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

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x > 10:
            player_x -= player_speed
            last_move_time = current_time
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < WIDTH - player_width - 10:
            player_x += player_speed
            last_move_time = current_time

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and current_time - last_special_ball_time > 19:
            dx = random.choice([-8, 8]) 
            dy = random.randint(-5, -2)
            special_balls.append(SpecialBall(player_x + player_width // 2, player_y - ball_radius, dx, dy, current_time + 3))
            pygame.mixer.music.pause()
            track1.play()
            last_special_ball_time = current_time

        if keys[pygame.K_RSHIFT]:
            return

        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            balls[i] = (ball_x, ball_y, ball_dx * speed_increment, ball_dy * speed_increment)

        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            ball_x += ball_dx
            ball_y += ball_dy

            if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
                ball_dx = -ball_dx

            if ball_y <= ball_radius:
                ball_dy = -ball_dy

            if ball_y >= HEIGHT - 60 - ball_radius and not balls_crossed_line[i]:
                balls_crossed_line[i] = True

            if player_x < ball_x < player_x + player_width and player_y < ball_y + ball_radius < player_y + player_height:
                center_x = player_x + player_width / 2
                hit_position = (ball_x - center_x) / (player_width / 2)
                ball_dx = ball_speed_x * hit_position
                ball_dy = -abs(ball_dy)
                ball_y = player_y - ball_radius

            balls[i] = (ball_x, ball_y, ball_dx, ball_dy)

        if all(balls_crossed_line):
            game_over(score)
            return

        if current_time - last_brick_move_time > 1:
            for brick in bricks:
                brick.y += brick_move_speed
                if brick.y + brick_height >= HEIGHT:
                    game_over(score)
                    return
            last_brick_move_time = current_time

        bricks_to_remove = []
        for brick in bricks:
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
                pygame.mixer.music.pause()
                track2.play()
                for _ in range(5):
                    if bricks:
                        random_brick = random.choice(bricks)
                        bricks.remove(random_brick)
                        score += 20
                last_x_key_time = current_time

        for powerup in powerups[:]:
            powerup.move()
            powerup.draw()

            if player_x < powerup.x + powerup.width and player_x + player_width > powerup.x and player_y < powerup.y + powerup.height and player_y + player_height > powerup.y:
                powerups.remove(powerup)
                if powerup.type == "extra_ball":
                    balls.append((WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y))
                    balls_crossed_line.append(False)

        for special_ball in special_balls[:]:
            special_ball.move()
            special_ball.draw()

            if special_ball.x < 0 or special_ball.x > WIDTH or special_ball.y < 0 or special_ball.y > HEIGHT:
                special_balls.remove(special_ball)

        draw_bricks(bricks)
        draw_player(player_x, player_y)
        for ball_x, ball_y, _, _ in balls:
            draw_ball(ball_x, ball_y)

        show_score(score)

        if current_time - last_special_ball_time > 19:
            special_ball_text = font.render("Special Ball Ready (UP)", True, GREEN)
        else:
            remaining_time = max(0, 20 - (current_time - last_special_ball_time))
            special_ball_text = font.render(f"Special Ball in {int(remaining_time)}s", True, WHITE)

        if current_time - last_x_key_time > random_destruction_interval - 1:
            countdown_text = font.render("Brick Destruction Ready (DOWN)", True, GREEN)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width() - 20) * SCALE, (HEIGHT - 40) * SCALE))
        else:
            time_until_destruction = max(0, random_destruction_interval - (current_time - last_x_key_time))
            countdown_text = font.render(f"Brick Destruction in {int(time_until_destruction)}s", True, WHITE)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width() - 20) * SCALE, (HEIGHT - 40) * SCALE))

        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)
        screen.blit(special_ball_text, (20 * SCALE, (HEIGHT - 40) * SCALE))

        pygame.display.flip()

        if not special_balls or current_time - last_special_ball_time >= 2:
            track1.stop()
            pygame.mixer.music.unpause()

        if current_time - last_x_key_time >= 5:
            track2.stop()
            pygame.mixer.music.unpause()


def main_game2():
    # Initialize variables as before
    last_brick_move_time = time.time()
    brick_move_speed = 3
    player_width = 100 * SCALE
    player_height = 20 * SCALE
    player_speed = 50 * SCALE  # Player speed remains constant
    player_x = (WIDTH * SCALE - player_width) // 2
    player_y = HEIGHT * SCALE - player_height - 70
    balls = [(random.randint(200, WIDTH // 2), random.randint(400, 500), ball_speed_x, ball_speed_y)]
    balls_crossed_line = [False] * len(balls)
    score = 0
    bricks = create_new_bricks()
    powerups = []
    special_balls = []
    running = True

    last_special_ball_time = time.time()
    last_x_time = time.time()
    random_destruction_interval = 60
    last_ball_missed_time = 0
    ball_miss_chance = 0.2
    game_over = False
    game_over_start_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        current_time = time.time()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RSHIFT]:
            return

        if current_time - last_brick_move_time > 1:
            for brick in bricks:
                brick.y += brick_move_speed
                if brick.y + brick_height >= HEIGHT:
                    game_over(score)
                    return
            last_brick_move_time = current_time

        # If game is over, show "Game Over" message for 5 seconds, then reset
        if game_over:
            if current_time - game_over_start_time < 5:
                ...
                # show_game_over()  # Display "Game Over" message
            else:
                # Reset game variables after 5 seconds
                balls = [(random.randint(200, WIDTH // 2), random.randint(400, 500), ball_speed_x, ball_speed_y)]
                balls_crossed_line = [False] * len(balls)
                bricks = create_new_bricks()
                powerups = []
                score = 0
                game_over = False
            pygame.display.flip()
            continue

        clock.tick(60)  # Keep the frame rate constant

        if len(bricks) == 0:
            bricks = create_new_bricks()

        # Draw the horizontal line 10px below the player paddle
        line_y = player_y + player_height + 10
        pygame.draw.line(screen, WHITE, (0, line_y), (WIDTH, line_y), 2)

        # Adjust paddle position based on multiple balls
        if balls:
            avg_ball_x = sum(ball[0] for ball in balls) / len(balls)
            if player_x + player_width / 2 < avg_ball_x:
                player_x += min(player_speed, avg_ball_x - (player_x + player_width / 2))
            elif player_x + player_width / 2 > avg_ball_x:
                player_x -= min(player_speed, (player_x + player_width / 2) - avg_ball_x)

        # Automatic special ball shot every 20 seconds
        if current_time - last_special_ball_time > 20:
            dx = random.choice([-8, 8]) 
            dy = random.randint(-5, -2)
            # Add expiration_time to each special ball
            special_balls.append(SpecialBall(player_x + player_width // 2, player_y - ball_radius, dx, dy, current_time + 3))
            pygame.mixer.music.pause()
            track1.play()
            last_special_ball_time = current_time

        if current_time - last_x_time > random_destruction_interval:
                pygame.mixer.music.pause()
                track2.play()
                for _ in range(5):
                    if bricks:
                        random_brick = random.choice(bricks)
                        bricks.remove(random_brick)
                        score += 20
                last_x_time = current_time

        # Speed increment on each ball
        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            balls[i] = (ball_x, ball_y, ball_dx * speed_increment, ball_dy * speed_increment)

        # Ball movement and boundary collision
        balls_to_remove = []  # List to track balls that should be removed
        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            ball_x += ball_dx
            ball_y += ball_dy

            if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
                ball_dx = -ball_dx
            if ball_y <= ball_radius:
                ball_dy = -ball_dy

            # Check if ball falls below the line
            if ball_y > line_y:
                balls_to_remove.append(i)
                continue

            # Paddle collision logic with slight randomness in bounce angle
            if player_x < ball_x < player_x + player_width and player_y < ball_y + ball_radius < player_y + player_height:
                center_x = player_x + player_width / 2
                hit_position = (ball_x - center_x) / (player_width / 2)
                ball_dx = ball_speed_x * (hit_position + random.uniform(-0.1, 0.1))
                ball_dy = -abs(ball_dy)
                ball_y = player_y - ball_radius

            balls[i] = (ball_x, ball_y, ball_dx, ball_dy)

        # After the loop, remove all balls that should be removed
        for i in reversed(balls_to_remove):
            balls.pop(i)
            balls_crossed_line.pop(i)

        # Check if all balls have fallen below the line
        if len(balls) == 0:
            game_over = True
            game_over_start_time = current_time

        # Brick collision detection for each ball
        bricks_to_remove = []
        for brick in bricks:
            for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
                if brick.x < ball_x < brick.x + brick_width and brick.y < ball_y < brick.y + brick_height:
                    bricks_to_remove.append(brick)
                    score += 10
                    balls[i] = (ball_x, ball_y, ball_dx, -ball_dy)

                    # Chance to spawn a power-up at the broken brick's location
                    if random.random() < 0.3:
                        powerup_type = random.choice(["extra_ball"])
                        powerups.append(PowerUp(brick.x, brick.y, powerup_type))

        # Remove hit bricks
        for brick in bricks_to_remove:
            if brick in bricks:
                bricks.remove(brick)

        # Power-up movement and collision with paddle
        for powerup in powerups[:]:
            powerup.move()
            powerup.draw()
            if powerup.y > line_y:  # Remove power-up if it falls below the line
                powerups.remove(powerup)
            elif player_x < powerup.x < player_x + player_width and player_y < powerup.y < player_y + player_height:
                powerups.remove(powerup)
                if powerup.type == "extra_ball":
                    balls.append((WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y))
                    balls_crossed_line.append(False)

        # Special ball handling (movement and collision)
        for special_ball in special_balls[:]:
            special_ball.move()
            special_ball.draw()
            
            if special_ball.y >= HEIGHT - 10:  # Use expiration_time to check for removal
                special_balls.remove(special_ball)


            for brick in bricks:
                if brick.x < special_ball.x < brick.x + brick_width and brick.y < special_ball.y < brick.y + brick_height:
                    bricks.remove(brick)
                    score += 20  # Reward for destroying a brick with a special ball
                    break  # Special ball is consumed on brick hit

        # Draw bricks, special balls, and score
        draw_bricks(bricks)
        draw_player(player_x, player_y)
        for ball_x, ball_y, _, _ in balls:
            draw_ball(ball_x, ball_y)
        for special_ball in special_balls:
            special_ball.draw()  # Draw special balls separately
        show_score(score)


        if current_time - last_special_ball_time > 19:
            special_ball_text = font.render("Special Ball Ready (UP)", True, GREEN)
        else:
            remaining_time = max(0, 20 - (current_time - last_special_ball_time))
            special_ball_text = font.render(f"Special Ball in {int(remaining_time)}s", True, WHITE)

        if current_time - last_x_time > random_destruction_interval - 1:
            countdown_text = font.render("Brick Destruction Ready (DOWN)", True, GREEN)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() * SCALE // 2 + 250 * SCALE, HEIGHT - 40 * SCALE))
        else:
            time_until_destruction = max(0, random_destruction_interval - (current_time - last_x_time))
            countdown_text = font.render(f"Brick Destruction in {int(time_until_destruction)}s", True, WHITE)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() * SCALE // 2 + 200 * SCALE, HEIGHT - 40 * SCALE))

        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)
        screen.blit(special_ball_text, (WIDTH // 2 - special_ball_text.get_width() * SCALE // 2 - 250 * SCALE, HEIGHT - 40 * SCALE))

        pygame.display.flip()

        if not special_balls or current_time - last_special_ball_time >= 2:
            track1.stop()
            pygame.mixer.music.unpause()

        if current_time - last_x_time >= 5:
            track2.stop()
            pygame.mixer.music.unpause()




class FallingTile:
    def __init__(self):
        self.width = brick_width
        self.height = brick_height
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.randint(2, 7) * SCALE
        self.color = random.choice([RED, BLUE, GREEN])

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH - self.width) 

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

def main_menu():
    title_font = pygame.font.SysFont(None, int(72 * SCALE))
    menu_font = pygame.font.SysFont(None, int(48 * SCALE))

    tiles = [FallingTile() for _ in range(20)]

    options = ["Main Game", "Demo Game"]
    selected_option = 0  # Track the currently selected option

    while True:
        screen.fill(BLACK)

        # Falling tiles effect
        for tile in tiles:
            tile.move()
            tile.draw()

        # Display title
        title_text = title_font.render("BRICKMANIA", True, YELLOW)
        screen.blit(title_text, ((WIDTH // 2 - title_text.get_width() // 2) * SCALE, (HEIGHT // 2 - 150) * SCALE))

        # Display options and highlight selected one
        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            option_text = menu_font.render(option, True, color)
            screen.blit(option_text, ((WIDTH // 2 - option_text.get_width() // 2) * SCALE,
                                      (HEIGHT // 2 + i * 60) * SCALE))

        # Instructions
        quit_text = menu_font.render("Press Q to Quit", True, WHITE)
        screen.blit(quit_text, ((WIDTH // 2 - quit_text.get_width() // 2) * SCALE, (HEIGHT // 2 + 150) * SCALE))

        pygame.display.flip()

        # Event handling for menu navigation and selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected_option
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)

if __name__ == "__main__":
    while True:
        selected_option = main_menu()
        
        if selected_option == 0:
            main_game()   # Start the Main Game
        elif selected_option == 1:
            main_game2()  # Start the Demo Game
