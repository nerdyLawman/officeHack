from libtcod import libtcodpy as libtcod
import gameconfig
from random import randint
from interface.rendering import message, send_to_back, render_all, remote_render

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

def read_document(document):
    message('The document reads: ' + document.special)
    
def floppy_overwrite(floppy):
    if not gameconfig.player_at_computer: #in computer
        message("Can't use that here. Try finding a computer.", libtcod.white)
        return 'cancelled'
    message('floppy disc renamed.')

def throw_coffee(coffee):
    #find closest npc (inside a maximum range) and damage it
    target = closest_npc(gameconfig.COFFEE_RANGE)
    if target is None:  #no enemy found within maximum range
        message('No CO-WORKER is close enough to STRIKE.', libtcod.red)
        return 'cancelled'
    # douce em!
    message('A wave of HOT COFFEE strikes the ' + target.name.upper() + '! ' + target.name.upper() + ' is REPULSED!', libtcod.lime)
    target.change_ai('repulsed')
