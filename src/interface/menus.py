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


def conversation(header, npc_name):
    # basic test conversation
    img = libtcod.image_load('data/img/portrait2.png')
    portrait = libtcod.console_new(50, 20)
    libtcod.console_set_default_background(portrait, gameconfig.MENU_BKGND)
    libtcod.console_set_default_foreground(portrait, libtcod.white)
    libtcod.console_rect(portrait, 0, 0, 50, 20, False, libtcod.BKGND_SET)
    libtcod.console_print_ex(portrait, 10, 10, libtcod.BKGND_NONE, libtcod.LEFT, npc_name)
    libtcod.image_blit_rect(img, portrait, 1, 1, -1, -1, libtcod.BKGND_SET)
    libtcod.console_blit(portrait, 0, 0, 50, 20, 0, gameconfig.SCREEN_WIDTH/2-25, gameconfig.SCREEN_HEIGHT/2-16, 1.0, 1.0)
    responses = ['yeah.', 'I guess.', 'sure do.', 'maybe?', 'no way.']
    index = menu(header, responses, gameconfig.INVENTORY_WIDTH)
    if index is None or len(responses) == 0: return None
    return responses[index]
