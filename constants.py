import pygame

pygame.init()
SCALE = 1
WIDTH, HEIGHT = int(800 * SCALE), int(600 * SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
bottom_font = pygame.font.SysFont(None, int(20 * SCALE))
trail_length = 10
ball_trails = {}