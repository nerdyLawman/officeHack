import gameconfig
import libtcodpy as libtcod

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

def get_leveldata(objects):
    # returns counts of NPCs and Items --todo return instead of assignment
    start_npc_count = 0
    start_item_count = 0
    for obj in objects:
        if obj.ai:
            start_npc_count += 1
        if obj.item:
            start_item_count += 1
    npc_count = start_npc_count
    item_count = start_item_count
    return start_npc_count, npc_count, start_item_count, item_count

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
    if level_map[x][y].blocked:
        return True
    return False
