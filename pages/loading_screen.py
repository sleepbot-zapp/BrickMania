import math
from random import choice
from pygame.font import SysFont
from pygame import KEYDOWN, K_q, K_LSHIFT, K_RSHIFT, K_RETURN, quit, QUIT, event
from pygame.draw import line
from pygame.display import flip
from helpers.constants import screen, WIDTH, HEIGHT, font, bottom_font, clock
from models import Color
from sys import exit

def loading_screen(func1, func2):
    radius = 30  
    spinner_segments = 12
    angle_per_segment = 25
    spinner_speed = choice([-2, 2])
    angle = 0  

    
    tip_font = SysFont("Arial", 24)
    tips = [
        "Use the paddle to deflect the ball!",
        "Hit bricks for power-ups!",
        "Press UP to launch a special ball!",
        "Stay active to avoid the paddle drifting!",
        "Press DOWN to destroy 5 random bricks!"
    ]
    tip = choice(tips)
    direc = choice([-1, 1])
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
            
            start_x1 = spinner_center[0] + radius * func1(math.cos(math.radians(segment_angle_start)))
            start_y1 = spinner_center[1] + radius * func1(math.sin(math.radians(segment_angle_start)))

            end_x1 = spinner_center[0] - radius * func1(math.cos(math.radians(segment_angle_start)))
            end_y1 = spinner_center[1] - radius * func1(math.sin(math.radians(segment_angle_start)))

            start_x2 = spinner_center[0] + radius * func2(math.cos(math.radians(segment_angle_end)))
            start_y2 = spinner_center[1] + radius * func2(math.sin(math.radians(segment_angle_end)))

            end_x2 = spinner_center[0] - radius * func2(math.cos(math.radians(segment_angle_end)))
            end_y2 = spinner_center[1] - radius * func2(math.sin(math.radians(segment_angle_end)))

            
            line(screen, Color.BLUE, (end_x1, end_y1), (end_x2, end_y2), 3)
            line(screen, Color.RED, (start_x1, start_y1), (start_x2, start_y2), 3)

            line(screen, Color.BLUE, (end_x1, end_y1 ), (end_x2, end_y2), 3)
            line(screen, Color.RED, (start_x1, start_y1), (start_x2, start_y2), 3)

        
        angle += spinner_speed * direc

        bottom_text = bottom_font.render("Press Enter to Continue", True, (92, 95, 119))
        screen.blit(bottom_text, (WIDTH - bottom_text.get_width() - 10, HEIGHT - bottom_text.get_height() - 10))
        bottom_text = bottom_font.render("Press Shift to go back ", True, (92, 95, 119))
        screen.blit(bottom_text, (10, HEIGHT - bottom_text.get_height() - 10))
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    return
                if e.key == K_q:
                    quit()
                    exit()
                if e.key in (K_RSHIFT, K_LSHIFT):
                    return

        
        flip()
