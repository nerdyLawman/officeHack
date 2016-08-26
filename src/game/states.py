import libtcodpy as libtcod
import shelve
import gameconfig
from objects.classes import Object, Fighter
from objects.actions import player_death
from interface.helpers import message, draw_object, clear_object, initialize_interface, render_hud
from maps.helpers import make_map, initialize_fov, get_leveldata
from interface.controls import get_names_under_mouse, initialize_controls, handle_keys

def render_all():
    # main fucntion which draws all objects on the screen every cycle
    global fov_map, fov_recompute

    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, gameconfig.TORCH_RADIUS, gameconfig.FOV_LIGHT_WALLS, gameconfig.FOV_ALGO)
        #go through all tiles, and set their background color
        for y in range(gameconfig.MAP_HEIGHT):
            for x in range(gameconfig.MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
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
            draw_object(obj)
    # draw player last
    draw_object(player)

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.SCREEN_HEIGHT, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # hud info render
    #render_hud()
    
    # mouse look
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, gameconfig.SCREEN_WIDTH/4, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(objects))
    libtcod.console_blit(panel, 0, 0, gameconfig.SCREEN_WIDTH, gameconfig.PANEL_HEIGHT, 0, 0, gameconfig.PANEL_Y)

def new_game(new_cons, new_panel):
    global player, panel, con, objects, inventory, game_state, dungeon_level, player_level, level_map, fov_map, fov_recompute, key, mouse
    # interface
    con = new_cons
    
    #gui
    panel = new_panel
    
    # controls
    key, mouse = initialize_controls()
    
    # player
    fighter_component = Fighter(hp=30, defense=1, power=5, xp=0, death_function=player_death)
    player = Object(0, 0, '@', 'Hero', libtcod.white, blocks=True, fighter=fighter_component)
    player.level = 1
    
    # level
    dungeon_level = 1
    objects, level_map = make_map(player)
    inventory = []
    get_leveldata()

    # game
    game_state = 'playing'
    
    # fov
    fov_map = initialize_fov()
    fov_recompute = False

    #a warm welcoming message!
    message(gameconfig.WELCOME_MESSAGE, libtcod.red)

def save_game():
    # open new empty shelve - overwrites old
    file = shelve.open('savegame', 'n')
    file['map'] = level_map
    file['objects'] = objects
    file['player_index'] = objects.index(player)
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file['stairs_index'] = objects.index(stairs)
    file['dungron_level'] = dungeon_level
    file.close()

def load_game():
    global level_map, objects, player, inventory, game_msgs, game_state, stairs, dungeon_level
    # open previously saved shelve
    file = shelve.open('savegame', 'r')
    level_map = file['map']
    objects = file['objects']
    player = objects[file['player_index']]
    inventory = file['inventory']
    game_msgs = file['game_msgs']
    game_state = file['game_state']
    stairs = objects[file['stairs_index']]
    dungeon_level = file['dungeon_level']
    file.close()
    # render FOV
    initialize_fov()

def play_game():
    global key, mouse, player, objects

    player_action = None
    # control assignment
    #mouse = libtcod.Mouse()
    #key = libtcod.Key()

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
        render_all()
        libtcod.console_flush()
        for obj in objects:
            clear_object(obj)

        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break
        if game_state == 'playing' and player_action != 'no turn':
            for obj in objects:
                if obj.ai:
                    obj.ai.take_turn()

def next_level():
    global dungeon_level

    # go to next level
    message('You take a moment to rest and recover your strength.', libtcod.light_cyan)
    player.fighter.heal(player.fighter.max_hp / 2)
    message('After a moment of peace, you descend deeper into the depths of horror.', libtcod.dark_red)
    dungeon_level += 1

    # create new level
    make_map()
    initialize_leveldata()
    initialize_fov()
