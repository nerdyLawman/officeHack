import libtcodpy as libtcod
import gameconfig

# public vars
con = libtcod.console_new(gameconfig.MAP_WIDTH, gameconfig.MAP_HEIGHT)
panel = libtcod.console_new(gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT)
game_msgs = []
key = libtcod.Key()
mouse = libtcod.Mouse()

# set features
libtcod.console_set_custom_font('data/fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, gameconfig.CONSOLE_TITLE, False)
libtcod.sys_set_fps(gameconfig.LIMIT_FPS) #FPS
