import libtcodpy as libtcod
import gameconfig
from interface.helpers import message

def send_to_back(target, objects):
    #gotta get objects here somehow
    objects.remove(target)
    objects.insert(0, target_npc)

def player_death(player):
    # you ded
    message('You died!', libtcod.white)
    player.char = '%'
    player.color = libtcod.dark_red
    return 'dead' #game_state

def npc_death(npcc):
    npc = npcc.owner
    # npc death
    message(npc.name.upper() + ' is dead! You gain ' + str(npc.fighter.xp) + 'XP!', libtcod.cyan)
    npc.char = '%'
    npc.color = libtcod.dark_red
    npc.blocks = False
    npc.fighter = None
    npc.ai = None
    npc.name = 'remains of ' + npc.name.upper()
    gameconfig.npc_count -= 1
    #npc.send_to_back(npc, objects) #gotta get objects here or take send_to_back call outside npc_death

def closest_npc(max_range):
    # find closest enemy to max range and in FOV
    closest_npc = None
    closest_dist = max_range + 1

    for obj in objects:
        if obj.fighter and not obj == player and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
            dist = player.distance_to(obj)
            if dist < closest_dist:
                closest_npc = obj
                closest_dist = dist
    return closest_npc