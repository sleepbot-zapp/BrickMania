from random import choice
from helpers.loading_combinations import combs
from helpers.constants import font
from pygame.mixer import music
from pages.auto_scroll import auto_screen_window

def runner(main_menu, loading_screen, main_game, type_=0): #, is_paused=True
    # is_paused = True
    if not type_:
        selected_option = main_menu() #is_paused
    while True:
        if type_:
            selected_option = main_menu() #is_paused
            type_ = 0
        if selected_option == 0:
            loading_screen(*(choice(combs)))
            main_game(font) #is_paused
        if selected_option == 1:
            # if not is_paused: # True
            #     music.stop()
            # else:
            #     music.play(-1)
            # is_paused = not is_paused
            selected_option = main_menu() #is_paused
        if selected_option==2: 
            selected_option = auto_screen_window() #is_paused


        # sec = lambda x : 1/math.cos(x)
        # cosec = lambda x : 1/math.sin(x)
        # cot = lambda x : 1/math.tan(x)
        # inv_sinh = lambda x : 1/math.sinh(x)
        # inv_cosh = lambda x : 1/math.cosh(x)
        # inv_tanh = lambda x : 1/math.tanh(x)
        # for i in combs:
        #     print(*i)
        #     loading_screen(*i)
        