from libtcod import libtcodpy as libtcod
import gameconfig
from random import randint
from maps.components import Tile, RectRoom
from maps.helpers import random_choice, random_choice_index, random_dict_entry, make_person, true_or_false, get_room_walls, get_map_bounds
from interface.rendering import send_to_back
from game import color_themes, game_items, game_npcs
from objects.Player import Player
from objects.Fighter import Fighter
from objects.Object import Object
from objects.Ai import BaseNPC, TalkerNPC, StationaryNPC
from objects.Item import Item

# ---------------------------------------------------------------------
# [ MAPPING UTILITIES ] -----------------------------------------------
# ---------------------------------------------------------------------
def is_blocked(x, y):
    if gameconfig.level_map[x][y].blocked:
        return True
    return False


def create_room(room):
    # basic room
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            gameconfig.level_map[x][y].blocked = False
            gameconfig.level_map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    # horizontal tunnel
    for x in range(min(x1, x2), max(x1, x2) + 1):
        gameconfig.level_map[x][y].blocked = False
        gameconfig.level_map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        gameconfig.level_map[x][y].blocked = False
        gameconfig.level_map[x][y].block_sight = False


def initialize_fov():
    # set initial FOV condition
    gameconfig.fov_map = libtcod.map_new(gameconfig.MAP_WIDTH, gameconfig.MAP_HEIGHT)
    for y in range(gameconfig.MAP_HEIGHT):
        for x in range(gameconfig.MAP_WIDTH):
            libtcod.map_set_properties(gameconfig.fov_map, x, y,
                not gameconfig.level_map[x][y].block_sight,
                not gameconfig.level_map[x][y].blocked)


# ---------------------------------------------------------------------
# [ OBJECT PLACEMENT ] ------------------------------------------------
# ---------------------------------------------------------------------
def place_objects(room):
    # random number of NPCS per room
    num_npcs = libtcod.random_get_int(0, 0, gameconfig.MAX_ROOM_NPCS)
    num_items = libtcod.random_get_int(0, 0, gameconfig.MAX_ROOM_ITEMS)

    # add NPCS -----------------------------
    for i in range(num_npcs):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        if not is_blocked(x, y):
            dice = random_dict_entry(game_npcs.NPC_classes)
            if dice.get('ai') == 'talk':
                npc_ai = TalkerNPC()
            else:
                npc_ai = BaseNPC()
            npc_name, npc_gender, npc_portrait = make_person()
            npc = Object(x, y, dice.get('char'), npc_name, dice.get('color'), dice.get('info'), blocks=True,
                fighter=Fighter(hp=dice.get('hp'), defense=dice.get('defense'),
                power=dice.get('power'), xp=dice.get('xp'), drone=true_or_false(30),
                gender=npc_gender, portrait=npc_portrait), ai=npc_ai)
            gameconfig.objects.append(npc)
            gameconfig.level_npc_count += 1
            send_to_back(npc)
            if npc.fighter.drone is True:
                gameconfig.level_drones.append(npc)
                npc.fighter.codeword = 'oswald'

    gameconfig.npc_count = gameconfig.level_npc_count

    # add stationary objects -------------------------
    for i in range(1):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y1-1)

        if not is_blocked(x, y):
            # place stationary object
            dice = random_dict_entry(game_npcs.stationary_objects)
            if dice:
                stationary = Object(x, y, dice.get('char'), dice.get('name'),
                    dice.get('color'), dice.get('info'), blocks=True,
                    ai=StationaryNPC(base_color=dice.get('color'),
                    interact=dice.get('interact'),special=dice.get('special')))
                if dice.get('interact') == 'terminal':
                    gameconfig.level_terminals.append(stationary)
                    stationary.name = 'TERMINAL STATION 1X00G5-00' + str(len(gameconfig.level_terminals))
                elif dice.get('interact') == 'gaze':
                    stationary.ai.special = game_npcs.views[randint(0, len(game_npcs.views)-1)]
                if dice.get('wall'):
                    bounds = get_room_walls(room)
                    xy = bounds[randint(0, len(bounds)-1)]
                    stationary.x = xy[0]
                    stationary.y = xy[1]
                gameconfig.objects.append(stationary)
                send_to_back(stationary)

    # add Items ---------------------------
    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y1-1)

        if not is_blocked(x, y):
            # place item
            dice = random_dict_entry(game_items.ITEMS)
            item = Object(x, y, dice.get('char'), dice.get('name'), dice.get('color'), dice.get('info'),
                item=Item(special=dice.get('special'), use_function=dice.get('use'), is_instant=dice.get('instant')))

            gameconfig.objects.append(item)
            gameconfig.level_item_count += 1
            send_to_back(item)

    gameconfig.item_count = gameconfig.level_item_count


# ---------------------------------------------------------------------
# [ MAKE MAP ] --------------------------------------------------------
# ---------------------------------------------------------------------
def make_map():
    # generate the level map
    gameconfig.objects[:] = [gameconfig.player]
    gameconfig.level_drones[:] = []
    gameconfig.level_terminals[:] = []
    rooms = []
    num_rooms = 0
    gameconfig.level_npc_count = 0
    gameconfig.level_item_count = 0

    #pick a random color theme for the level
    gameconfig.color_theme = color_themes.COLOR_THEMES[libtcod.random_get_int(0, 0, len(color_themes.COLOR_THEMES)-1)]

    # fill map with unblocked tiles
    gameconfig.level_map = [[ Tile(True)
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
            create_room(new_room)
            (new_x, new_y) = new_room.center() #center coordinates of new room
            if num_rooms == 0:
                #this is the first room, where the player starts at
                gameconfig.player.x = new_x
                gameconfig.player.y = new_y

                # create stairs in the first room
                gameconfig.stairs_down = Object(new_x, new_y, '<', 'stairs down', gameconfig.STAIRS_COLOR)
                gameconfig.objects.append(gameconfig.stairs_down)
                send_to_back(gameconfig.stairs_down)

            else:
                #all rooms after the first:
                (prev_x, prev_y) = rooms[num_rooms-1].center() #center coordinates of previous room
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

                place_objects(new_room)
            rooms.append(new_room)
            num_rooms += 1

    # place a single window to the outside -------------------
    bounds = get_map_bounds()
    xy = bounds[randint(0, len(bounds)-1)]
    #if object in this position
    for obj in gameconfig.objects:
        if obj.x == xy[0] and obj.y == xy[1]:
            gameconfig.objects.remove(obj)
    win = game_npcs.window
    window = Object(xy[0], xy[1], win.get('char'), win.get('name'),
        win.get('color'), win.get('info'), blocks=True,
        ai=StationaryNPC(base_color=win.get('color'),
        interact=win.get('interact'),special=win.get('special')))
    window.ai.special = game_npcs.views[randint(0, len(game_npcs.views)-1)]
    gameconfig.objects.append(window)
    send_to_back(window)

    # create stairs in the last room --------------------------
    gameconfig.stairs_up = Object(new_x, new_y, '<', 'stairs up', gameconfig.STAIRS_COLOR)
    gameconfig.objects.append(gameconfig.stairs_up)
    send_to_back(gameconfig.stairs_up)
    initialize_fov()
