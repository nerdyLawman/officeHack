import libtcodpy as libtcod

# TEMP GAME VARIABLES SPOT
start_npc_count = 0
npc_count = 0
start_item_count = 0
item_count = 0

#fighter hp=6, defense=0, power=2, xp=10
jeff = { 'char' : 'D',
    'name' : 'Jeff',
    'color' : libtcod.sky,
    'hp' : 6,
    'defense' : 0,
    'power' : 2,
    'xp' : 10,
    'chance' : 70,
}

sophie = { 'char' : 'E',
    'name' : 'Sophie',
    'color' : libtcod.magenta,
    'hp' : 10,
    'defense' : 0,
    'power' : 3,
    'xp' : 15,
    'chance' : 25,
}

alan = { 'char' : 'A',
    'name' : 'Alan',
    'color' : libtcod.lime,
    'hp' : 30,
    'defense' : 0,
    'power' : 6,
    'xp' : 45,
    'chance' : 5,
}

level_npcs = [ jeff, sophie, alan ]


floppy_disc =   { 'char' : '!',
    'name' : 'floppy disc',
    'color' : libtcod.light_lime,
    'use' : None,
    'chance': 80
}

document = { 'char' : '#',
    'name' : 'document',
    'color' : libtcod.lightest_sepia,
    'use' : None,
    'chance' : 10
}

coffee = { 'char' : '0',
    'name' : 'coffee',
    'color' : libtcod.dark_sepia,
    'use' : None,
    'chance' : 10
}

level_items = [ floppy_disc, document, coffee ]

# GAME TITLE
CONSOLE_TITLE = 'offICE_HACK//'
GAME_TITLE = 'Office_HACK'
GAME_AUTHOR = 'Nord Mulman & Chairvan Arocstore'

# MESSAGES
WELCOME_MESSAGE = 'Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.'

# SCREEN
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

# MAP SIZE
MAP_WIDTH = 80
MAP_HEIGHT = 43

# ROOMS
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_NPCS = 3
MAX_ROOM_ITEMS = 2

# FOV
FOV_ALGO = 2
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 8

# INTERFACE
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
INVENTORY_WIDTH = 50
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

#EXP AND LV
LEVEL_UP_BASE = 100
LEVEL_UP_FACTOR = 50

# SPELLS
LIGHTNING_RANGE = 5
LIGHTNING_DAMAGE = 10
FIREBALL_RADIUS = 4
FIREBALL_DAMAGE = 11
CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8
HEAL_AMOUNT = 6

# COLORS
STAIRS_COLOR = libtcod.black
MENU_BKGND = libtcod.black
MENU_SELECT_BKGND = libtcod.amber

# THEMES
DEFAULT_THEME = { 'color_dark_wall' : libtcod.Color(0, 0, 100),
    'color_light_wall' : libtcod.Color(130, 110, 50),
    'color_dark_ground' : libtcod.Color(50, 50, 100),
    'color_light_ground' : libtcod.Color(200, 180, 50),
}

DARK_THEME = {'color_dark_wall' : libtcod.darker_gray,
    'color_light_wall' : libtcod.gray,
    'color_dark_ground' : libtcod.darkest_gray,
    'color_light_ground' : libtcod.dark_gray,
}

RED_THEME = {'color_dark_wall' : libtcod.darker_red,
    'color_light_wall' : libtcod.red,
    'color_dark_ground' : libtcod.darker_flame,
    'color_light_ground' : libtcod.flame,
}

BLUE_THEME = {'color_dark_wall' : libtcod.darker_azure,
    'color_light_wall' : libtcod.sky,
    'color_dark_ground' : libtcod.darker_han,
    'color_light_ground' : libtcod.azure,
}

COLOR_THEMES = [ DEFAULT_THEME, DARK_THEME, RED_THEME, BLUE_THEME ]
