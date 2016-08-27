import libtcodpy as libtcod
import gameconfig
from interface.menus import main_menu
from interface.interfaceconfig import initialize_interface
from interface.helpers import message, message_box
from game.states import new_game, play_game, save_game

con, panel, game_msgs = initialize_interface() #setup screen here

choice = main_menu()

while not libtcod.console_is_window_closed():
    if choice == 0:
        key, mouse, inventory, player, objects, level_map, stairs, fov_map, fov_recompute = new_game()
        message(gameconfig.WELCOME_MESSAGE, libtcod.red)
        play_game(player, objects, level_map, fov_map, key, mouse, con, panel)
    if choice == 1:
        try:
            load_game()
        except:
            message_box('\n No saved gamedata to load.\n', 24)
            continue
        play_game(player, objects, key, mouse)
    elif choice == 2:
        break
