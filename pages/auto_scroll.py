import pygame
import sys
from models import Color
from helpers.constants import screen, HEIGHT, WIDTH
from pages.main_menu import main_menu
import os

long_text = """Lorem  Ipsum"""
"""
**BrickMania**\n
^
How to Play
---
Keyboard Controls
    Line after line, it keeps going.
    Use it to test the scrolling effect.
    Pygame is a great library for graphical apps!
    Here's some more text for good measure.
---
Options
On the start menu, you can select certain options that modify gameplay. 
Currently, these settings do not persist across restarts, but this feature is planned for future updates.
You can navigate the options using the arrow keys.
    Mute Music / Unmute Music: Mutes / Unmutes the music and sounds of the game. [Temporarily Removed]
---
Special Moves
    Special moves are powerful abilities with cooldowns. 
    There are currently 2 special moves available:
    Every 20 seconds, you’ll gain a SPECIAL Ball, which is red in color. 
    You can activate it by pressing either the W key or the Down Arrow key.
    Every 60 seconds, you’ll unlock the Brick Destruction powerup.
    You will destroy 5 bricks.
Powerups
    Powerups are items that drop randomly as you play, 
    either after destroying bricks or at specific intervals.
    After breaking a brick, there’s a chance an Extra Ball powerup will begin to fall. 
      Catch it, and you’ll gain an additional ball that can help you clear more bricks! 
      However, be cautious—each extra ball makes the game significantly faster!
Game Mechanics
    If you stay stationary for too long (5 seconds), the paddle will move on its own.
^"""

def auto_screen_window():
    font = pygame.font.Font(None, 25)
    bold_font = pygame.font.Font(None, 30)
    copyright_font = pygame.font.Font(None, 24)

    sprite_width = 50
    sprite_height = 50

    def make_circular_icon(sprite):
        icon_surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        pygame.draw.circle(icon_surface, (255, 255, 255), (sprite_width // 2, sprite_height // 2), sprite_width // 2)
        icon_surface.blit(sprite, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return icon_surface

    sprites = [
        make_circular_icon(
            pygame.transform.scale(pygame.image.load(f"./assets/sprites/{i}").convert_alpha(), (sprite_width, sprite_height))
        )
        for i in os.listdir("./assets/sprites")
    ]

    
    def parse_markdown(line):
        if line.startswith("**") and line.endswith("**"):  
            return {"type": "text", "surface": bold_font.render(line[2:-2], True, Color.WHITE)}
        elif line.startswith("---"):  
            return {"type": "line"}
        elif line.startswith("^"): 
            return {"type": "line2"}
        else:  
            return {"type": "text", "surface": font.render(line, True, Color.WHITE)}

    
    text_lines = long_text.split("\n")
    rendered_lines = [parse_markdown(line) for line in text_lines]

    scroll_y = 0
    line_height = font.get_linesize()
    total_text_height = line_height * len(rendered_lines) + 1
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
                    return main_menu()

        if auto_scroll:
            scroll_y -= scroll_speed
            if scroll_y <= -(total_text_height - HEIGHT // 2):
                auto_scroll = False

        scroll_y = max(-(total_text_height - HEIGHT // 2), min(0, scroll_y))

        screen.fill(Color.BLACK)

        
        current_y = scroll_y
        for line in rendered_lines:
            if line["type"] == "text":  
                line_surface = line["surface"]
                line_x = (WIDTH - line_surface.get_width()) // 2
                if -line_height < current_y < HEIGHT:
                    screen.blit(line_surface, (line_x, current_y))
                current_y += line_height
            elif line["type"] == "line":  
                if -line_height < current_y < HEIGHT:
                    line_width = int(WIDTH * 0.4)  
                    line_x_start = (WIDTH - line_width) // 2  
                    pygame.draw.line(
                        screen,
                        (60,68,76),  
                        (line_x_start, current_y + 5),  
                        (line_x_start + line_width, current_y + 5),  
                        2,  
                    )
                current_y += 15  
            elif line["type"] == "line2":
                current_y += 15  
                if -line_height < current_y < HEIGHT:
                    line_width = int(WIDTH * 0.8)  
                    line_x_start = (WIDTH - line_width) // 2  
                    pygame.draw.line(
                        screen,
                        (69,70,80),  
                        (line_x_start, current_y + 5),  
                        (line_x_start + line_width, current_y + 5),  
                        5,  
                    )
                current_y += 20  

        
        pos = WIDTH // (len(sprites) + 1)
        icon_y = current_y + 40  

        if -line_height < icon_y < HEIGHT:
            for i, sprite in enumerate(sprites):
                screen.blit(sprite, ((i + 1) * pos, icon_y))

        
        copyright_y = icon_y + sprite_height + 40
        if copyright_y < HEIGHT:
            copyright_text = "© Copyright Text Here"
            copyright_surface = copyright_font.render(copyright_text, True, Color.WHITE)
            copyright_x = (WIDTH - copyright_surface.get_width()) // 2
            screen.blit(copyright_surface, (copyright_x, copyright_y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
