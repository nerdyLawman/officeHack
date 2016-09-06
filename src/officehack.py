from libtcod import libtcodpy as libtcod
import gameconfig
from interface.menus import main_menu, message_box
from interface.rendering import message, fetch_message
from game.states import new_game, play_game, save_game, load_game
from game import game_messages
from sound.SoundPlayer import SoundPlayer

choice = main_menu()


while not libtcod.console_is_window_closed():
    # NEW GAME
    if choice == 0:
        new_game()
        fetch_message('WELCOME_MESSAGE')
        play_game()
        break
    # CONTINUE
    elif choice == 1:
        try:
            load_game()
        except:
            message_box(game_messages.NO_LOAD_DATA)
            continue
        play_game()
    # QUIT
    elif choice == 2:
        break
    # SOMETHING UNEXPECTED HAPPEND!
    else: break
