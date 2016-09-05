from libtcod import libtcodpy as libtcod
import gameconfig
import textwrap
from maps.helpers import in_fov

# ---------------------------------------------------------------------
# [ RENDERING UTILITIES ] ---------------------------------------------
# ---------------------------------------------------------------------
def draw_object(obj, con):
    # draws a object (char) to specified screenspace
    libtcod.console_set_default_foreground(con, obj.color)
    libtcod.console_set_char_background(con, obj.x, obj.y, obj.color, libtcod.BKGND_SET)
    libtcod.console_put_char(con, obj.x, obj.y, obj.char, libtcod.BKGND_NONE)


def clear_object(obj, con):
    # sets objt char to blank
    libtcod.console_put_char(con, obj.x, obj.y, ' ', libtcod.BKGND_NONE)


def clear_console(console):
    # blacks out the specified screenspace
    libtcod.console_clear(console)
    libtcod.console_set_default_background(console, libtcod.black)
    libtcod.console_rect(console, 0, 0, gameconfig.SCREEN_WIDTH,
        gameconfig.SCREEN_HEIGHT, True, libtcod.BKGND_SET)


def clear_all(objects, con):
    for obj in objects: clear_object(obj, con)


def send_to_back(item):
    gameconfig.objects.remove(item)
    gameconfig.objects.insert(0, item)


# ---------------------------------------------------------------------
# [ RENDERING ] -------------------------------------------------------
# ---------------------------------------------------------------------
def render_all(fov_recompute):
    # main fucntion which draws all objects on the screen every cycle
    
    player = gameconfig.player #local renders for convenience
    objects = gameconfig.objects
    level_map = gameconfig.level_map
    fov_map = gameconfig.fov_map

    if fov_recompute: render_map(level_map, fov_map, player)
    # draw all objects in the list
    render_objects(objects, player, fov_map)
    libtcod.console_blit(gameconfig.con, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0)

    # panel - HUD + messages
    libtcod.console_set_default_background(gameconfig.panel, gameconfig.LEVEL_BKGND)
    libtcod.console_clear(gameconfig.panel)
    if gameconfig.REMOTE_FLAG: single_message('REMOTE VIEWING: ' + gameconfig.remote_target + '.\nPRESS ANY KEY TO EXIT')
    else:
        render_hud()
        render_messages()
    libtcod.console_blit(gameconfig.panel, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT, 0, 0, gameconfig.PANEL_Y)

    # filters
    if gameconfig.DRONE_FLAG:
        render_drone_filter()
        libtcod.console_blit(gameconfig.filter, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0, 0.2, 0.2)
        libtcod.console_clear(gameconfig.filter)
    
    if gameconfig.REMOTE_FLAG:
        render_station_filter()
        libtcod.console_blit(gameconfig.filter, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0, 0.2, 0.2)
        libtcod.console_clear(gameconfig.filter)

    # clean up
    libtcod.console_flush()
    clear_all(objects, gameconfig.con)


def render_map(level_map, fov_map, position):
    theme = gameconfig.color_theme
    
    libtcod.map_compute_fov(fov_map, position.x, position.y,
        gameconfig.TORCH_RADIUS, gameconfig.FOV_LIGHT_WALLS, gameconfig.FOV_ALGO)
    # go through all tiles, and set their background color
    for y in range(gameconfig.MAP_HEIGHT):
        for x in range(gameconfig.MAP_WIDTH):
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            wall = level_map[x][y].block_sight
            if not visible:
                if level_map[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(gameconfig.con, x, y,
                            theme['color_dark_wall'], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(gameconfig.con, x, y,
                            theme['color_dark_ground'], libtcod.BKGND_SET)
            else:
                if wall:
                    libtcod.console_set_char_background(gameconfig.con, x, y,
                        theme['color_light_wall'], libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(gameconfig.con, x, y,
                        theme['color_light_ground'], libtcod.BKGND_SET)
                level_map[x][y].explored = True


def render_objects(objects, player, fov_map):
    for obj in objects:
        if obj != player:
            if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
                draw_object(obj, gameconfig.con)
    draw_object(player, gameconfig.con) # draw player last


def render_hud():
    player = gameconfig.player # easy-access
    # dungeon level ---------------------
    libtcod.console_set_default_foreground(gameconfig.panel, libtcod.white)
    libtcod.console_print_ex(gameconfig.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, 'OFFICE LEVEL: ' + str(gameconfig.game_level))
    # health bar -----------------------
    render_bar(1, 1, gameconfig.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.red, libtcod.darker_flame)
    # NPCs bar ------------------------
    render_bar(1, 3, gameconfig.BAR_WIDTH, 'CO-WORKERS', gameconfig.npc_count, gameconfig.level_npc_count, libtcod.azure, libtcod.darker_blue)
    # items bar -------------------------
    render_bar(1, 5, gameconfig.BAR_WIDTH, 'ITEMS', gameconfig.item_count, gameconfig.level_item_count, libtcod.light_violet, libtcod.darker_violet)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a status bar
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(gameconfig.panel, back_color)
    libtcod.console_rect(gameconfig.panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(gameconfig.panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(gameconfig.panel, x, y, bar_width, 1, False, libtcod.BKGND_SET)
    libtcod.console_set_default_foreground(gameconfig.panel, libtcod.white)
    libtcod.console_print_ex(gameconfig.panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))


# ---------------------------------------------------------------------
# [ FILTERS ] ---------------------------------------------------------
# ---------------------------------------------------------------------
def render_drone_filter():
    libtcod.console_set_default_background(gameconfig.filter, gameconfig.DRONE_FILTER_COLOR)
    libtcod.console_rect(gameconfig.filter, 0, 0, gameconfig.SCREEN_WIDTH,
        gameconfig.SCREEN_HEIGHT, False, libtcod.BKGND_SCREEN)


def render_station_filter():
    libtcod.console_set_default_background(gameconfig.filter, gameconfig.REMOTE_FILTER_COLOR)
    libtcod.console_rect(gameconfig.filter, 0, 0, gameconfig.SCREEN_WIDTH,
        gameconfig.SCREEN_HEIGHT, False, libtcod.BKGND_SCREEN)


# ---------------------------------------------------------------------
# [ MESSAGES ] --------------------------------------------------------
# ---------------------------------------------------------------------
def message(new_msg, color=libtcod.white):
    # play by play message display
    new_msg_lines = textwrap.wrap(new_msg, gameconfig.MSG_WIDTH)
    for line in new_msg_lines:
        if len(gameconfig.game_msgs) == gameconfig.MSG_HEIGHT:
            del gameconfig.game_msgs[0]
        gameconfig.game_msgs.append((line, color))


def fetch_message(msg):
    #coming soon
    return gamemessages.SET_MESSAGES.get(msg)[0], 


def render_messages():
    # display a message
    y = 1 # give it a line break at the top
    for (line, color) in gameconfig.game_msgs:
        libtcod.console_set_default_foreground(gameconfig.panel, color)
        libtcod.console_print_ex(gameconfig.panel, gameconfig.MSG_X, y,
            libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1


def single_message(text, color=libtcod.white):
    # just the one
    libtcod.console_set_default_foreground(gameconfig.panel, color)
    libtcod.console_print_ex(gameconfig.panel, gameconfig.MSG_X, 1,
        libtcod.BKGND_NONE, libtcod.LEFT, text)