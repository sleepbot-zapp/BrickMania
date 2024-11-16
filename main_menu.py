from pygame.font import SysFont
from pygame.display import flip
from pygame import event, KEYDOWN, K_UP, K_DOWN, K_RETURN, K_q, QUIT, quit
from models import FallingTile
from models import Color
from sys import exit
from constants import SCALE, screen, brick_width, brick_height, WIDTH, HEIGHT, bottom_font, clock


def main_menu(mode=False):
    title_font = SysFont(None, int(72 * SCALE))
    menu_font = SysFont(None, int(48 * SCALE))

    tiles = [FallingTile(brick_width, brick_height, WIDTH, HEIGHT, SCALE) for _ in range(20)]

    options = ["Main Game", ["Mute Music", "Unmute Music"][mode], "How to Play"]
    selected_option = 0

    while True:
        screen.fill(Color.BLACK)

        for tile in tiles:
            tile.move(HEIGHT, WIDTH)
            tile.draw(screen)

        title_text = title_font.render("BRICKMANIA", True, Color.YELLOW)
        screen.blit(title_text, ((WIDTH // 2 - title_text.get_width() // 2) * SCALE, (HEIGHT // 2 - 150) * SCALE))

        for i, option in enumerate(options):
            color = Color.YELLOW if i == selected_option else Color.WHITE
            option_text = menu_font.render(option, True, color)
            screen.blit(option_text, ((WIDTH // 2 - option_text.get_width() // 2) * SCALE,
                                      (HEIGHT // 2 + i * 60) * SCALE))

        quit_text = bottom_font.render("Press Q to Quit", True, Color.GREY)
        screen.blit(quit_text, (10, (HEIGHT - quit_text.get_height() - 10) * SCALE))

        bottom_text = bottom_font.render("Press Enter to Continue ", True, Color.GREY)
        screen.blit(bottom_text, (WIDTH - bottom_text.get_width() - 10, HEIGHT - bottom_text.get_height() - 10))

        flip()
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif e.key == K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif e.key == K_RETURN:
                    return selected_option
                elif e.key == K_q:
                    quit()
                    exit()
        clock.tick(60)