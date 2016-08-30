import libtcodpy as libtcod
import gameconfig
import textwrap
from maps.helpers import in_fov

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
    libtcod.console_rect(console, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, True, libtcod.BKGND_SET)

def clear_all(objects, con):
    # clears them all
    for obj in objects:
        clear_object(obj, con)

def render_all(fov_recompute):
    # main fucntion which draws all objects on the screen every cycle

    #local renders
    player = gameconfig.player
    objects = gameconfig.objects
    level_map = gameconfig.level_map
    fov_map = gameconfig.fov_map
    theme = gameconfig.color_theme

    if fov_recompute:
        libtcod.map_compute_fov(fov_map, player.x, player.y, gameconfig.TORCH_RADIUS, gameconfig.FOV_LIGHT_WALLS, gameconfig.FOV_ALGO)
        # go through all tiles, and set their background color
        for y in range(gameconfig.MAP_HEIGHT):
            for x in range(gameconfig.MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = level_map[x][y].block_sight
                if not visible:
                    if level_map[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(gameconfig.con, x, y, theme['color_dark_wall'], libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(gameconfig.con, x, y, theme['color_dark_ground'], libtcod.BKGND_SET)
                else:
                    if wall:
                        libtcod.console_set_char_background(gameconfig.con, x, y, theme['color_light_wall'], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(gameconfig.con, x, y, theme['color_light_ground'], libtcod.BKGND_SET)
                    level_map[x][y].explored = True

    # draw all objects in the list
    for obj in objects:
        if obj != player:
            if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
                draw_object(obj, gameconfig.con)
    draw_object(player, gameconfig.con) # draw player last

    #blit the contents of "con" to the root console
    libtcod.console_blit(gameconfig.con, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0)

    # panel
    libtcod.console_set_default_background(gameconfig.panel, libtcod.black)
    libtcod.console_clear(gameconfig.panel)

    # HUD
    render_hud()
    render_messages()

    libtcod.console_blit(gameconfig.panel, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT, 0, 0, gameconfig.PANEL_Y)

    # clean up
    libtcod.console_flush()
    for obj in objects:
        clear_object(obj, gameconfig.con)

def render_hud():
    player = gameconfig.player
    # dungeon level
    libtcod.console_set_default_foreground(gameconfig.panel, libtcod.white)
    libtcod.console_print_ex(gameconfig.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, 'OFFICE LEVEL: ' + str(gameconfig.game_level))
    # health bar
    render_bar(1, 1, gameconfig.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.red, libtcod.darker_flame)
    # NPCs bar
    render_bar(1, 3, gameconfig.BAR_WIDTH, 'COWORKERS', gameconfig.npc_count, gameconfig.start_npc_count, libtcod.azure, libtcod.darker_blue)
    # items bar
    render_bar(1, 5, gameconfig.BAR_WIDTH, 'ITEMS', gameconfig.item_count, gameconfig.start_item_count, libtcod.light_violet, libtcod.darker_violet)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a status bar
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(gameconfig.panel, back_color)
    libtcod.console_rect(gameconfig.panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(gameconfig.panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(gameconfig.panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(gameconfig.panel, libtcod.white)
    libtcod.console_print_ex(gameconfig.panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))

def render_messages():
    # display a message
    y = 0
    for (line, color) in gameconfig.game_msgs:
        libtcod.console_set_default_foreground(gameconfig.panel, color)
        libtcod.console_print_ex(gameconfig.panel, gameconfig.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

def menu(header, options, width):
    # general selection menu
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options!')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(gameconfig.con, 0, 0, width, gameconfig.SCREEN_HEIGHT, header+'\n')
    if header == '':
        header_height = 1
    height = len(options) + header_height + 1

    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, gameconfig.MENU_BKGND)
    libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SCREEN)

    #print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 1, 1, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

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
    libtcod.console_set_default_background(window, libtcod.red)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)

    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    selected = 0
    while True:
        key = libtcod.console_wait_for_keypress(True)

        if options: # selection loop
            if key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_UP:
                if key.vk == libtcod.KEY_DOWN:
                    if selected < len(options):
                        selected += 1
                    else:
                        selected = 1
                if key.vk == libtcod.KEY_UP:
                    if selected > 1:
                        selected -= 1
                    else:
                        selected = len(options)
                # hightlight selected option
                libtcod.console_set_default_background(window, gameconfig.MENU_BKGND)
                libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SET)
                libtcod.console_set_default_background(window, gameconfig.MENU_SELECT_BKGND)
                libtcod.console_rect(window, 0, selected-1+header_height, width, 1, False, libtcod.BKGND_SCREEN)
                libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
                libtcod.console_flush()
            if key.vk == libtcod.KEY_ENTER:
                return(selected-1)

            # convert ascii to index
            index = key.c - ord('a')
            if index >= 0 and index < len(options): return index

        if key.vk == libtcod.KEY_ESCAPE:
            return None

def message(new_msg, color=libtcod.white):
    # play by play message display
    new_msg_lines = textwrap.wrap(new_msg, gameconfig.MSG_WIDTH)

    for line in new_msg_lines:
        if len(gameconfig.game_msgs) == gameconfig.MSG_HEIGHT:
            del gameconfig.game_msgs[0]
        gameconfig.game_msgs.append((line, color))

def message_box(text, width=50):
    # popup message box
    menu(text, [], width)
