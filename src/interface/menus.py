import libtcodpy as libtcod
import gameconfig
from interface.helpers import menu

def main_menu():
    # start game menu - logic handled in officehack.py
    #img = libtcod.image_load('bgk.png') #background image for menu
    return menu('', ['New Game', 'Continue', 'Quit'], 24)

def inventory_menu(header, inventory):
    # inventory menu
    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.owner.name for item in inventory]
    index = 'no selection'
    #return selected item
    while index == 'no selection':
        index = menu(header, options, gameconfig.INVENTORY_WIDTH)
    if index is None or len(inventory) == 0: return None
    return inventory[index]