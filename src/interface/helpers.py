import libtcodpy as libtcod
import gameconfig
import textwrap
from interface import interfaceconfig
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

def render_all(player, objects, level_map, fov_map, fov_recompute, theme):
    # main fucntion which draws all objects on the screen every cycle

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
                            libtcod.console_set_char_background(interfaceconfig.con, x, y, theme['color_dark_wall'], libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(interfaceconfig.con, x, y, theme['color_dark_ground'], libtcod.BKGND_SET)
                else:
                    if wall:
                        libtcod.console_set_char_background(interfaceconfig.con, x, y, theme['color_light_wall'], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(interfaceconfig.con, x, y, theme['color_light_ground'], libtcod.BKGND_SET)
                    level_map[x][y].explored = True

    # draw all objects in the list
    for obj in objects:
        if obj != player:
            if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
                draw_object(obj, interfaceconfig.con)
    # draw player last
    draw_object(player, interfaceconfig.con)

    #blit the contents of "con" to the root console
    libtcod.console_blit(interfaceconfig.con, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0)

    #panel
    libtcod.console_set_default_background(interfaceconfig.panel, libtcod.black)
    libtcod.console_clear(interfaceconfig.panel)
    
    render_hud(player)
    render_messages()
    
    libtcod.console_blit(interfaceconfig.panel, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT, 0, 0, gameconfig.PANEL_Y)

    libtcod.console_flush()
    for obj in objects:
        clear_object(obj, interfaceconfig.con)

def render_hud(player):
    # dungeon level
    libtcod.console_set_default_foreground(interfaceconfig.panel, libtcod.white)
    libtcod.console_print_ex(interfaceconfig.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level: ' + str(1))
    # health bar
    render_bar(1, 1, gameconfig.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
    # NPCs bar
    #render_bar(1, 3, gameconfig.BAR_WIDTH, 'NPCS', npc_count, start_npc_count, libtcod.light_blue, libtcod.darker_blue)
    # items bar
    #render_bar(1, 5, gameconfig.BAR_WIDTH, 'ITEMS', item_count, start_item_count, libtcod.light_violet, libtcod.darker_violet)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a status bar
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(interfaceconfig.panel, back_color)
    libtcod.console_rect(interfaceconfig.panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(interfaceconfig.panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(interfaceconfig.panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(interfaceconfig.panel, libtcod.white)
    libtcod.console_print_ex(interfaceconfig.panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))

def render_messages():
    #game_msgs = [['test1',libtcod.red], ['hello world',libtcod.white], ['I\'d like to go now',libtcod.blue]]
    y = 1
    for (line, color) in interfaceconfig.game_msgs:
        libtcod.console_set_default_foreground(interfaceconfig.panel, color)
        libtcod.console_print_ex(interfaceconfig.panel, gameconfig.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1


def menu(header, options, width):
    # general selection menu
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options!')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(interfaceconfig.con, 0, 0, width, gameconfig.SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, gameconfig.MENU_BKGND)
    libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SCREEN)

    #print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
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
            if key.vk == libtcod.KEY_ENTER:
                return(selected-1)
            
            # hightlight selected option
            libtcod.console_set_default_background(window, gameconfig.MENU_BKGND)
            libtcod.console_rect(window, 0, 0, width, height, False, libtcod.BKGND_SET)
            libtcod.console_set_default_background(window, gameconfig.MENU_SELECT_BKGND)
            libtcod.console_rect(window, 0, selected-1+header_height, width, 1, False, libtcod.BKGND_SCREEN)
            libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
            libtcod.console_flush()
            
            # convert ascii to index
            index = key.c - ord('a')
            if index >= 0 and index < len(options): return index
        
        if key.vk == libtcod.KEY_ESCAPE:
            return None

def message(new_msg, color=libtcod.white):
    # play by play message display
    # NEEDS game_msgs
    new_msg_lines = textwrap.wrap(new_msg, gameconfig.MSG_WIDTH)

    for line in new_msg_lines:
        if len(interfaceconfig.game_msgs) == gameconfig.MSG_HEIGHT:
            del interfaceconfig.game_msgs[0]
        interfaceconfig.game_msgs.append((line, color))

def message_box(text, width=50):
    # popup message box
    menu(text, [], width)
