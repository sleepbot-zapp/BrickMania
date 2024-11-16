import random
from loading_combinations import functions
import pygame


def runner(main_menu, loading_screen, main_game, type_=0, is_paused=True):
    is_paused = True
    if not type_:
        selected_option = main_menu(is_paused)
    while True:
        if type_:
            selected_option = main_menu(is_paused)
            type_ = 0
        # sec = lambda x : 1/math.cos(x)
        # cosec = lambda x : 1/math.sin(x)
        # cot = lambda x : 1/math.tan(x)
        # inv_sinh = lambda x : 1/math.sinh(x)
        # inv_cosh = lambda x : 1/math.cosh(x)
        # inv_tanh = lambda x : 1/math.tanh(x)
        # for i in combs:
        #     print(*i)
        #     loading_screen(*i)
        if selected_option == 0:
            def gen_spinner():
                try:
                    loading_screen(random.choice(functions), random.choice(functions))
                except (ZeroDivisionError, ValueError, OverflowError):
                    gen_spinner()
            gen_spinner()
            main_game(is_paused)
        if selected_option == 1:
            if not is_paused: # True
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(-1)
            is_paused = not is_paused
            selected_option = main_menu(is_paused)
        if selected_option==2: 
            """auto_screen_window(WIDTH, HEIGHT, dummy_text)"""
            selected_option = main_menu(is_paused)