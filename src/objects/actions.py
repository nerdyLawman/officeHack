import libtcodpy as libtcod
import gameconfig
from random import randint
from interface.rendering import message, send_to_back, render_all, remote_render

def player_death(player):
    # you ded
    message('You have DIED!', libtcod.white)
    player.char = '%'
    player.color = libtcod.dark_red
    return 'dead' #game_state

def npc_death(npc):
    # npc death
    message(npc.name.upper() + ' is DEAD! You gain ' + str(npc.fighter.xp) + 'XP!', libtcod.cyan)
    npc.char = '%'
    npc.color = libtcod.dark_red
    npc.blocks = False
    npc.fighter = None
    npc.ai = None
    npc.name = 'remains of ' + npc.name.upper()
    send_to_back(npc)
    gameconfig.npc_count -= 1

def drone_death(drone):
    # kill the drone and switch back to the player
    gameconfig.player.player = gameconfig.real_player.player
    gameconfig.player.player.inventory = list(gameconfig.real_inventory)
    gameconfig.real_inventory = None #just so we're not storing a useless list
    gameconfig.player.fighter = gameconfig.real_player.fighter
    gameconfig.player.player.owner = gameconfig.real_player
    gameconfig.player.fighter.owner = gameconfig.real_player
    gameconfig.player = gameconfig.real_player
    npc_death(drone)
    gameconfig.level_drones.remove(drone)
    render_all(True)
    gameconfig.player_at_computer = False

def closest_npc(max_range):
    # find closest enemy to max range and in FOV
    closest_npc = None
    closest_dist = max_range + 1

    for obj in gameconfig.objects:
        if obj.fighter and not obj == gameconfig.player and libtcod.map_is_in_fov(gameconfig.fov_map, obj.x, obj.y):
            dist = gameconfig.player.distance_to(obj)
            if dist < closest_dist:
                closest_npc = obj
                closest_dist = dist
    return closest_npc

def random_object():
    # return a random object
    return gameconfig.objects[libtcod.randint(0,len(gameconfig.objects)-1)]

def random_from(collection):
    return collection[libtcod.randint(0,len(collection)-1)]

def random_from_except(collection, exception):
    _collection = list(collection) # local copy of list
    if exception in _collection: _collection.remove(exception)
    if len(_collection) > 1: return _collection[randint(0,len(_collection)-1)]
    return None

def objects_in_fov():
    # get all that you can see
    fov_objects = []
    for obj in gameconfig.objects:
        if obj is not gameconfig.player and libtcod.map_is_in_fov(gameconfig.fov_map, obj.x, obj.y):
            fov_objects.append(obj)
    return fov_objects

def read_write_file(floppy):
    #if in_computer()
    if gameconfig.player_at_computer: #in computer
        return(floppy.special)
    message("Can't use that here. Try finding a computer.", libtcod.white)
    return 'cancelled'

def remote_view(target):
    # move FOV to another location for a turn
    remote_render(target)
    libtcod.console_wait_for_keypress(True)
    render_all(True)

def remote_control(target):
    # switch player control
    gameconfig.player_at_computer = False
    gameconfig.real_player = gameconfig.player
    gameconfig.real_inventory = list(gameconfig.player.player.inventory)
    target.player = gameconfig.player.player
    target.player.inventory = []
    target.player.owner = target
    target.ai = None
    gameconfig.player = target
    render_all(True)

def throw_coffee(coffee):
    #find closest npc (inside a maximum range) and damage it
    target = closest_npc(gameconfig.COFFEE_RANGE)
    if target is None:  #no enemy found within maximum range
        message('No CO-WORKER is close enough to STRIKE.', libtcod.red)
        return 'cancelled'
    # douce em!
    message('A wave of HOT COFFEE strikes the ' + target.name.upper() + '! ' + target.name.upper() + ' is REPULSED!', libtcod.lime)
    target.change_ai('repulsed')
