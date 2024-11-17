import pygame
import sys
from models import Color
from helpers.constants import screen, HEIGHT, WIDTH
from pages.main_menu import main_menu
import os

dummy_text = """
This is a long block of text.
Line after line, it keeps going.
Use it to test the scrolling effect.
Pygame is a great library for graphical apps!
Here's some more text for good measure.
And some more text...
Even more text!
It just keeps going and going...
Eventually, it will loop back to the top.""" * 3

def auto_screen_window(mode, long_text=dummy_text):
    font = pygame.font.Font(None, 36)
    copyright_font = pygame.font.Font(None, 24)  

    text_lines = long_text.split("\n")
    rendered_lines = [font.render(line, True, Color.WHITE) for line in text_lines]

    sprite_width = 50
    sprite_height = 50


    def make_circular_icon(sprite):
        icon_surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        pygame.draw.circle(icon_surface, (255, 255, 255), (sprite_width // 2, sprite_height // 2), sprite_width // 2)
        icon_surface.blit(sprite, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return icon_surface


    sprites = [
            make_circular_icon(pygame.transform.scale(pygame.image.load(f"./assets/sprites/{i}").convert_alpha(), (sprite_width, sprite_height))) 
            for i in os.listdir("./assets/sprites")
        ]
    

    
    scroll_y = 0
    line_height = font.get_linesize()
    total_text_height = line_height * (len(rendered_lines) + 1)  
    scroll_speed = 1
    auto_scroll = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * scroll_speed * 10
                auto_scroll = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_UP:
                    scroll_y += scroll_speed * 10
                    auto_scroll = False
                if event.key == pygame.K_DOWN:
                    scroll_y -= scroll_speed * 10
                    auto_scroll = False
                if event.key == pygame.K_RSHIFT:
                    return main_menu(mode)

        if auto_scroll:
            scroll_y -= scroll_speed
            if scroll_y <= -(total_text_height - HEIGHT // 2):
                auto_scroll = False

        scroll_y = max(-(total_text_height - HEIGHT // 2), min(0, scroll_y))

        screen.fill(Color.BLACK)

        
        for i, line_surface in enumerate(rendered_lines):
            line_y = i * line_height + scroll_y
            if -line_height < line_y < HEIGHT:
                line_x = (WIDTH - line_surface.get_width()) // 2
                screen.blit(line_surface, (line_x, line_y))

        
        pos = WIDTH//(len(sprites)+1)
        icon_y = len(rendered_lines) * line_height + scroll_y + 40  

        if -line_height < icon_y < HEIGHT:
            for i in enumerate(sprites):
                screen.blit(i[1], ((i[0]+1) * pos, icon_y))

        
        copyright_y = icon_y + sprite_height + 40  
        if copyright_y < HEIGHT:
            copyright_text = "© Copyright Text Here"
            copyright_surface = copyright_font.render(copyright_text, True, Color.WHITE)
            copyright_x = (WIDTH // 2 - copyright_surface.get_width()//4 - 20) 
            screen.blit(copyright_surface, (copyright_x, copyright_y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

