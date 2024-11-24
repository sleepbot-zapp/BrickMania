import pygame
import time
import random
import sys

from helpers import settings
from helpers.constants import ball_radius, bottom_font, font
from models import (
    Ball,
    Color,
    Player,
    SpecialBall,
    create_new_bricks,
)
from pages.pages import Page


class DarkModeGame(Page):
    def __init__(self, screen, height, width, scale, game, color, fonts=None):
        super().__init__(screen, height, width, scale, game)
        self.fonts = (pygame.font.SysFont(None, int(42 * self.scale)),)
        self.data = settings.Settings.open()
        self.score = 0
        self.powerups = []
        self.special_balls = []
        self.running = True
        self.bricks = create_new_bricks(color)
        self.last_move_time = self.last_brick_move_time = (
            self.last_special_ball_time
        ) = self.last_x_time = time.time()
        self.balls = [
            Ball(
                screen=self.screen,
                height=self.height,
                width=self.width,
                scale=self.scale,
            )
        ]
        self.player = Player(
            screen=self.screen, height=self.height, width=self.width, scale=self.scale
        )

    def apply_dark_mode(self):
        """Apply dark mode by darkening the entire screen with a semi-transparent layer."""
        dim_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 230))  # Darken with a transparent black surface
        self.screen.blit(dim_surface, (0, 0))

    def pause_game(self, clock, color):
        paused = True
        pause_text = self.fonts[0].render(
            "Game Paused. Press 'P' to Resume.", True, color.WHITE
        )
        dim_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        while paused:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_p, pygame.K_SPACE, pygame.K_RCTRL):
                        paused = False
                    if e.key == pygame.K_q:
                        quit()
                        sys.exit()

            self.screen.blit(dim_surface, (0, 0))
            self.screen.blit(
                pause_text,
                ((self.width - pause_text.get_width()) // 2, self.height // 2),
            )
            pygame.display.flip()

            clock.tick(10)

    def show_score(self, color):
        score = self.score
        text = font.render(f"Score: {score}", True, color.RED)
        self.screen.blit(
            text,
            (
                (self.width // 2 - text.get_width() / 2) * self.scale,
                (self.height - 30) * self.scale,
            ),
        )

    def game_over(self, score, color, settings: settings.Settings):
        self.balls = [
            Ball(
                screen=self.screen,
                height=self.height,
                width=self.width,
                scale=self.scale,
            )
        ]
        curr = time.time()
        if self.game.music_is_playing:
            pygame.mixer.music.pause()
            self.game.music_files[2].play()
        self.screen.fill(color.BLACK)
        font_for_game_over = self.fonts[0]
        text = font_for_game_over.render(
            "Game Over! Press ENTER to restart", True, color.RED
        )
        highscore = settings.highscore
        text2 = font_for_game_over.render(
            f"High Score = {[score, highscore][highscore > score]}",
            True,
            [color.GREEN, color.YELLOW][highscore > score],
        )
        text3 = font_for_game_over.render(f"Your Score = {score}", True, color.YELLOW)

        if highscore < score:
            settings.highscore = score
            settings.flush()

        self.screen.blit(
            text,
            (
                (self.width // 2 - text.get_width() / 2) * self.scale,
                (self.height // 2 - 40) * self.scale,
            ),
        )
        self.screen.blit(
            text2,
            (
                (self.width // 2 - text2.get_width() / 2) * self.scale,
                (self.height // 2) * self.scale,
            ),
        )
        self.screen.blit(
            text3,
            (
                (self.width // 2 - text3.get_width() / 2) * self.scale,
                (self.height // 2 + 40) * self.scale,
            ),
        )

        quit_text = bottom_font.render(
            "Press Shift to go to Main Window", True, color.GREY
        )
        self.screen.blit(
            quit_text, (10, (self.height - quit_text.get_height() - 10) * self.scale)
        )
        pygame.display.flip()

        while True:
            if self.game.music_is_playing and curr - time.time() > 3:
                self.game.music_files[2].stop()
                pygame.mixer.music.unpause()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return False
                    if e.key in (pygame.K_RSHIFT, pygame.K_LCTRL):
                        return True

    def runner(self, color: Color, brick_height, brick_width, trails, clock):
        self.score = 0
        self.bricks = create_new_bricks(color)
        self.powerups = []
        self.special_balls = []
        self.last_move_time = self.last_brick_move_time = (
            self.last_special_ball_time
        ) = self.last_x_time = time.time()

        self.balls = [
            Ball(
                screen=self.screen,
                height=self.height,
                width=self.width,
                scale=self.scale,
            )
        ]

        self.running = True

        while self.running:
            # Apply dark mode if enabled
            self.apply_dark_mode()

            self.screen.fill(color.BLACK)
            dt = clock.tick(60) / 1000
            current_time = time.time()

            if len(self.bricks) == 0:
                self.bricks = create_new_bricks(color)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if current_time - self.last_move_time > 1:
                if self.player.x_start <= self.width // 2:
                    self.player.x_start += 5 * self.player.player_speed * dt
                else:
                    self.player.x_start -= 5 * self.player.player_speed * dt
                self.last_move_time = current_time

            if keys[pygame.K_RCTRL]:
                self.pause_game(clock, color)

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.player.x_start > 10:
                self.player.x_start -= self.player.player_speed * dt
                self.last_move_time = current_time
            if (
                keys[pygame.K_d] or keys[pygame.K_RIGHT]
            ) and self.player.x_start < self.width - self.player.player_width - 10:
                self.player.x_start += self.player.player_speed * dt
                self.last_move_time = current_time

            if (
                (keys[pygame.K_w] or keys[pygame.K_UP])
                and current_time - self.last_special_ball_time
                > 3
            ):
                dx = random.choice([-500, 500])
                dy = random.randint(-300, -120)
                self.special_balls.append(
                    SpecialBall(
                        self.player.x_start + self.player.player_width // 2,
                        self.player.y_start - ball_radius,
                        dx,
                        dy,
                    )
                )
                if self.game.music_is_playing:
                    pygame.mixer.music.pause()
                    self.game.music_files[0].play()
                self.last_special_ball_time = current_time

            for ball in self.balls:
                ball.draw_ball()
                ball.move_ball()

            self.score += ball_radius

            self.show_score(color)

            if self.game_over(self.score, color, self.data):
                break
