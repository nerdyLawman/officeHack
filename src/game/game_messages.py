from libtcod import libtcodpy as libtcod
import gameconfig

# GAME MESSAGES
DEFINED_MESSAGES = {
    'WELCOME_MESSAGE' : ['Welcome to your NEW JOB.', libtcod.flame],
    'LEVEL_REST_MESSAGE' : ['You take a moment to lay low.', libtcod.sky],
    'LEVEL_CONTINUE_MESSAGE' : ['You decide to continue probing deeper.', libtcod.flame],
    'WAIT_TURN_MESSAGE' : ['You WAIT a turn for the PARANOIA to close in on you.', libtcod.flame],
    'FULL_INVENTORY' : ['Your INVENTORY is FULL! You can\'t PICK UP: ', libtcod.yellow],
    'DROPPED_MESSAGE' : ['You DROPPED a ', libtcod.yellow],
}
PLAYER_LEVEL_UP = 'Your skills increase. LEVEL UP! Now at level: '
MENU_OVER = 'Cannot have a MENU with more than 26 OPTIONS!'

# MESSAGE BOXES
NO_LOAD_DATA = 'No saved gamedata to load.'
EMPTY_INVENTORY = 'INVENTORY is EMPTY.'

# TERMINALS MESSAGES
TERMINAL_WELCOME = 'Welcome to '
TERMINAL_TITLE = 'HAPPY TERMINAL V1.0 - 1993'
TERMINAL_START_MESSAGE = 'Enter a command to begin. Help for options.'

# MENU HEADERS
HELP_HEADER = 'PRESS the key next to any of the OPTIONS for more INFORMATION'
INVENTORY_HEADER = 'PRESS the KEY next to an ITEM to USE it, or ESC to CANCEL'
DROP_HEADER = 'PRESS the KEY next to an ITEM to DROP it'
LOOK_HEADER = 'SELECT an OBJECT in you FOV for more INFORMATION'
