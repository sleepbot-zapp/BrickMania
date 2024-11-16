import pygame

pygame.init()
SCALE = 1
WIDTH, HEIGHT = int(800 * SCALE), int(600 * SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player_width = 100 * SCALE
player_height = 20 * SCALE
player_speed = 900 * SCALE

ball_radius = 10 * SCALE
ball_speed_x, ball_speed_y = 300 * SCALE, -300 * SCALE

brick_width = int(80 * SCALE)
brick_height = 20 * SCALE
brick_speed = 100 * SCALE
brick_rows = 6
brick_cols = WIDTH // brick_width

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, int(25 * SCALE))
bottom_font = pygame.font.SysFont(None, int(20 * SCALE))
trail_length = 10
ball_trails = {}

speed_increment = 1.0001

track1 = pygame.mixer.Sound("./assets/music1.mp3")
track2 = pygame.mixer.Sound("./assets/music2.mp3")
track3 = pygame.mixer.Sound("./assets/music3.mp3")

