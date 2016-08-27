import libtcodpy as libtcod
import gameconfig

def initialize_interface():
    # here we go!
    libtcod.console_set_custom_font('data/fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 'Office_Hack', False)
    con = libtcod.console_new(gameconfig.MAP_WIDTH, gameconfig.MAP_HEIGHT) # creates con
    panel = libtcod.console_new(gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT) #creates panel
    game_msgs = []

    libtcod.sys_set_fps(gameconfig.LIMIT_FPS) #FPS

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
        gameconfig.GAME_TITLE)
    libtcod.console_print_ex(0, gameconfig.SCREEN_WIDTH/2, gameconfig.SCREEN_HEIGHT/2-3, libtcod.BKGND_NONE, libtcod.CENTER,
        gameconfig.GAME_AUTHOR)
    return con, panel, game_msgs

def initialize_controls():
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    return key, mouse
