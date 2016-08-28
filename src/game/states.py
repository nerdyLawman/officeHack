import libtcodpy as libtcod
import shelve
import gameconfig
from interface import interfaceconfig
from interface.helpers import render_all, clear_console, message, message_box
from game.controls import handle_keys
from maps.mapconfig import make_map, initialize_fov
from objects.classes import Fighter, Player, Object

def new_game():

    # player - create player
    player_component = Player(inventory=[])
    fighter_component = Fighter(hp=30, defense=1, power=5, xp=0)
    player = Object(0, 0, '@', 'Hero', libtcod.white, blocks=True, player=player_component, fighter=fighter_component)
    player.level = 1

    # level -- DARIN! don't run off making make_map a cofig just yet, because it needs to be callable to use on different levelzzz.
    objects, level_map, stairs, color_theme = make_map(player)    
    # fov -- COULD THINK ABOUT PUTTING THIS TOGETHER WITH map_map actually
    fov_map = initialize_fov(level_map)
    
    #dungeon_level = 1
    #get_leveldata() #bunch of stuff from here for HUD - currently disabled

    return player, objects, level_map, stairs, color_theme, fov_map

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

"""def load_game():
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
    initialize_fov()"""

def play_game(player, objects, level_map, stairs, color_theme, fov_map):
    game_state = 'playing'
    player_action = None
    fov_recompute = True
    current_level = 0 # make a gameconfig variable
    level1 = [ player, objects, level_map, stairs, color_theme, fov_map ]
    levels = [ level1 ]
    message('Welcome to your DOOM!', libtcod.red) #welcome message

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,interfaceconfig.key,interfaceconfig.mouse)

        render_all(player, objects, level_map, fov_map, fov_recompute, color_theme)
        player_action = handle_keys(player, objects, level_map, stairs)

        if player_action == 'exit':
            save_game()
            break
        if player_action == 'stairs down':
            objects, level_map, stairs, color_theme, fov_map = next_level(player)
            
            new_level = [ objects, level_map, stairs, color_theme, fov_map ]
            levels.append(new_level) # this needs to get fleshed out a lot more
            # then we could have something like levels[current_level].objects, levels[current_level].level_map, etc...
        if game_state == 'playing' and player_action != 'no turn':
            fov_recompute = True

            for obj in objects:
                if obj.ai:
                    obj.ai.take_turn(fov_map, player)

def next_level(player):
    # go to next level
    
    # we should also consider storing the previous levels so you can return to previously explored ones
    
    #message('You take a moment to rest and recover your strength.', libtcod.light_cyan)
    #player.fighter.heal(player.fighter.max_hp / 2)
    #message('After a moment of peace, you descend deeper into the depths of horror.', libtcod.dark_red)
    #dungeon_level += 1

    # create new level
    clear_console(interfaceconfig.con) #consider moving out of here - are there situations where you would want to create the level and not display it? Probably not, actually.
    objects, level_map, stairs, color_theme = make_map(player)  
    #initialize_leveldata()
    fov_map = initialize_fov(level_map)
    return objects, level_map, stairs, color_theme, fov_map
