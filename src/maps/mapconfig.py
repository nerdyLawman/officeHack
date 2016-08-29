import libtcodpy as libtcod
import gameconfig
from maps.components import Tile, RectRoom
from maps.helpers import random_choice, random_choice_index, random_dict_entry
from objects.classes import Object, Fighter, BaseNPC, Item
from game import color_themes, game_items, game_npcs

def initialize_fov(level_map):
    # set initial FOV condition
    fov_map = libtcod.map_new(gameconfig.MAP_WIDTH, gameconfig.MAP_HEIGHT)
    for y in range(gameconfig.MAP_HEIGHT):
        for x in range(gameconfig.MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not level_map[x][y].block_sight, not level_map[x][y].blocked)
    return fov_map

def is_blocked(level_map, x, y):
    if level_map[x][y].blocked:
        return True
    return False

def create_room(level_map, room):
    # basic room
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            level_map[x][y].blocked = False
            level_map[x][y].block_sight = False

def create_h_tunnel(level_map, x1, x2, y):
    # horizontal tunnel
    for x in range(min(x1, x2), max(x1, x2) + 1):
        level_map[x][y].blocked = False
        level_map[x][y].block_sight = False

def create_v_tunnel(level_map, y1, y2, x):
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        level_map[x][y].blocked = False
        level_map[x][y].block_sight = False

def send_to_back(item, objects):
    objects.remove(item)
    objects.insert(0, item)

def place_objects(level_map, room, objects):
    # random number of NPCS per room
    num_npcs = libtcod.random_get_int(0, 0, gameconfig.MAX_ROOM_NPCS)
    num_items = libtcod.random_get_int(0, 0, gameconfig.MAX_ROOM_ITEMS)

    # add NPCS
    for i in range(num_npcs):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        if not is_blocked(level_map, x, y):
            dice = random_dict_entry(game_npcs.NPCS)
            npc = Object(x, y, dice.get('char'),
                dice.get('name'), dice.get('color'), blocks=True,
                fighter=Fighter(hp=dice.get('hp'), defense=dice.get('defense'), power=dice.get('power'), xp=dice.get('xp')),
                ai=BaseNPC())

            objects.append(npc)
            gameconfig.start_npc_count += 1
            send_to_back(npc, objects)

    gameconfig.npc_count = gameconfig.start_npc_count

    # add Items
    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y1-1)

        if not is_blocked(level_map, x, y):
            # place item
            dice = random_dict_entry(game_items.ITEMS)
            item = Object(x, y, dice.get('char'), dice.get('name'), dice.get('color'), item=Item(use_function=dice.get('use')))

            objects.append(item)
            gameconfig.start_item_count += 1
            send_to_back(item, objects)

    gameconfig.item_count = gameconfig.start_item_count

def make_map(player):
    # generate the level map

    objects = [player]
    rooms = []
    num_rooms = 0
    gameconfig.start_npc_count = 0
    gameconfig.start_item_count = 0

    #pick a random color theme for the level
    color_theme = color_themes.COLOR_THEMES[libtcod.random_get_int(0, 0, len(color_themes.COLOR_THEMES)-1)]

    # fill map with unblocked tiles
    level_map = [[ Tile(True)
        for y in range(gameconfig.MAP_HEIGHT)]
            for x in range(gameconfig.MAP_WIDTH)]

    for r in range(gameconfig.MAX_ROOMS):

        # random width and height
        w = libtcod.random_get_int(0, gameconfig.ROOM_MIN_SIZE, gameconfig.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, gameconfig.ROOM_MIN_SIZE, gameconfig.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, gameconfig.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, gameconfig.MAP_HEIGHT - h - 1)

        # basic room
        new_room = RectRoom(x, y, w, h)
        failed = False

        #run through the other rooms and see if they intersect with this one
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            create_room(level_map, new_room)
            (new_x, new_y) = new_room.center() #center coordinates of new room
            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                #all rooms after the first:
                (prev_x, prev_y) = rooms[num_rooms-1].center() #center coordinates of previous room
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(level_map, prev_x, new_x, prev_y)
                    create_v_tunnel(level_map, prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(level_map, prev_y, new_y, prev_x)
                    create_h_tunnel(level_map, prev_x, new_x, new_y)

                place_objects(level_map, new_room, objects)
            rooms.append(new_room)
            num_rooms += 1

    # create stairs in the last room
    stairs = Object(new_x, new_y, '<', 'stairs', gameconfig.STAIRS_COLOR)
    objects.append(stairs)
    send_to_back(stairs, objects)
    return objects, level_map, stairs, color_theme
