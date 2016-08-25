import libtcodpy as libtcod
from helpers import menu
from game.states import new_game, play_game, load_game

def main_menu():
    #img = libtcod.image_load('bgk.png')
    while not libtcod.console_is_window_closed():
        choice = menu('', ['New Game', 'Continue', 'Quit'], 24)
        if choice == 0:
            new_game()
            play_game()
        if choice == 1:
            try:
                load_game()
            except:
                message_box('\n No saved gamedata to load.\n', 24)
                continue
            play_game()
        elif choice == 2:
            break

def inventory_menu(header):
    # inventory
    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.name for item in inventory]
    index = 'no selection'
    #return selected item
    while index == 'no selection':
        index = menu(header, options, INVENTORY_WIDTH)
    if index is None or len(inventory) == 0: return None
    return inventory[index].item
