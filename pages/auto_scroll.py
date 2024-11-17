import pygame
import sys
from models import Color
from helpers.constants import screen, HEIGHT, WIDTH
from pages.main_menu import main_menu
import os
import textwrap

long_text = """
**BrickMania**
^
@How to Play
---
@Keyboard Controls
    Use the keyboard to control your paddle and interact with the game:
    1. Arrow keys: Move the paddle left or right.
    2. Space: Pause or resume the game.
    3. W / Down Arrow: Activate special moves.
    4. Shift: Return to the main menu.

    Keep the paddle moving to avoid losing balls. Stay sharp!
---
@Options
    From the start menu, you can adjust gameplay settings, such as:
    1. Game speed: Slow, Normal, or Fast.
    2. Sound effects: Mute or Unmute.

    Please note: Settings will reset when you restart the game. Persistent settings will be added in a future update.
---
@Special Moves
    Special moves provide powerful abilities with cooldowns:
    1. Special Ball: Available every 20 seconds. Press W or Down Arrow to activate.
    2. Brick Destruction: Activated every 60 seconds. Destroys 5 bricks instantly!

    These abilities can turn the tide of the game. Use them wisely!
---
@Power-ups
    Power-ups appear randomly as you destroy bricks:
        Extra Ball: Adds another ball to the game. Be cautious! The game speeds up as more balls appear.

    Power-ups can help you clear levels faster but require skill to manage effectively.
---
@Game Mechanics
    Stay engaged! If you stop moving the paddle for more than 5 seconds, it will move automatically.

    The challenge increases as you progress. Adapt and improve your skills to master BrickMania!
^
"""

def auto_screen_window():
    font = pygame.font.Font(None, 20)
    bold_font = pygame.font.Font(None, 30)
    subtitle_font = pygame.font.Font(None, 24)
    copyright_font = pygame.font.Font(None, 24)
    sprite_width = 50
    sprite_height = 50
    top_margin = 50  # Margin at the top

    # Load sprites
    def make_circular_icon(sprite):
        icon_surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        pygame.draw.circle(icon_surface, (255, 255, 255), (sprite_width // 2, sprite_height // 2), sprite_width // 2)
        icon_surface.blit(sprite, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return icon_surface

    sprites = []
    for filename in os.listdir("./assets/sprites"):
        sprite = pygame.image.load(f"./assets/sprites/{filename}").convert_alpha()
        sprite = pygame.transform.scale(sprite, (sprite_width, sprite_height))
        sprites.append(make_circular_icon(sprite))

    # Text wrapping function
    def wrap_text(line, font):
        max_text_width = int(WIDTH * 0.8)
        words = textwrap.wrap(line, width=max_text_width // font.size(" ")[0])
        return words

    # Parse and render markdown
    def parse_markdown(line):
        if line.startswith("**") and line.endswith("**"):
            wrapped_lines = wrap_text(line[2:-2], bold_font)
            return [{"type": "text", "surface": bold_font.render(w, True, Color.WHITE)} for w in wrapped_lines]
        elif line.startswith("@"):
            wrapped_lines = wrap_text(line[1:], subtitle_font)
            return [{"type": "subtitle", "surface": subtitle_font.render(w, True, Color.GREY)} for w in wrapped_lines]
        elif line.startswith("---"):
            return [{"type": "line"}]
        elif line.startswith("^"):
            return [{"type": "line2"}]
        else:
            wrapped_lines = wrap_text(line, font)
            return [{"type": "text", "surface": font.render(w, True, Color.WHITE)} for w in wrapped_lines]

    text_lines = long_text.split("\n")
    rendered_lines = []
    for line in text_lines:
        rendered_lines.extend(parse_markdown(line))

    scroll_y = top_margin  # Add top margin
    line_height = font.get_linesize()
    total_text_height = line_height * len(rendered_lines)
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

        scroll_y = max(-(total_text_height - HEIGHT // 2), min(top_margin, scroll_y))  # Limit scrolling to top_margin
        screen.fill(Color.BLACK)

        # Render lines with wrapping
        current_y = scroll_y
        for line in rendered_lines:
            if line["type"] == "text":
                line_surface = line["surface"]
                line_x = (WIDTH - line_surface.get_width()) // 2
                if -line_height < current_y < HEIGHT:
                    screen.blit(line_surface, (line_x, current_y))
                current_y += line_height
            elif line["type"] == "subtitle":
                line_surface = line["surface"]
                line_x = (WIDTH - line_surface.get_width()) // 2
                if -line_height < current_y < HEIGHT:
                    screen.blit(line_surface, (line_x, current_y))
                current_y += line_height + 10
            elif line["type"] == "line":
                current_y += 15
                if -line_height < current_y < HEIGHT:
                    line_width = int(WIDTH * 0.4)
                    line_x_start = (WIDTH - line_width) // 2
                    pygame.draw.line(
                        screen,
                        (60, 68, 76),
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
                        (69, 70, 80),
                        (line_x_start, current_y + 5),
                        (line_x_start + line_width, current_y + 5),
                        5,
                    )
                current_y += 20

        # Render sprites and copyright text
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

# Run the auto_screen_window function
