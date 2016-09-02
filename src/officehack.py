import libtcodpy as libtcod
import gameconfig
from interface.menus import main_menu
from interface.helpers import message, message_box
from game.states import new_game, play_game, save_game, load_game
from game import game_messages


#TEST DIALOGUE
from dialogue.dialogues import level_1
from dialogue.helpers import init_dialogue
init_dialogue(level_1['test'])

choice = main_menu()

while not libtcod.console_is_window_closed():
    if choice == 0:
        new_game()
        message(game_messages.WELCOME_MESSAGE, libtcod.red)
        play_game()
        break
    if choice == 1:
        try:
            load_game()
        except:
            message_box(game_messages.NO_LOAD_DATA, 24)
            continue
        play_game()
    elif choice == 2:
        break
