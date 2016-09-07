from libtcod import libtcodpy as libtcod
import gameconfig
import math
from random import randint

def random_choice_index(chances):
    # returns a random index
    dice = libtcod.random_get_int(0, 1, sum(chances))
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w
        if dice <= running_sum:
            return choice
        choice += 1


def random_choice(chances_dict):
    # returns a string of a random selection
    chances = chances_dict.values()
    strings = chances_dict.keys()
    return strings[random_choice_index(chances)]


def random_dict_entry(dict_list):
    # returns a random dictionary entry from a list of dictionaries based on 'chance'
    dice = libtcod.random_get_int(0, 1, 100)
    running_sum = 0
    for d in dict_list:
        running_sum += d.get('chance')
        if dice <= running_sum:
            return d


def make_person():
    if randint(0, 1) < 1:
        gender = 'F'
        portrait = 'data/img/fportrait.png'
        namestxt = 'data/banks/femaleNames.txt'
    else:
        gender = 'M'
        portrait = 'data/img/mportrait.png'
        namestxt = 'data/banks/maleNames.txt'
    with open (namestxt, 'r') as namefile:
        names=namefile.readlines()
        return names[randint(1,len(names)-1)][:-1], gender, portrait


def true_or_false(chance):
    if randint(0,100) <= chance: return True
    return False


def in_fov(fov_map, x, y):
    return libtcod.map_is_in_fov(fov_map, x, y)


def is_blocked(x, y):
    # test if tile is blocked
    if gameconfig.level_map[x][y].blocked:
        return True
    # now check for any blocking objects
    for obj in gameconfig.objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
    return False


def check_map_blocked(x, y):
    if gameconfig.level_map[x][y].blocked: return True
    return False


def get_map_bounds():
    # THIS FUNCTION IS UGLY - UPDATE
    bounds = []
    bounded = False #top bounds
    y = 0
    while bounded is False:
        for x in range(gameconfig.MAP_WIDTH):
            if check_map_blocked(x, y) is False:
                bounded = True
                bounds.append([x,y-1])
        if y < gameconfig.MAP_HEIGHT: y += 1
        else: bounded = True

    bounded = False #bottom bounds
    y = gameconfig.MAP_HEIGHT-1
    while bounded is False:
        for x in range(gameconfig.MAP_WIDTH):
            if check_map_blocked(x, y) is False:
                bounded = True
                bounds.append([x,y+1])
        if y > 0: y -= 1
        else: bounded = True

    bounded = False #left bounds
    x = 0
    while bounded is False:
        for y in range(gameconfig.MAP_HEIGHT):
            if check_map_blocked(x, y) is False:
                bounded = True
                bounds.append([x-1,y])
        if x < gameconfig.MAP_WIDTH: x += 1
        else: bounded = True

    bounded = False #right bounds
    x = gameconfig.MAP_WIDTH-1
    while bounded is False:
        for y in range(gameconfig.MAP_HEIGHT):
            if check_map_blocked(x, y) is False:
                bounded = True
                bounds.append([x+1,y])
        if x > 0: x -= 1
        else: bounded = True
    return bounds

def get_room_walls(room):
    roomx = [room.x1, room.x2]
    roomy = [room.y1, room.y2]
    wall_tiles = []
    for x in range(room.x1+1, room.x2-1):
        if gameconfig.level_map[x][room.y1].blocked: wall_tiles.append([x,room.y1])
    for x in range(room.x1+1, room.x2-1):
        if gameconfig.level_map[x][room.y2].blocked: wall_tiles.append([x,room.y2])
    for y in range(room.y1+1, room.y2-1):
        if gameconfig.level_map[room.x1][y].blocked: wall_tiles.append([room.x1,y])
    for y in range(room.y1+1, room.y2-1):
        if gameconfig.level_map[room.x2][y].blocked: wall_tiles.append([room.x2,y])
    return wall_tiles
