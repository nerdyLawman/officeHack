from libtcod import libtcodpy as libtcod

# GAME INFO -----------------------------
CONSOLE_TITLE = 'offICE_HACK//'
GAME_TITLE = 'Office_HACK'
GAME_AUTHOR = 'Nord Mulman & Chairvan Arocstore'

# SCREEN --------------------------
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

# LIBTCOD SETTINGS ---------------------------------------
libtcod.console_set_custom_font('data/fonts/arial10x10.png',
    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, CONSOLE_TITLE, False)
libtcod.sys_set_fps(LIMIT_FPS) #FPS

# MAP SIZE ----------------------------
MAP_WIDTH = 80
MAP_HEIGHT = 43

# FOV ------------------------------
FOV_ALGO = 2
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 8

# ROOMS ---------------------------
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_NPCS = 3
MAX_ROOM_ITEMS = 2

# INTERFACE VARS -----------------------------
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
INVENTORY_WIDTH = 50
MAIN_MENU_WIDTH = 30
MENU_WIDTH = 50
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

# CONSOLES ----------------------------------
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
filter = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# CONTROLLERS ------------------------------------------
key = libtcod.Key()
mouse = libtcod.Mouse()


# ---------------------------------------------------------------------
# [ GAME STATE VARIABLES ] --------------------------------------------
# ---------------------------------------------------------------------

# LEVEL PUBLIC ACCESS ---------------------------------
objects = []
level_map = None
fov_map = None
color_theme = None
stairs_up = None
stairs_down = None
game_msgs = []
game_level = 1
game_levels = []
level_npc_count = npc_count = 0
level_item_count = item_count = 0

# LEVEL-OBJECT EASY-ACCESS -----------------------------
level_terminals = []
level_drones = []

# PLAYER VARIABLES ----------------------------------
player = None
real_player = None
real_inventory = []
saved_discs = []

# DRONE VARIABLE --------------------------
drone_holder = None

# STATUS FLAGS -----------------------------
player_at_computer = False
remote_target = None

# FILTER FLAGS ----------------------------
DRONE_FLAG = False
REMOTE_FLAG = False
VISION_FLAG = None # takes an image unlike the other two

# ---------------------------------------------------------------------
# [ VOLUME CONFIG VARIABLES ] -----------------------------------------
# ---------------------------------------------------------------------

SOUND = 'enabled' # 'enabled', 'disabled'

VOLUME = {
    'MUSIC': 0.0,
    'SOUND_FX': 0.0
}

CURRENT_TRACK = None

BACKGROUND_MUSIC = {
  'terminal': 'terminal',
  'level_1' : 'intro'
}

## if sound type has multiple randomly generated effects, include name prefix and
## the number of files with the given prefix. if there is only one file associated
## with the sound type, include the filename minus the extension as a string.

SOUND_FX = {
   'dialogue': {
       'name': 'blip',
       'number': 6
   },
   'attack': {
       'name': 'hit',
       'number': 3
   }
}

# ---------------------------------------------------------------------
# [ GAMEPLAY CONFIG VARIABLES ] ---------------------------------------
# ---------------------------------------------------------------------

# PLAYER VARIABLES ------------------------------
START_HP = 50
START_DEFENSE = 1
START_POWER = 5
HERO_CHAR = '@'
HERO_NAME = 'Hero Protagonist'
HERO_COLOR = libtcod.white

# INVENTORY -----------------------
MAX_INVENTORY = 26

# MENUS --------------------------
MAX_MENU_OPTIONS = 26

# TERMINAL ---------------------------
TERMINAL_CURSOR = '_'
TERMINAL_PROMPT = '$ '

# STATUS --------------------------------------------
CONFUSE_NUM_TURNS = 5
REPULSED_NUM_TURNS = 7
COFFEE_RANGE = 4
TALK_RECHARGE = 7
TALK_RANGE = 2

#EXP AND LV -----------------------------
LEVEL_UP_BASE = 50
LEVEL_UP_FACTOR = 50
LEVEL_HEAL_AMOUNT = 20


# ---------------------------------------------------------------------
# [ COLOR CONFIG VARIABLES ] ------------------------------------------
# ---------------------------------------------------------------------

# COLOR DEFINITIONS ---------------------------------------
TITLE_FRGND = libtcod.light_yellow
TITLE_BKGND = libtcod.flame

TERMINAL_BKGND = libtcod.dark_azure
TERMINAL_FRGND = libtcod.lighter_sky
TERMINAL_SELECT_BKGND = libtcod.light_azure

STAIRS_COLOR = libtcod.black
LEVEL_BKGND = libtcod.black
MENU_BKGND = libtcod.darkest_gray
MENU_SELECT_BKGND = libtcod.amber

GAME_UPDATE_COLOR = libtcod.light_cyan
CAUTION_COLOR = libtcod.light_orange

DRONE_FILTER_COLOR = libtcod.green
REMOTE_FILTER_COLOR = libtcod.red

# BASIC COLORS --------------------------------
WHITE = libtcod.white
BLACK = libtcod.black
GREY = libtcod.grey
SEPIA = libtcod.sepia
RED = libtcod.red
FLAME = libtcod.flame
ORANGE = libtcod.orange
AMBER = libtcod.amber
YELLOW = libtcod.yellow
LIME = libtcod.lime
CHARTREUSE = libtcod.chartreuse
GREEN = libtcod.green
SEA = libtcod.sea
TURQUOISE = libtcod.turquoise
CYAN = libtcod.cyan
SKY = libtcod.sky
AZURE = libtcod.azure
BLUE = libtcod.blue
HAN = libtcod.han
VIOLET = libtcod.violet
PURPLE = libtcod.purple
FUCHSIA = libtcod.fuchsia
MAGENTA = libtcod.magenta
PINK = libtcod.pink
CRIMSON = libtcod.crimson


# ---------------------------------------------------------------------
# [ DEBUG ] -----------------------------------------------------------
# ---------------------------------------------------------------------
DEBUG = False
