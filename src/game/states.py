import libtcodpy as libtcod
import shelve
import gameconfig
from objects.classes import Object, Fighter, Player
from objects.actions import player_death
from interface.helpers import message, initialize_interface, render_all, clear_object
from maps.helpers import make_map, initialize_fov, get_leveldata
from interface.controls import get_names_under_mouse, initialize_controls, handle_keys
from interface.menus import menu

def main_menu():
    global con, panel, game_msgs
    #img = libtcod.image_load('bgk.png')
    con, panel, game_msgs = initialize_interface() #setup screen here
    while not libtcod.console_is_window_closed():
        choice = menu('', ['New Game', 'Continue', 'Quit'], 24)
        if choice == 0:
            new_game()
            play_game()
        if choice == 1:
            try:
                load_game()
            except:
                message_box('\n No saved gamedata to load.\n', 24)
                continue
            play_game()
        elif choice == 2:
            break

def new_game():
    global key, mouse, player, objects, level_map, stairs, inventory, dungeon_level, game_state, fov_map, fov_recompute
    # interface
    #con = new_cons
    #gui
    #panel = new_panel

    # controls - setup key and mouse
    key, mouse = initialize_controls()

    # player - create player
    inventory = []
    #player_component = Player(inventory=inventory)
    fighter_component = Fighter(hp=30, defense=1, power=5, xp=0, death_function=player_death)
    player = Object(0, 0, '@', 'Hero', libtcod.white, blocks=True, fighter=fighter_component)
    player.level = 1

    # level
    objects, level_map, stairs = make_map(player)
    dungeon_level = 1
    get_leveldata() #bunch of stuff from here for HUD - currently disabled

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
    #global key, mouse, player, objects
    player_action = None

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
        render_all(fov_map, fov_recompute, level_map, objects, player)
        libtcod.console_flush()
        for obj in objects:
            clear_object(obj)

        player_action = handle_keys(player, objects)
        if player_action == 'exit':
            save_game()
            break
        if game_state == 'playing' and player_action != 'no turn':
            for obj in objects:
                if obj.ai:
                    obj.ai.take_turn(fov_map, player)

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
