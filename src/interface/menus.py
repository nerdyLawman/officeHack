import libtcodpy as libtcod
from interface.helpers import menu
#from game.states import new_game, play_game, load_game

def inventory_menu(header):
    # inventory
    # NEEDS: inventory
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
