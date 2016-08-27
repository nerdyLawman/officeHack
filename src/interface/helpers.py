import libtcodpy as libtcod
import gameconfig
import textwrap
from maps.helpers import in_fov

# ADDRESS:
# render_all()
# menu()
# inventory_menu()

def clear_console(console):
    libtcod.console_clear(console)

def clear_all(objects, con):
    for obj in objects:
        clear_object(obj, con)

def render_all(player, objects, level_map, fov_map, con, panel):
    # main fucntion which draws all objects on the screen every cycle
    
    fov_recompute = True
    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, gameconfig.TORCH_RADIUS, gameconfig.FOV_LIGHT_WALLS, gameconfig.FOV_ALGO)
        
        # go through all tiles, and set their background color
        for y in range(gameconfig.MAP_HEIGHT):
            for x in range(gameconfig.MAP_WIDTH):
                #visible = libtcod.map_is_in_fov(fov_map, x, y)
                visible = True
                wall = level_map[x][y].block_sight
                if not visible:
                    if level_map[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(con, x, y, gameconfig.color_dark_wall, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(con, x, y, gameconfig.color_dark_ground, libtcod.BKGND_SET)
                else:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, gameconfig.color_light_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, gameconfig.color_light_ground, libtcod.BKGND_SET)
                    level_map[x][y].explored = True

    # draw all objects in the list
    for obj in objects:
        if obj != player:
            if libtcod.map_is_in_fov(fov_map, x, y):
                draw_object(obj, con)
    # draw player last
    draw_object(player, con)

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0)
    
    #panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    # hud info render
    #render_hud()

    # mouse look
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    #libtcod.console_print_ex(panel, gameconfig.SCREEN_WIDTH/4, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(objects))

    libtcod.console_blit(panel, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT, 0, 0, gameconfig.PANEL_Y)
    
    libtcod.console_flush()
    for obj in objects:
        clear_object(obj, con)

def render_hud():
    # dungeon level
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level: ' + str(dungeon_level))
    # health bar
    render_bar(1, 1, gameconfig.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
        libtcod.light_red, libtcod.darker_red)
    # NPCs bar
    render_bar(1, 3, gameconfig.BAR_WIDTH, 'NPCS', npc_count, start_npc_count, libtcod.light_blue, libtcod.darker_blue)
    # items bar
    render_bar(1, 5, gameconfig.BAR_WIDTH, 'ITEMS', item_count, start_item_count, libtcod.light_violet, libtcod.darker_violet)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a status bar
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))

    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, gameconfig.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

def menu(header, options, width):
    # general selection menu
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options!')

    # calculate total height for the header (after auto-wrap) and one line per option
    #header_height = libtcod.console_get_height_rect(con, 0, 0, width, gameconfig.SCREEN_HEIGHT, header)
    header_height = 1
    if header == '':
        header_height = 0
    height = len(options) + header_height

    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

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
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    selected = 0
    while True:
        key = libtcod.console_wait_for_keypress(True)
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
        if key.vk == libtcod.KEY_ESCAPE:
            return None
        
        libtcod.console_clear(window)
        libtcod.console_set_default_background(window, libtcod.light_yellow)
        libtcod.console_rect(window, 0, selected-1+header_height, 100, 1, False, libtcod.BKGND_SCREEN)
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    
        # convert ascii to index
        index = key.c - ord('a')
        if index >= 0 and index < len(options): return index
    return 'no selection'

def message(new_msg, color=libtcod.white):
    # play by play message display
    # NEEDS game_msgs
    new_msg_lines = textwrap.wrap(new_msg, gameconfig.MSG_WIDTH)

    #for line in new_msg_lines:
    #    if len(game_msgs) == gameconfig.MSG_HEIGHT:
    #        del game_msgs[0]
        #game_msgs.append((line, color))

def message_box(text, width=50):
    # popup message box
    menu(text, [], width)

def draw_object(obj, con):
    libtcod.console_set_default_foreground(con, obj.color)
    libtcod.console_set_char_background(con, obj.x, obj.y, obj.color, libtcod.BKGND_SET)
    libtcod.console_put_char(con, obj.x, obj.y, obj.char,libtcod.BKGND_NONE)

def clear_object(obj, con):
    libtcod.console_put_char(con, obj.x, obj.y, ' ', libtcod.BKGND_NONE)

def inventory_menu(header, inventory):
    # inventory
    # NEEDS: inventory
    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.name for item in inventory]
    index = 'no selection'
    #return selected item
    while index == 'no selection':
        index = menu(header, options, INVENTORY_WIDTH)
    if index is None or len(inventory) == 0: return None
    return inventory[index].item
