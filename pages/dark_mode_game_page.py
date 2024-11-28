import random
import sys
import time
import pygame
from helpers.constants import ball_radius, bottom_font, font
from models import (
    Ball,
    Color,
    Player,
    SpecialBall,
    draw_bricks,
    drop_powerup,
    create_new_bricks,
)
from .pages import Page


class DarkModeGame(Page):
    inactivity_threshold = 5
    special_ball_time = 20
    random_destruction_time = 60

    def __init__(self, screen, height, width, scale, game) -> None:
        super().__init__(screen, height, width, scale, game)
        self.fonts = (pygame.font.SysFont(None, int(42 * self.scale)),)
        self.score = 0
        self.powerups = []
        self.special_balls = []
        self.running = True
        self.color = Color(
            BLACK=(
                max(Color.BLACK[0] - 25, 0),
                max(Color.BLACK[1] - 25, 0),
                max(Color.BLACK[2] - 36, 0),
            ),
            RED=(
                min(Color.RED[0] - 225, 0),
                max(Color.RED[1] - 125, 0),
                max(Color.RED[2] - 130, 0),
            ),
            BLUE=(
                min(Color.BLUE[0] - 120, 0),
                min(Color.BLUE[1] - 170, 0),
                max(Color.BLUE[2] - 210, 0),
            ),
            GREEN=(
                max(Color.GREEN[0] - 130, 0),
                max(Color.GREEN[1] - 215, 0),
                max(Color.GREEN[2] - 120, 0),
            ),
            YELLOW=(
                min(Color.YELLOW[0] - 230, 0),
                min(Color.YELLOW[1] - 215, 0),
                min(Color.YELLOW[2] - 160, 0),
            ),
        )
        self.bricks = create_new_bricks(self.color)
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

    def pause_game(self, clock):
        paused = True
        pause_text = self.fonts[0].render(
            "Game Paused. Press 'P' to Resume.", True, self.color.WHITE
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

            clock.tick(60)

    def show_score(self):
        score = self.score
        text = font.render(f"Score: {score}", True, Color.RED)
        self.screen.blit(
            text,
            (
                (self.width // 2 - text.get_width() / 2) * self.scale,
                (self.height - 30) * self.scale,
            ),
        )

    def game_over(self, score):
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
        self.screen.fill(Color.BLACK)
        font_for_game_over = self.fonts[0]
        text = font_for_game_over.render(
            "Game Over! Press ENTER to restart", True, Color.RED
        )
        highscore = self.update_db("Dark", score)
        text2 = font_for_game_over.render(
            f"High Score = {[score, highscore][highscore > score]}",
            True,
            [Color.GREEN, Color.YELLOW][highscore > score],
        )
        text3 = font_for_game_over.render(f"Your Score = {score}", True, Color.YELLOW)

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
            "Press Shift to go to Main Window", True, Color.GREY
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

    def runner(self, brick_height, brick_width, trails, clock):
        self.score = 0
        self.bricks = create_new_bricks(self.color)
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

        dt = 0
        clock.tick(60)
        while self.running:
            self.screen.fill(self.color.BLACK)
            # dt = min(0.02, clock.tick(60) / 1000)
            current_time = time.time()

            if len(self.bricks) == 0:
                self.bricks = create_new_bricks(self.color)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if current_time - self.last_move_time > self.inactivity_threshold:
                if self.player.x_start <= self.width // 2:
                    self.player.x_start += 5 * self.player.player_speed * dt
                else:
                    self.player.x_start -= 5 * self.player.player_speed * dt
                self.last_move_time = current_time

            if keys[pygame.K_RCTRL]:
                self.pause_game(clock)

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
                > self.special_ball_time - 1
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

            if (
                keys[pygame.K_DOWN] or keys[pygame.K_s]
            ) and current_time - self.last_x_time > self.random_destruction_time - 1:
                for _ in range(5):
                    if self.bricks:
                        random_brick = random.choice(self.bricks)
                        self.bricks.remove(random_brick)
                        self.score += 10
                if self.game.music_is_playing:
                    pygame.mixer.music.pause()
                    self.game.music_files[1].play()
                self.last_x_time = current_time

            if keys[pygame.K_RSHIFT]:
                self.balls = [
                    Ball(
                        screen=self.screen,
                        height=self.height,
                        width=self.width,
                        scale=self.scale,
                    )
                ]
                self.player = Player(
                    screen=self.screen,
                    height=self.height,
                    width=self.width,
                    scale=self.scale,
                )
                return True

            for ball in self.balls:
                ball.x, ball.y, ball.dx, ball.dy = ball.move_ball(dt, self.player)

            if all(ball.y >= self.height - 60 for ball in self.balls):
                user_exited = self.game_over(self.score)
                if user_exited:
                    self.balls = [
                        Ball(
                            screen=self.screen,
                            height=self.height,
                            width=self.width,
                            scale=self.scale,
                        )
                    ]
                    self.player = Player(
                        screen=self.screen,
                        height=self.height,
                        width=self.width,
                        scale=self.scale,
                    )
                    return True
                else:
                    self.balls = [
                        Ball(
                            screen=self.screen,
                            height=self.height,
                            width=self.width,
                            scale=self.scale,
                        )
                    ]
                    self.player = Player(
                        screen=self.screen,
                        height=self.height,
                        width=self.width,
                        scale=self.scale,
                    )
                    break

            if current_time - self.last_brick_move_time > 1:
                for brick in self.bricks:
                    brick.y += brick.speed * dt
                    if brick.y + brick.height >= self.height:
                        user_exited = self.game_over(self.score)
                        if user_exited:
                            return True
                        else:
                            break
                self.last_brick_move_time = current_time

            bricks_to_remove = []
            for brick in self.bricks:
                for ball in self.balls:
                    if (
                        brick.x < ball.x < brick.x + brick.width
                        and brick.y < ball.y < brick.y + brick.height
                    ):
                        bricks_to_remove.append(brick)
                        self.score += 10
                        powerup = drop_powerup(
                            brick.x, brick.y, self.powerups, self.scale, self.color
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
                            brick.x, brick.y, self.powerups, self.scale, self.color
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
                    self.player.x_start < powerup.x + powerup.width
                    and self.player.x_start + self.player.player_width > powerup.x
                    and self.player.y_start < powerup.y + powerup.height
                    and self.player.y_start + self.player.player_height > powerup.y
                ):
                    self.powerups.remove(powerup)
                    if powerup.type == "extra_ball":
                        self.balls.append(
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
                    special_ball.draw(self.screen, ball_radius, self.color)

                if (
                    special_ball.x < 0
                    or special_ball.x > self.width
                    or special_ball.y < 0
                    or special_ball.y > self.height
                ):
                    self.special_balls.remove(special_ball)

            draw_bricks(self.bricks, self.screen)
            self.player.draw_player(self.color)

            if self.game.music_is_playing:
                if (
                    not self.special_balls
                    or current_time - self.last_special_ball_time >= 2
                ):
                    self.game.music_files[0].stop()
                    pygame.mixer.music.unpause()
                if current_time - self.last_x_time >= 3:
                    self.game.music_files[1].stop()
                    pygame.mixer.music.unpause()
            for i, ball in enumerate(self.balls):
                if ball.y < self.height - 60:
                    ball.draw_ball(
                        self.screen, self.color.GREEN, i, ball.x, ball.y, trails
                    )

            self.show_score()

            if current_time - self.last_special_ball_time > self.special_ball_time - 1:
                special_ball_text = font.render(
                    "Special Ball Ready (UP)", True, Color.GREEN
                )
            else:
                remaining_time = max(
                    0,
                    self.special_ball_time
                    - (current_time - self.last_special_ball_time),
                )
                special_ball_text = font.render(
                    f"Special Ball in {int(remaining_time)}s", True, Color.WHITE
                )

            if current_time - self.last_x_time > self.random_destruction_time - 1:
                countdown_text = font.render(
                    "Brick Destruction Ready (DOWN)", True, Color.GREEN
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
                    self.random_destruction_time - (current_time - self.last_x_time),
                )
                countdown_text = font.render(
                    f"Brick Destruction in {int(time_until_destruction)}s",
                    True,
                    Color.WHITE,
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
                Color.WHITE,
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
                Color.WHITE,
                (0, self.height - 50),
                (self.width, self.height - 50),
                2,
            )

            pygame.display.flip()
            dt = clock.tick(60) / 1000
