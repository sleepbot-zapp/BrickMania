from pages.pages import Page
from helpers import settings
from helpers.game_control import create_new_bricks
from helpers.constants import (
    ball_radius,
    track1,
    track2,
    track3,
    font,
    bottom_font,
)
from models import Player, Color, SpecialBall, Ball, drop_powerup, draw_bricks
import pygame
import sys
import time
import random


class MainGame(Page):
    inactivity_threshold = 5
    special_ball_time = 20
    random_destruction_time = 60

    def __init__(self, screen, height, width, scale, game, fonts=None) -> None:
        super().__init__(screen, height, width, scale, fonts)
        self.fonts = (pygame.font.SysFont(None, int(42 * self.scale)),)
        self.data = settings.Settings.open()
        self.game = game
        self.score = 0
        self.powerups = []
        self.special_balls = []
        self.running = True
        self.bricks = create_new_bricks()
        self.last_move_time = self.last_brick_move_time = (
            self.last_special_ball_time
        ) = self.last_x_time = time.time()

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
        curr = time.time()
        if self.game.music_is_playing:
            pygame.mixer.music.pause()
            track3.play()
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
        text3 = font_for_game_over.render(f"Your Score = {score}", True, color.BLUE)

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
                track3.stop()
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

    def runner(
        self, color: Color, player, balls, brick_height, brick_width, trails, clock
    ):
        while True:
            self.score = 0
            self.bricks = create_new_bricks()
            self.powerups = []
            self.special_balls = []
            self.last_move_time = self.last_brick_move_time = (
                self.last_special_ball_time
            ) = self.last_x_time = time.time()

            player = Player(
                screen=self.screen,
                height=self.height,
                width=self.width,
                scale=self.scale,
            )
            balls = [
                Ball(
                    screen=self.screen,
                    height=self.height,
                    width=self.width,
                    scale=self.scale,
                )
            ]

            self.running = True

            while self.running:
                self.screen.fill(color.BLACK)
                dt = clock.tick(60) / 1000
                current_time = time.time()

                if len(self.bricks) == 0:
                    self.bricks = create_new_bricks()

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()

                if current_time - self.last_move_time > self.inactivity_threshold:
                    if player.x_start <= self.width // 2:
                        player.x_start += 5 * player.player_speed * dt
                    else:
                        player.x_start -= 5 * player.player_speed * dt
                    self.last_move_time = current_time

                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x_start > 10:
                    player.x_start -= player.player_speed * dt
                    self.last_move_time = current_time
                if (
                    keys[pygame.K_d] or keys[pygame.K_RIGHT]
                ) and player.x_start < self.width - player.player_width - 10:
                    player.x_start += player.player_speed * dt
                    self.last_move_time = current_time

                if (
                    (keys[pygame.K_w] or keys[pygame.K_UP])
                    and current_time - self.last_special_ball_time
                    > self.special_ball_time - 1
                ):
                    dx = random.choice([-500, 500])
                    dy = random.randint(-300, -120)
                    self.special_balls.append(
                        SpecialBall(
                            player.x_start + player.player_width // 2,
                            player.y_start - ball_radius,
                            dx,
                            dy,
                        )
                    )
                    if self.game.music_is_playing:
                        pygame.mixer.music.pause()
                        track1.play()
                    self.last_special_ball_time = current_time

                if (
                    (keys[pygame.K_DOWN] or keys[pygame.K_s])
                    and current_time - self.last_x_time
                    > self.random_destruction_time - 1
                ):
                    for _ in range(5):
                        if self.bricks:
                            random_brick = random.choice(self.bricks)
                            self.bricks.remove(random_brick)
                            self.score += 10
                    if self.game.music_is_playing:
                        pygame.mixer.music.pause()
                        track2.play()
                    self.last_x_time = current_time

                if keys[pygame.K_RSHIFT]:
                    return True

                for ball in balls:
                    ball.x, ball.y, ball.dx, ball.dy = ball.move_ball(dt, player)

                if all(ball.ball_crossed_line for ball in balls):
                    user_exited = self.game_over(self.score, color, self.data)
                    if user_exited:
                        return True
                    else:
                        break

                if current_time - self.last_brick_move_time > 1:
                    for brick in self.bricks:
                        brick.y += brick.speed * dt
                        if brick.y + brick.height >= self.height:
                            user_exited = self.game_over(self.score, color, self.data)
                            if user_exited:
                                return True
                            else:
                                break
                    self.last_brick_move_time = current_time

                bricks_to_remove = []
                for brick in self.bricks:
                    for ball in balls:
                        if (
                            brick.x < ball.x < brick.x + brick.width
                            and brick.y < ball.y < brick.y + brick.height
                        ):
                            bricks_to_remove.append(brick)
                            self.score += 10
                            powerup = drop_powerup(
                                brick.x, brick.y, self.powerups, self.scale
                            )
                            if powerup:
                                self.powerups.append(powerup)
                            ball.dy = -ball.dy

                    for special_ball in self.special_balls:
                        if (
                            brick.x < special_ball.x < brick.x + brick_width
                            and brick.y < special_ball.y < brick.y + brick_height
                        ):
                            bricks_to_remove.append(brick)
                            self.score += 10
                            powerup = drop_powerup(
                                brick.x, brick.y, self.powerups, self.scale
                            )
                            if powerup:
                                self.powerups.append(powerup)

                for brick in bricks_to_remove:
                    if brick in self.bricks:
                        self.bricks.remove(brick)

                for powerup in self.powerups:
                    if powerup.y < self.height - 70:
                        powerup.move(dt)
                        powerup.draw(self.screen)

                    if (
                        player.x_start < powerup.x + powerup.width
                        and player.x_start + player.player_width > powerup.x
                        and player.y_start < powerup.y + powerup.height
                        and player.y_start + player.player_height > powerup.y
                    ):
                        self.powerups.remove(powerup)
                        if powerup.type == "extra_ball":
                            balls.append(
                                Ball(
                                    screen=self.screen,
                                    height=self.height,
                                    width=self.width,
                                    scale=self.scale,
                                )
                            )

                for special_ball in self.special_balls:
                    if special_ball.y < self.height - 70:
                        special_ball.move(ball_radius, self.width, dt)
                        special_ball.draw(self.screen, ball_radius)

                    if (
                        special_ball.x < 0
                        or special_ball.x > self.width
                        or special_ball.y < 0
                        or special_ball.y > self.height
                    ):
                        self.special_balls.remove(special_ball)

                draw_bricks(self.bricks, self.screen, brick_width, brick_height)
                player.draw_player()

                if self.game.music_is_playing:
                    if (
                        not self.special_balls
                        or current_time - self.last_special_ball_time >= 2
                    ):
                        track1.stop()
                        pygame.mixer.music.unpause()
                    if current_time - self.last_x_time >= 3:
                        track2.stop()
                        pygame.mixer.music.unpause()
                for i, ball in enumerate(balls):
                    if ball.y < self.height - 60:
                        ball.draw_ball(
                            self.screen, color.GREEN, i, ball.x, ball.y, trails
                        )

                self.show_score(color)

                if (
                    current_time - self.last_special_ball_time
                    > self.special_ball_time - 1
                ):
                    special_ball_text = font.render(
                        "Special Ball Ready (UP)", True, color.GREEN
                    )
                else:
                    remaining_time = max(
                        0,
                        self.special_ball_time
                        - (current_time - self.last_special_ball_time),
                    )
                    special_ball_text = font.render(
                        f"Special Ball in {int(remaining_time)}s", True, color.WHITE
                    )

                if current_time - self.last_x_time > self.random_destruction_time - 1:
                    countdown_text = font.render(
                        "Brick Destruction Ready (DOWN)", True, color.GREEN
                    )
                    self.screen.blit(
                        countdown_text,
                        (
                            (self.width - countdown_text.get_width() - 20) * self.scale,
                            (self.height - 30) * self.scale,
                        ),
                    )
                else:
                    time_until_destruction = max(
                        0,
                        self.random_destruction_time
                        - (current_time - self.last_x_time),
                    )
                    countdown_text = font.render(
                        f"Brick Destruction in {int(time_until_destruction)}s",
                        True,
                        color.WHITE,
                    )
                    self.screen.blit(
                        countdown_text,
                        (
                            (self.width - countdown_text.get_width() - 20) * self.scale,
                            (self.height - 30) * self.scale,
                        ),
                    )

                pygame.draw.line(
                    self.screen,
                    color.WHITE,
                    (0, self.height - 50),
                    (self.width, self.height - 50),
                    2,
                )
                self.screen.blit(
                    special_ball_text,
                    (20 * self.scale, (self.height - 30) * self.scale),
                )

                pygame.draw.line(
                    self.screen,
                    color.WHITE,
                    (0, self.height - 50),
                    (self.width, self.height - 50),
                    2,
                )

                pygame.display.flip()
