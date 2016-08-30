import libtcodpy as libtcod

# GAME TITLE
CONSOLE_TITLE = 'offICE_HACK//'
GAME_TITLE = 'Office_HACK'
GAME_AUTHOR = 'Nord Mulman & Chairvan Arocstore'

# SCREEN
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

# MAP SIZE
MAP_WIDTH = 80
MAP_HEIGHT = 43

# INTERFACE
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
INVENTORY_WIDTH = 50
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

# public game vars
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
key = libtcod.Key()
mouse = libtcod.Mouse()
objects = []
player = None
level_map = None
fov_map = None
color_theme = None
stairs_up = None
stairs_down = None
game_msgs = []
game_level = 1
game_levels = []
start_npc_count = npc_count = 0
start_item_count = item_count = 0

# libtcod settings
libtcod.console_set_custom_font('data/fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, CONSOLE_TITLE, False)
libtcod.sys_set_fps(LIMIT_FPS) #FPS

# STATUS
CONFUSE_NUM_TURNS = 5
REPULSED_NUM_TURNS = 7
COFFEE_RANGE = 4
TALK_RECHARGE = 3
TALK_RANGE = 2

# FOV
FOV_ALGO = 2
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 8

# ROOMS
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_NPCS = 3
MAX_ROOM_ITEMS = 2

#EXP AND LV
LEVEL_UP_BASE = 100
LEVEL_UP_FACTOR = 50

# COLORS
STAIRS_COLOR = libtcod.black
MENU_BKGND = libtcod.black
MENU_SELECT_BKGND = libtcod.amber
