from libtcod import libtcodpy as libtcod
import gameconfig
from interface.rendering import message, send_to_back
from terminal.interactions import revert_control

def player_death(player):
    # you ded
    message('You have DIED!', libtcod.white)
    player.char = '%'
    player.color = libtcod.dark_red
    return 'dead' #game_state

def npc_death(npc):
    # npc death
    xp = npc.fighter.xp
    if npc.fighter.drone is True: gameconfig.level_drones.remove(npc)
    message(npc.name.upper() + ' is DEAD! You gain ' + str(xp) + 'XP!', libtcod.cyan)
    npc.char = '%'
    npc.color = libtcod.dark_red
    npc.blocks = False
    npc.fighter = None
    npc.ai = None
    npc.name = 'remains of ' + npc.name.upper()
    send_to_back(npc)
    gameconfig.npc_count -= 1
    return xp

def drone_death(drone):
    # kill the drone and switch back to the player
    revert_control(drone, gameconfig.real_player)
    gameconfig.level_drones.remove(drone)
    npc_death(drone)
    gameconfig.DRONE_FLAG = False
    #cli_window('drone') eventually get it so you go back to the terminal after drone death
    gameconfig.player_at_computer = True