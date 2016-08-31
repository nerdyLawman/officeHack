import libtcodpy as libtcod
import gameconfig
from interface.helpers import menu, cli_window

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

    return menu('', ['New Game', 'Continue', 'Quit'], gameconfig.MAIN_MENU_WIDTH)

def inventory_menu(header, inventory):
    # inventory menu
    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = []
        for item in inventory:
            options.append(item.inv_id + ' [' + str(item.count) +']')
    index = menu(header, options)
    if index is None or len(inventory) == 0: return None
    return inventory[index].item

def terminal(header=''):
    # computer terminal
    header = 'Welcome to TERMINAL-A' # give it a name eventually
    options = ['read_', 'write_', 'save_']
    index = menu(header, options, bgnd_color=libtcod.dark_azure,
        fgnd_color=libtcod.lighter_sky, sel_color=libtcod.light_azure)
    if options[index] == 'write_':
        cli_window()

def conversation(header, npc_name):
    # basic test conversation

    # messy portrait bullshit
    img = libtcod.image_load('data/img/portrait2x.png') # this should ultimately be an attribute the object posesses.
    portrait = libtcod.console_new(50, 20)
    libtcod.console_set_default_background(portrait, gameconfig.MENU_BKGND)
    libtcod.console_set_default_foreground(portrait, libtcod.white)
    libtcod.console_rect(portrait, 0, 0, 50, 20, False, libtcod.BKGND_SET)
    libtcod.console_print_ex(portrait, 10, 10, libtcod.BKGND_NONE, libtcod.LEFT, npc_name)
    #libtcod.image_blit_rect(img, portrait, 1, 1, -1, -1, libtcod.BKGND_SET) #1x size 8x10
    libtcod.image_blit_2x(img, portrait, 1, 1, 0, 0, -1, -1) #2x size 16x20
    libtcod.console_blit(portrait, 0, 0, 50, 20, 0, gameconfig.SCREEN_WIDTH/2-25, gameconfig.SCREEN_HEIGHT/2-16, 1.0, 1.0)

    responses = ['yeah.', 'I guess.', 'sure do.', 'maybe?', 'no way.']
    index = menu(header, responses)
    if index is None or len(responses) == 0: return None
    return responses[index]
