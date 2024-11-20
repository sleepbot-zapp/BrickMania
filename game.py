from helpers.constants import (
    HEIGHT, WIDTH, SCALE,
    track, track1, track2, track3
)
from models import Player, Ball, Color
import time
import sys
from pages.main_menu_page import MainMenu
from pages.settings_page import Settings
import pygame

class Game:
    def __init__(self, *, height=HEIGHT, width=WIDTH, scale=SCALE,) -> None:
        pygame.init()
        # window
        self.height = height
        self.width = width
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width, self.height))
        # colors
        self.colors = Color()
        # entities
        self.player = Player(screen=self.screen, height=self.height, width=self.width, scale=self.scale)
        self.balls = [Ball(screen=self.screen, height=self.height, width=self.width, scale=self.scale)]
        # game variables
        self.clock = pygame.time.Clock()
        self.music_files = track, track1, track2, track3
        self.music_is_playing = False
        self.keys = pygame.key.get_pressed()
        # entity variables
        self.trails = []
        # pages
        self.main_menu = MainMenu(self.screen, self.height, self.width, self.scale)
        self.settings_page = Settings(self.screen, self.height, self.width, self.scale)
        

    def gameloop(self):
        while True:
            if self.music_is_playing:
                pygame.mixer.music.load("./assets/music.mp3")
                pygame.mixer.music.play(-1)
            self.screen.fill(self.colors.BLACK)
            dt = self.clock.tick(60) / 1000
            current_time = time.time()
            # selected_option = self.main_menu.generate(self.colors, 80, 20, self.clock)
            self.settings_page.display(self.colors)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  
            # if selected_option == 1:
            #     if self.music_is_playing:
            #         pygame.mixer.music.stop()
            #     else:
            #         pygame.mixer.music.play(-1)
            #     self.music_is_playing = not self.music_is_playing


            
            


a = Game()
a.gameloop()
