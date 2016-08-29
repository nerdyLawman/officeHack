import libtcodpy as libtcod
import gameconfig
from interface.menus import main_menu
from interface.helpers import message, message_box
from game.states import new_game, play_game, save_game
from game import game_messages

choice = main_menu()

while not libtcod.console_is_window_closed():
    if choice == 0:
        new_game()
        message(game_messages.WELCOME_MESSAGE, libtcod.red)
        play_game()
    if choice == 1:
        try:
            load_game()
        except:
            message_box(game_messages.NO_LOAD_DATA, 24)
            continue
        play_game(player, objects)
    elif choice == 2:
        break
