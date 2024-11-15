from pygame.font import SysFont
from pygame.display import flip
from pygame import event, KEYDOWN, K_UP, K_DOWN, K_RETURN, K_q, QUIT, quit
from models import FallingTile
from models import Color
from sys import exit
from .game_control import game_over

def main_menu(scale, screen, HEIGHT, WIDTH, clock):
    title_font = SysFont(None, int(72 * scale))
    menu_font = SysFont(None, int(48 * scale))

    tiles = [FallingTile() for _ in range(20)]

    options = ["Main Game", "Demo Game"]
    selected_option = 0

    while True:
        screen.fill(Color.BLACK)

        for tile in tiles:
            tile.move()
            tile.draw()

        screen.blit(text:=title_font.render("BRICKMANIA", True, Color.YELLOW), ((WIDTH // 2 - text.get_width() // 2) * scale, (HEIGHT // 2 - 150) * scale))
        for i, option in enumerate(options):
            color = Color.YELLOW if i == selected_option else Color.WHITE
            screen.blit(text:=menu_font.render(option+[" [PRESS ENTER]",''][color!=Color.YELLOW], True, color), ((WIDTH // 2 - text.get_width() // 2) * scale, (HEIGHT // 2 + i * 60) * scale))
        screen.blit(text:=menu_font.render("Press Q to Quit", True, Color.WHITE), ((WIDTH // 2 - text.get_width() // 2) * scale, (HEIGHT // 2 + 150) * scale))

        flip()
        for event in event.get():
            if event.type == QUIT:
                game_over()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == K_RETURN:
                    return selected_option
                elif event.key == K_q:
                    game_over()

        clock.tick(60)