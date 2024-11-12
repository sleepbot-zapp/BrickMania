import pygame
import random
import sys
import time

pygame.init()

pygame.mixer.music.load("./brickmania/music.mp3")
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICKMANIA")

WHITE = (255, 255, 255)
RED = (255, 30, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

player_width = 100
player_height = 20
player_speed = 15

ball_radius = 10
ball_speed_x, ball_speed_y = 5, -5

brick_width = 60
brick_height = 20
brick_speed = 10
brick_rows = 6
brick_cols = WIDTH // brick_width

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

trail = []
trail_length = 10

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.type = "extra_ball"
        self.color = GREEN
        self.fall_speed = 2

    def move(self):
        self.y += self.fall_speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice([RED, BLUE, GREEN, YELLOW])  # Randomize brick color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, brick_width, brick_height))
        # Draw black border around the brick
        pygame.draw.rect(screen, BLACK, (self.x, self.y, brick_width, brick_height), 2)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=10)

def draw_ball(x, y):
    trail.append((x, y))
    if len(trail) > trail_length:
        trail.pop(0)

    for i, (tx, ty) in enumerate(trail):
        alpha = 255 - int(255 * (i / trail_length))
        color = (YELLOW[0], YELLOW[1], YELLOW[2], alpha)
        trail_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, color, (ball_radius, ball_radius), ball_radius)
        screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))

    pygame.draw.circle(screen, YELLOW, (x, y), ball_radius)

def draw_bricks(bricks):
    for brick in bricks:
        brick.draw()

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over(score):
    text = font.render("Game Over! Press SPACE to restart", True, WHITE)
    highscore = int(open("./brickmania/highscore.txt").read())
    text2 = font.render(f"High Score = {[score, highscore][highscore>score]}", True, WHITE)
    if highscore < score:
        with open('./brickmania/highscore.txt', 'w') as f:
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

def drop_powerup(brick_x, brick_y, powerups):
    if len(powerups) < 2 and random.random() < 0.2:
        return PowerUp(brick_x, brick_y)
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

def main_game():
    player_x = (WIDTH - player_width) // 2
    player_y = HEIGHT - player_height - 70

    balls = [(WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y)]
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

    while running:
        screen.fill(BLACK)
        delta_time = clock.tick(60) / 1000
        current_time = time.time()

        if len(bricks) == 0:
            bricks = create_new_bricks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if current_time - last_move_time > inactivity_threshold:
            if player_x < WIDTH // 2:
                player_x += random.choice([player_speed, -player_speed])
            elif player_x > WIDTH // 2:
                player_x -= random.choice([player_speed, -player_speed])
            last_move_time = current_time

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            last_move_time = current_time
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
            last_move_time = current_time

        # Create 10 special balls if UP key is pressed
        if keys[pygame.K_UP] and current_time - last_special_ball_time > 20:
            for _ in range(10):  # Create exactly 10 special balls
                dx = random.choice([8, -8])  # Faster speed
                dy = random.choice([-16, -16])  # Ensure they go up
                special_balls.append(SpecialBall(player_x + player_width // 2, player_y - ball_radius, dx, dy, current_time + 3))
            last_special_ball_time = current_time

        balls_to_remove = []
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
                if abs(ball_x - center_x) < player_width / 4:
                    ball_dy = -ball_dy
                else:
                    ball_dy = -ball_dy
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

        bricks_to_remove = []  # Store bricks to remove here
        for brick in bricks:
            for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
                if brick.x < ball_x < brick.x + brick_width and brick.y < ball_y < brick.y + brick_height:
                    bricks_to_remove.append(brick)  # Mark brick for removal
                    score += 10
                    powerup = drop_powerup(brick.x, brick.y, powerups)
                    if powerup:
                        powerups.append(powerup)
                    balls[i] = (ball_x, ball_y, ball_dx, -ball_dy)

            for special_ball in special_balls[:]:
                if brick.x < special_ball.x < brick.x + brick_width and brick.y < special_ball.y < brick.y + brick_height:
                    bricks_to_remove.append(brick)  # Mark brick for removal
                    score += 10
                    powerup = drop_powerup(brick.x, brick.y, powerups)
                    if powerup:
                        powerups.append(powerup)
                    special_ball.dy = -special_ball.dy

        # Remove the bricks after iterating through the list
        for brick in bricks_to_remove:
            if brick in bricks:
                bricks.remove(brick)

        # Handle powerup collection
        for powerup in powerups[:]:
            powerup.move()
            powerup.draw()

            # Check if the player collects the powerup
            if player_x < powerup.x + powerup.width and player_x + player_width > powerup.x and player_y < powerup.y + powerup.height and player_y + player_height > powerup.y:
                powerups.remove(powerup)
                if powerup.type == "extra_ball":
                    # Create an extra ball
                    balls.append((WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y))
                    balls_crossed_line.append(False)
                    score += 50  # Bonus score for collecting powerup


        # Handle special balls
        for special_ball in special_balls[:]:
            special_ball.move()
            special_ball.draw()

        draw_bricks(bricks)
        draw_player(player_x, player_y)
        for ball_x, ball_y, _, _ in balls:
            draw_ball(ball_x, ball_y)

        show_score(score)

        if current_time - last_special_ball_time > 20:
            special_ball_text = font.render("Special Balls Ready!", True, WHITE)
        else:
            remaining_time = max(0, 20 - (current_time - last_special_ball_time))
            special_ball_text = font.render(f"Special Balls in {int(remaining_time)}s", True, WHITE)

        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)

        screen.blit(special_ball_text, (WIDTH // 2 - special_ball_text.get_width() // 2, HEIGHT - 40))

        pygame.display.flip()





if __name__ == "__main__":
    while True:
        main_game()