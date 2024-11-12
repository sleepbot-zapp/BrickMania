import pygame
import random
import sys
import time

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

# Trail list to store ball positions for trail effect
trail = []
trail_length = 10  # Number of trail elements

# Power-up class for extra balls
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.type = "extra_ball"  # Type of power-up: extra ball
        self.color = GREEN
        self.fall_speed = 1  # Increased fall speed for power-ups

    def move(self):
        self.y += self.fall_speed  # Drop speed of the power-up

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Create a new class for bricks without hit counters (bricks will break in one hit)
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED  # Initial color of the brick

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, brick_width, brick_height))

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=10)

def draw_ball(x, y):
    # Add the current ball position to the trail
    trail.append((x, y))
    if len(trail) > trail_length:
        trail.pop(0)

    # Draw the trail with decreasing opacity
    for i, (tx, ty) in enumerate(trail):
        alpha = 255 - int(255 * (i / trail_length))
        color = (YELLOW[0], YELLOW[1], YELLOW[2], alpha)

        # Create a surface for the trail with per-pixel alpha
        trail_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, color, (ball_radius, ball_radius), ball_radius)
        screen.blit(trail_surface, (tx - ball_radius, ty - ball_radius))

    # Draw the main ball
    pygame.draw.circle(screen, YELLOW, (x, y), ball_radius)

def draw_bricks(bricks):
    for brick in bricks:
        brick.draw()

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
    
    # Wait for spacebar press to restart the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Return to restart the game

def drop_powerup(brick_x, brick_y, powerups):
    # Only drop a power-up if there are fewer than 2 power-ups already on the screen
    if len(powerups) < 2 and random.random() < 0.2:  # 20% chance to drop a power-up
        return PowerUp(brick_x, brick_y)
    return None

def create_new_bricks():
    # Regenerate bricks with no hit counts (break with one hit)
    bricks = []
    for col in range(brick_cols):
        for row in range(brick_rows):
            bricks.append(Brick(col * brick_width, row * brick_height))
    return bricks

def main_game():
    player_x = (WIDTH - player_width) // 2
    player_y = HEIGHT - player_height - 10

    balls = [(WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y)]  # List of balls
    score = 0

    bricks = create_new_bricks()  # Create the initial set of bricks
    powerups = []  # List to store power-ups
    running = True

    # Track player inactivity
    last_move_time = time.time()  # Initialize time of last movement
    inactivity_threshold = 2  # Time in seconds after which player moves automatically

    # Track time for brick movement
    last_brick_move_time = time.time()  # Time to move bricks
    brick_move_speed = 1  # Speed at which bricks move down

    while running:
        screen.fill(BLACK)
        delta_time = clock.tick(60) / 1000
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # If player has been inactive for more than 2 seconds, move randomly
        if current_time - last_move_time > inactivity_threshold:
            if player_x < WIDTH // 2:  # Near the left boundary
                player_x += random.choice([player_speed, -player_speed])  # Move right or left
            elif player_x > WIDTH // 2:  # Near the right boundary
                player_x -= random.choice([player_speed, -player_speed])  # Move left or right
            last_move_time = current_time  # Reset inactivity timer

        # Player movement logic
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            last_move_time = current_time  # Reset inactivity timer
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
            last_move_time = current_time  # Reset inactivity timer

        # Create a list to store balls to be removed
        balls_to_remove = []

        for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collision with screen boundaries
            if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
                ball_dx = -ball_dx

            if ball_y <= ball_radius:
                ball_dy = -ball_dy

            if ball_y >= HEIGHT - ball_radius:
                balls_to_remove.append(i)  # Mark the ball to be removed

            # Ball and player collision logic
            if player_x < ball_x < player_x + player_width and player_y < ball_y + ball_radius < player_y + player_height:
                center_x = player_x + player_width / 2
                if abs(ball_x - center_x) < player_width / 4:  # Near the center
                    ball_dy = -ball_dy  # Reflect vertically, keep ball moving straight
                else:
                    ball_dy = -ball_dy  # Reflect as normal
                ball_y = player_y - ball_radius

            # Update the ball's position
            balls[i] = (ball_x, ball_y, ball_dx, ball_dy)

        # Remove balls that fell off the screen
        for index in reversed(balls_to_remove):  # Reverse to avoid index shifting issues
            balls.pop(index)

        if not balls:  # If no balls are left, end the game
            game_over(score)
            return

        # Brick movement logic: move bricks down every second
        if current_time - last_brick_move_time > 1:  # Move every second
            for brick in bricks:
                brick.y += brick_move_speed
            last_brick_move_time = current_time  # Reset timer

        # Check for collisions with bricks and power-up drops
        for brick in bricks:
            # Check if the ball hits a brick
            for i, (ball_x, ball_y, ball_dx, ball_dy) in enumerate(balls[:]):
                if brick.x < ball_x < brick.x + brick_width and brick.y < ball_y < brick.y + brick_height:
                    bricks.remove(brick)  # Remove the brick on hit
                    score += 10  # Increment score for hitting a brick
                    powerup = drop_powerup(brick.x, brick.y, powerups)
                    if powerup:
                        powerups.append(powerup)  # Drop power-up
                    balls[i] = (ball_x, ball_y, ball_dx, -ball_dy)  # Reflect ball

        # Check if player collects power-up
        for powerup in powerups[:]:
            if player_x < powerup.x + powerup.width and player_x + player_width > powerup.x and \
               player_y < powerup.y + powerup.height and player_y + player_height > powerup.y:
                powerups.remove(powerup)  # Remove the power-up after collection
                balls.append((WIDTH // 2, HEIGHT // 2, ball_speed_x, ball_speed_y))  # Add extra ball
                score += 20  # Score for collecting power-up

        # Move and draw power-ups
        for powerup in powerups:
            powerup.move()
            powerup.draw()

        draw_bricks(bricks)
        draw_player(player_x, player_y)
        for ball_x, ball_y, _, _ in balls:
            draw_ball(ball_x, ball_y)
        show_score(score)
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        main_game()  # Start the game and restart it after it ends
