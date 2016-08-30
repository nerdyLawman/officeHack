import libtcodpy as libtcod
import gameconfig
from interface.helpers import menu

def main_menu():
    # start game menu - logic handled in officehack.py

    #background image for menu
    img = libtcod.image_load('data/img/bg.png')
    libtcod.image_blit_2x(img, 0, 0, 0)

    # title
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_set_default_background(0, libtcod.flame)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-4, libtcod.BKGND_SET, libtcod.CENTER,
        gameconfig.GAME_TITLE)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-3, libtcod.BKGND_SET, libtcod.CENTER,
        gameconfig.GAME_AUTHOR)

    return menu('', ['New Game', 'Continue', 'Quit'], 24)

def inventory_menu(header, inventory):
    # inventory menu
    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.owner.name for item in inventory]
    index = menu(header, options, gameconfig.INVENTORY_WIDTH)
    if index is None or len(inventory) == 0: return None
    return inventory[index]


def conversation(header):
    # basic test conversation
    responses = ['yeah.', 'I guess.', 'sure do.', 'maybe?', 'no way.']
    index = menu(header, responses, gameconfig.INVENTORY_WIDTH)
    if index is None or len(responses) == 0: return None
    return responses[index]