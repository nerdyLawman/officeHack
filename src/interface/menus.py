from libtcod import libtcodpy as libtcod
import gameconfig
import time
import textwrap
from game import game_messages
from interface.rendering import message, render_drone_filter
from objects.actions import random_from_except
from terminal.cli import cli_window

# ---------------------------------------------------------------------
# [ MENU FUNCTIONS ] --------------------------------------------------
# ---------------------------------------------------------------------
def highlight_selection(window, bgnd_color, sel_color, selected, width, height, header_height, x, y):
    # highlights menu line corresponding to selected
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SET)
    libtcod.console_set_default_background(window, sel_color)
    libtcod.console_rect(window, 0, selected+header_height, width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
    libtcod.console_flush()


def menu(header, options, width=gameconfig.MENU_WIDTH, bgnd_color=None, fgnd_color=None, sel_color=None):
    # base selection menu
    
    # color inits
    if bgnd_color is None: bgnd_color = gameconfig.MENU_BKGND
    if fgnd_color is None: fgnd_color = libtcod.white
    if sel_color is None: sel_color = gameconfig.MENU_SELECT_BKGND

    if len(options) > gameconfig.MAX_MENU_OPTIONS: raise ValueError(game_messages.MENU_OVER)

    # calculate total height for the header (after auto-wrap) and one line per option
    header += '\n\n'
    header_height = libtcod.console_get_height_rect(gameconfig.con, 0, 0, width, gameconfig.SCREEN_HEIGHT, header)
    if header == '\n\n': header_height = 1 # if no header
    height = len(options) + header_height + 1

    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SCREEN)

    #print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, fgnd_color)
    libtcod.console_print_rect_ex(window, 1, 1, width-2, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 1, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    #blit window contents
    x = gameconfig.SCREEN_WIDTH/2 - width/2
    y = gameconfig.SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)

    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    selected = 0
    while True:
        key = libtcod.console_wait_for_keypress(True)

        if options: # selection loop
            if key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_UP:
                
                if key.vk == libtcod.KEY_DOWN:
                    if selected < len(options): selected += 1
                    else: selected = 1
                
                if key.vk == libtcod.KEY_UP:
                    if selected > 1: selected -= 1
                    else: selected = len(options)

                # hightlight selected option
                highlight_selection(window, bgnd_color, sel_color, selected-1, width, height, header_height, x, y)

            if key.vk == libtcod.KEY_ENTER:
                if selected == 0: selected = 1
                highlight_selection(window, bgnd_color, sel_color, selected-1, width, height, header_height, x, y)
                time.sleep(0.1) # give it a beat
                return(selected-1)

            # convert ascii to index
            index = key.c - ord('a')
            if index >= 0 and index < len(options):
                selected = index
                # hightlight selected option
                highlight_selection(window, bgnd_color, sel_color, selected, width, height, header_height, x, y)
                time.sleep(0.1)
                return index

        if key.vk == libtcod.KEY_ESCAPE:
            return None


# ---------------------------------------------------------------------
# [ SPECIFIC MENUS ] --------------------------------------------------
# ---------------------------------------------------------------------
def main_menu():
    # start game menu - logic handled in officehack.py
    #background image for menu
    img = libtcod.image_load('data/img/bg.png')
    libtcod.image_blit_2x(img, 0, 0, 0)

    # title
    libtcod.console_set_default_foreground(0, gameconfig.TITLE_FRGND)
    libtcod.console_set_default_background(0, gameconfig.TITLE_BKGND)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-4,
        libtcod.BKGND_SET, libtcod.CENTER, gameconfig.GAME_TITLE)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-3,
        libtcod.BKGND_SET, libtcod.CENTER, gameconfig.GAME_AUTHOR)

    return menu('', ['New Game', 'Continue', 'Quit'], gameconfig.MAIN_MENU_WIDTH)


def inventory_menu(header, inventory):
    # inventory menu
    if len(inventory) == 0: options = [game_messages.EMPTY_INVENTORY]
    else: options = [item.inv_id + ' [' + str(item.count) +']' for item in inventory]
    index = menu(header, options)
    if index is None or len(inventory) == 0: return None
    return inventory[index].item


def terminal_menu(station):
    # computer terminal station
    gameconfig.player_at_computer = True
    header = game_messages.TERMINAL_WELCOME + station.owner.name # give it a name eventually
    options = ['read_', 'write_', 'remote_', 'drone_']
    
    index = menu(header, options, bgnd_color=gameconfig.TERMINAL_BKGND,
        fgnd_color=gameconfig.TERMINAL_FRGND, sel_color=gameconfig.TERMINAL_SELECT_BKGND)
    
    if index is None: return
    
    # READ ----------------------------
    if options[index] == 'read_':
        floppy = next((inv for inv in gameconfig.player.player.inventory if inv.inv_id == 'floppy disc'), None)
        if floppy is not None: cli_window('read', floppy)
        else: cli_window('read')
    
    # WRITE ----------------------------
    if options[index] == 'write_':
        cli_window()
        
    # REMOTE --------------------------
    if options[index] == 'remote_':
        cli_window('remote')
    
    # DRONE ---------------------------
    if options[index] == 'drone_' and gameconfig.player.fighter.drone is False:
        cli_window('drone')

    gameconfig.player_at_computer = False


# ---------------------------------------------------------------------
# [ EXTRA MENUS ] -----------------------------------------------------
# ---------------------------------------------------------------------
def message_box(text, width=gameconfig.MENU_WIDTH):
    # popup message box
    menu(text, [], width)
