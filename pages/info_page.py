import pygame
from pages.pages import Page
import os
import sys
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

class Info(Page):
    def __init__(self, screen, game, height, width, scale, fonts=None,) -> None:
        super().__init__(screen, height, width, scale, fonts)
        self.fonts = (
            pygame.font.Font(None, 20), # Font
            pygame.font.Font(None, 30), # Bold
            pygame.font.Font(None, 24), # Subtitle
            pygame.font.Font(None, 26) # Bottom
        )
        self.game = game
        self.sprite_width = self.sprite_height = 50
        self.top_margin = 50
        

    def make_circular_icon(self, sprite):
        icon_surface = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
        pygame.draw.circle(icon_surface, (255, 255, 255), (self.sprite_width // 2, self.sprite_height // 2), self.sprite_width // 2)
        icon_surface.blit(sprite, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return icon_surface
    
    @property
    def sprites(self):
        sprites = []
        for filename in os.listdir("./assets/sprites"):
            sprite = pygame.image.load(f"./assets/sprites/{filename}").convert_alpha()
            sprite = pygame.transform.scale(sprite, (self.sprite_width, self.sprite_height))
            sprites.append(self.make_circular_icon(sprite))
        return sprites
    

    def wrap_text(self, line, font):
        max_text_width = int(self.width * 0.8)
        words = textwrap.wrap(line, width=max_text_width // font.size(" ")[0])
        return words
    

    def parse_markdown(self,line, color):
        if line.startswith("**") and line.endswith("**"):
            wrapped_lines = self.wrap_text(line[2:-2], self.fonts[1])
            return [{"type": "text", "surface": self.fonts[1].render(w, True, color.WHITE)} for w in wrapped_lines]
        elif line.startswith("@"):
            wrapped_lines = self.wrap_text(line[1:], self.fonts[2])
            return [{"type": "subtitle", "surface": self.fonts[2].render(w, True, color.GREY)} for w in wrapped_lines]
        elif line.startswith("---"):
            return [{"type": "line"}]
        elif line.startswith("^"):
            return [{"type": "line2"}]
        else:
            wrapped_lines = self.wrap_text(line, self.fonts[0])
            return [{"type": "text", "surface": self.fonts[0].render(w, True, color.WHITE)} for w in wrapped_lines]

    def scroll(self, color):
        rendered_lines = []
        for line in long_text.split("\n"):
            rendered_lines.extend(self.parse_markdown(line, color))
        auto_scroll = True
        line_height = self.fonts[0].get_linesize()
        scroll_y = self.top_margin
        total_text_height = self.fonts[0].get_linesize() * len(rendered_lines)
        running = True
        scroll_speed = 1
        tooltips = ["Saad", "Zapp", "Aarthex"]
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            hover_sprite_index = None 
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEWHEEL:
                    scroll_y -= e.y * scroll_speed * 10
                    auto_scroll = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return
                    if e.key == pygame.K_UP:
                        scroll_y += scroll_speed * 10
                        auto_scroll = False
                    if e.key == pygame.K_DOWN:
                        scroll_y -= scroll_speed * 10
                        auto_scroll = False
                    if e.key == pygame.K_RSHIFT:
                        return True

            if auto_scroll:
                scroll_y -= scroll_speed
                if scroll_y <= -(total_text_height - self.height // 2):
                    auto_scroll = False

            scroll_y = max(-(total_text_height - self.height // 2), min(self.top_margin, scroll_y))
            self.screen.fill(color.BLACK)

            current_y = scroll_y
            for line in rendered_lines:
                if line["type"] == "text":
                    line_surface = line["surface"]
                    line_x = (self.width - line_surface.get_width()) // 2
                    if -line_height < current_y < self.height:
                        self.screen.blit(line_surface, (line_x, current_y))
                    current_y += line_height
                elif line["type"] == "subtitle":
                    line_surface = line["surface"]
                    line_x = (self.width - line_surface.get_width()) // 2
                    if -line_height < current_y < self.height:
                        self.screen.blit(line_surface, (line_x, current_y))
                    current_y += line_height + 10
                elif line["type"] == "line":
                    current_y += 15
                    if -line_height < current_y < self.height:
                        line_width = int(self.width * 0.4)
                        line_x_start = (self.width - line_width) // 2
                        pygame.draw.line(
                            self.screen,
                            (60, 68, 76),
                            (line_x_start, current_y + 5),
                            (line_x_start + line_width, current_y + 5),
                            2,
                        )
                    current_y += 15
                elif line["type"] == "line2":
                    current_y += 15
                    if -line_height < current_y < self.height:
                        line_width = int(self.width * 0.8)
                        line_x_start = (self.width - line_width) // 2
                        pygame.draw.line(
                            self.screen,
                            (69, 70, 80),
                            (line_x_start, current_y + 5),
                            (line_x_start + line_width, current_y + 5),
                            5,
                        )
                    current_y += 20

            pos = self.width // (len(self.sprites) + 1)
            icon_y = current_y + 40
            if -line_height < icon_y < self.height:
                for i, sprite in enumerate(self.sprites):
                    sprite_x = (i + 1) * pos
                    sprite_rect = sprite.get_rect(center=(sprite_x, icon_y))
                    if sprite_rect.collidepoint(mouse_pos):
                        hover_sprite_index = i
                    self.screen.blit(sprite, sprite_rect.topleft)

            if hover_sprite_index is not None:
                tooltip_text = tooltips[hover_sprite_index]
                tooltip_surface = self.fonts[2].render(tooltip_text, True, color.RED)
                tooltip_x = mouse_pos[0]
                tooltip_y = mouse_pos[1] + 40
                self.screen.blit(tooltip_surface, (tooltip_x, tooltip_y))

            pygame.display.flip()
            pygame.time.Clock().tick(60)
