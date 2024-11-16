import math
import random
import pygame
from constants import screen, WIDTH, HEIGHT, font, bottom_font, clock
from models import Color
from runner import runner # to be used for later
import sys

def loading_screen(func1, func2):
    radius = 30  
    spinner_segments = 12  
    angle_per_segment = random.randint(-3600, 3600)
    spinner_speed = random.choice([-5, 5])
    angle = 0  

    
    tip_font = pygame.font.SysFont("Arial", 24)
    tips = [
        "Use the paddle to deflect the ball!",
        "Hit bricks for power-ups!",
        "Press UP to launch a special ball!",
        "Stay active to avoid the paddle drifting!",
        "Press DOWN to destroy 5 random bricks!"
    ]
    tip = random.choice(tips)

    while True:
        screen.fill(Color.BLACK)  
        clock.tick(60)  

        
        loading_text = font.render("BrickMania", True, Color.WHITE)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - 123))

        
        tip_text = tip_font.render("Tip: "+tip, True, Color.WHITE)
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT//2 + 123))

        
        spinner_center = (WIDTH // 2, HEIGHT // 2)  

        
        for i in range(spinner_segments):
            
            segment_angle_start = angle + (i * angle_per_segment)
            segment_angle_end = segment_angle_start + angle_per_segment

            x1_multiplier = random.choice([-1, 1])
            x2_multiplier = random.choice([-1, 1])
            start_x1 = spinner_center[0] - radius * func1(math.cos(math.radians(segment_angle_start))) * (x1_multiplier)
            start_y1 = spinner_center[1] + radius * func1(math.sin(math.radians(segment_angle_start))) * x2_multiplier

            end_x1 = spinner_center[0] + radius * func1(math.cos(math.radians(segment_angle_start))) * (x1_multiplier)
            end_y1 = spinner_center[1] - radius * func1(math.sin(math.radians(segment_angle_start))) * x2_multiplier

            start_x2 = spinner_center[0] - radius * func2(math.cos(math.radians(segment_angle_end))) * x2_multiplier
            start_y2 = spinner_center[1] + radius * func2(math.sin(math.radians(segment_angle_end))) * (x1_multiplier)

            end_x2 = spinner_center[0] + radius * func2(math.cos(math.radians(segment_angle_end))) * (x2_multiplier)
            end_y2 = spinner_center[1] - radius * func2(math.sin(math.radians(segment_angle_end))) * (x1_multiplier)

            pygame.draw.line(screen, Color.BLUE, (end_x1, end_y1 ), (end_x2, end_y2), 3)
            pygame.draw.line(screen, Color.RED, (start_x1, start_y1), (start_x2, start_y2), 3)

        
        angle += spinner_speed
        if angle >= 360:
            angle = 0  

        bottom_text = bottom_font.render("Press Enter to Continue", True, (92, 95, 119))
        screen.blit(bottom_text, (WIDTH - bottom_text.get_width() - 10, HEIGHT - bottom_text.get_height() - 10))
        bottom_text = bottom_font.render("Press Shift to go back ", True, (92, 95, 119))
        screen.blit(bottom_text, (10, HEIGHT - bottom_text.get_height() - 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                #    runner(main_menu, loading_screen, main_game)
                    return

        
        pygame.display.flip()
