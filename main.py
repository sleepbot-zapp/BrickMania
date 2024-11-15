from os import chdir
from os.path import dirname
import pygame
import random
import sys
import time
import math
import settings

chdir(dirname(__file__))

pygame.init()

pygame.mixer.music.load("./assets/music.mp3")
track1 = pygame.mixer.Sound("./assets/music1.mp3")
track2 = pygame.mixer.Sound("./assets/music2.mp3")
track3 = pygame.mixer.Sound("./assets/music3.mp3")

SCALE = 1
WIDTH, HEIGHT = int(800 * SCALE), int(600 * SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICKMANIA")

WHITE = (205, 214, 244)	
RED = (150, 15, 57)	
BLUE = (30, 102, 245)	
BLACK = (17, 17, 27)	
YELLOW = (223, 142, 29)		
GREEN = (64, 160, 43)	

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


ball_trails = {}

def draw_ball(x, y, ball_id):
    FIXED_TRAIL_LENGTH = 10
    FIXED_TRAIL_COLOR = (0, 156, 0)
    MAX_ALPHA = 50

    
    if ball_id not in ball_trails:
        ball_trails[ball_id] = []

    
    trail = ball_trails[ball_id]
    trail.append((x, y))
    if len(trail) > FIXED_TRAIL_LENGTH:
        trail.pop(0)

    
    for i, (tx, ty) in enumerate(trail):
        alpha = MAX_ALPHA - int(MAX_ALPHA * (i / FIXED_TRAIL_LENGTH))
        color = (FIXED_TRAIL_COLOR[0], FIXED_TRAIL_COLOR[1], FIXED_TRAIL_COLOR[2], alpha)
        trail_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, color, (ball_radius, ball_radius), ball_radius)
        screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))

    
    pygame.draw.circle(screen, FIXED_TRAIL_COLOR, (x, y), ball_radius)

def pause_game():
    paused = True
    pause_text = font.render("Game Paused. Press 'P' to Resume.", True, WHITE)
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


def draw_bricks(bricks):
    for brick in bricks:
        brick.draw()

def show_score(score):
    text = font.render(f"Score: {score}", True, RED)
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT - 30) * SCALE))

def game_over(score, settings: settings.Settings, type_=0, mode=0):
    if mode:
        pygame.mixer.music.pause()
        track3.play()
    screen.fill(BLACK)
    font_for_game_over = pygame.font.SysFont(None, int(42 * SCALE))
    text = font_for_game_over.render("Game Over! Press ENTER to restart", True, RED)
    highscore = settings.highscore
    text2 = font_for_game_over.render(f"High Score = {[score, highscore][highscore>score]}", True, [GREEN, YELLOW][highscore>score])
    text3 = font_for_game_over.render(f"Your Score = {score}", True, BLUE)
    if highscore < score and type_==0:
        settings.highscore = score
        settings.flush()
    screen.blit(text, ((WIDTH // 2 - text.get_width() / 2) * SCALE, (HEIGHT // 2 - 40) * SCALE))
    screen.blit(text2, ((WIDTH // 2 - text2.get_width() / 2) * SCALE, (HEIGHT // 2) * SCALE))
    screen.blit(text3, ((WIDTH // 2 - text3.get_width() / 2) * SCALE, (HEIGHT // 2 + 40) * SCALE))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: 
                if mode:
                    track2.stop()
                    pygame.mixer.music.unpause()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

def drop_powerup(brick_x, brick_y, powerups):
    powerup_type = random.choice(["extra_ball",])
    if len(powerups) < 2 and random.random() < 0.1:
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

def main_game(mode=False):
    player_width = 100 * SCALE
    player_height = 20 * SCALE
    player_speed = 15 * SCALE
    data = settings.Settings.open()
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
    inactivity_threshold = 5

    last_brick_move_time = time.time()
    brick_move_speed = 3

    last_special_ball_time = time.time()

    last_x_key_time = time.time()
    random_destruction_interval = 60

    last_x_time = time.time()
    last_x_value = None


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
            special_balls.append(SpecialBall(player_x + player_width // 2, player_y - ball_radius, dx, dy, current_time + 3))
            if mode:
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
                if mode:
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
                powerup.draw()

            if player_x < powerup.x + powerup.width and player_x + player_width > powerup.x and player_y < powerup.y + powerup.height and player_y + player_height > powerup.y:
                powerups.remove(powerup)
                if powerup.type == "extra_ball":
                    balls.append((WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y))
                    balls_crossed_line.append(False)

        for special_ball in special_balls[:]:
            if special_ball.y < HEIGHT - 70:  
                special_ball.move()
                special_ball.draw()

            if special_ball.x < 0 or special_ball.x > WIDTH or special_ball.y < 0 or special_ball.y > HEIGHT:
                special_balls.remove(special_ball)


        
        draw_bricks([brick for brick in bricks])  
        draw_player(player_x, player_y)

        for i, (ball_x, ball_y, _, _) in enumerate(balls):
            if ball_y < HEIGHT - 60:  
                draw_ball(ball_x, ball_y, i)


        show_score(score)

        if current_time - last_special_ball_time > 19:
            special_ball_text = font.render("Special Ball Ready (UP)", True, GREEN)
        else:
            remaining_time = max(0, 20 - (current_time - last_special_ball_time))
            special_ball_text = font.render(f"Special Ball in {int(remaining_time)}s", True, WHITE)

        if current_time - last_x_key_time > random_destruction_interval - 1:
            countdown_text = font.render("Brick Destruction Ready (DOWN)", True, GREEN)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width() - 20) * SCALE, (HEIGHT - 30) * SCALE))
        else:
            time_until_destruction = max(0, random_destruction_interval - (current_time - last_x_key_time))
            countdown_text = font.render(f"Brick Destruction in {int(time_until_destruction)}s", True, WHITE)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width() - 20) * SCALE, (HEIGHT - 30) * SCALE))

        pygame.draw.line(screen, WHITE, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 2)
        screen.blit(special_ball_text, (20 * SCALE, (HEIGHT - 30) * SCALE))

        pygame.display.flip()

        if not special_balls or current_time - last_special_ball_time >= 2:
            if mode:
                track1.stop()
                pygame.mixer.music.unpause()

        if current_time - last_x_key_time >= 3:
            if mode:
                track2.stop()
                pygame.mixer.music.unpause()


def loading_screen():
    bottom_font = pygame.font.SysFont(None, int(20 * SCALE))
    inner_radius = 20  
    outer_radius = 30  
    spinner_coverage = 0.7  
    total_angle = 360  
    covered_angle = total_angle * spinner_coverage  
    spinner_segments = 12  
    angle_per_segment = covered_angle / spinner_segments  
    spinner_speed = 5  
    angle = 0  

    
    tip_font = pygame.font.SysFont("Arial", 24)
    tips = [
        "Use the paddle to deflect the ball!",
        "Hit bricks for power-ups!",
        "Press UP to launch a special ball!",
        "Stay active to avoid the paddle drifting!"
    ]
    tip = random.choice(tips)

    while True:
        screen.fill(BLACK)  
        clock.tick(60)  

        
        loading_text = font.render("Loading...", True, WHITE)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - 123))

        
        tip_text = tip_font.render("Tip: "+tip, True, WHITE)
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT//2 + 123))

        
        spinner_center = (WIDTH // 2, HEIGHT // 2 + 50)  

        
        for i in range(spinner_segments):
            
            segment_angle_start = angle + (i * angle_per_segment) + 100
            segment_angle_end = segment_angle_start + angle_per_segment + 100

            
            start_x1 = spinner_center[0] - inner_radius * math.cos(math.radians(segment_angle_start))
            start_y1 = spinner_center[1] - inner_radius * math.sin(math.radians(segment_angle_start))

            end_x1 = spinner_center[0] + outer_radius * math.cos(math.radians(segment_angle_start))
            end_y1 = spinner_center[1] + outer_radius * math.sin(math.radians(segment_angle_start))

            start_x2 = spinner_center[0] - inner_radius * math.cos(math.radians(segment_angle_end))
            start_y2 = spinner_center[1] - inner_radius * math.sin(math.radians(segment_angle_end))

            end_x2 = spinner_center[0] + outer_radius * math.cos(math.radians(segment_angle_end))
            end_y2 = spinner_center[1] + outer_radius * math.sin(math.radians(segment_angle_end))

            
            pygame.draw.line(screen, BLUE, (end_x1, end_y1 - 40), (end_x2, end_y2 - 40), 3)
            pygame.draw.line(screen, RED, (start_x1, start_y1 - 40), (start_x2, start_y2 - 40), 3)

        
        angle += spinner_speed
        if angle >= 360:
            angle = 0  

        bottom_text = bottom_font.render("Press Enter to Continue ", True, (92, 95, 119))
        screen.blit(bottom_text, (WIDTH - bottom_text.get_width() - 10, HEIGHT - bottom_text.get_height() - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        
        pygame.display.flip()



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

    options = ["Main Game", "Mute Music"]
    selected_option = 0

    while True:
        screen.fill(BLACK)

        for tile in tiles:
            tile.move()
            tile.draw()

        title_text = title_font.render("BRICKMANIA", True, YELLOW)
        screen.blit(title_text, ((WIDTH // 2 - title_text.get_width() // 2) * SCALE, (HEIGHT // 2 - 150) * SCALE))

        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            option_text = menu_font.render(option+[" [PRESS ENTER]",''][color!=YELLOW], True, color)
            screen.blit(option_text, ((WIDTH // 2 - option_text.get_width() // 2) * SCALE,
                                      (HEIGHT // 2 + i * 60) * SCALE))

        quit_text = menu_font.render("Press Q to Quit", True, WHITE)
        screen.blit(quit_text, ((WIDTH // 2 - quit_text.get_width() // 2) * SCALE, (HEIGHT // 2 + 150) * SCALE))

        pygame.display.flip()
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

pygame.mixer.music.play(-1)

if __name__ == "__main__":
    is_paused = False
    while True:
        selected_option = main_menu()
        if selected_option == 0:
            loading_screen()
            main_game(is_paused)
        if selected_option== 1:
            if is_paused:
                pygame.mixer.music.stop()
                is_paused = not is_paused
            else:
                pygame.mixer.music.play(-1)
                is_paused = not is_paused