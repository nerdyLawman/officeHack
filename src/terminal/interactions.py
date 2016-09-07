from libtcod import libtcodpy as libtcod
import gameconfig
from interface.rendering import render_all, message

def floppy_write(floppy, name):
    # save/ID an unknown disc
    identified_disc = gameconfig.player.player.identify_item_inventory(floppy.item, name)
    gameconfig.saved_discs.append(identified_disc)
    floppy.item.use()

def remote_look(target):
    # move FOV to another location for a turn
    # NEED TO MOVE FOV!!!!
    gameconfig.REMOTE_FLAG = True
    gameconfig.remote_target = target
    render_all(True)
    libtcod.console_wait_for_keypress(True)
    gameconfig.REMOTE_FLAG = False
    render_all(True)

def revert_control(drone, real_player):
    # switch back to the real player
    drone = gameconfig.drone_holder
    drone.ai = gameconfig.drone_holder.ai
    #drone.ai.owner = gameconfig.drone_holder
    drone.fighter.owner = gameconfig.drone_holder
    drone.player.owner = None
    drone.player = None
    gameconfig.DRONE_FLAE = False
    gameconfig.level_drones.append(drone) #put em back in the running

    gameconfig.player.player = real_player.player
    gameconfig.player.player.inventory = list(gameconfig.real_inventory)
    gameconfig.real_inventory = None #just so we're not storing a useless list
    gameconfig.player.fighter = real_player.fighter
    gameconfig.player.player.owner = real_player
    gameconfig.player.fighter.owner = real_player
    gameconfig.player = real_player

def remote_control(target):
    # switch player control
    gameconfig.drone_holder = target
    gameconfig.drone_holder.ai = target.ai
    gameconfig.drone_holder.ai.owner = target
    gameconfig.drone_holder.fighter.owner = target
    gameconfig.level_drones.remove(target)

    gameconfig.player_at_computer = False
    gameconfig.real_player = gameconfig.player
    gameconfig.real_inventory = list(gameconfig.player.player.inventory)

    target.player = gameconfig.player.player
    target.player.inventory = []
    target.player.owner = target
    target.ai = None

    gameconfig.player = target
    gameconfig.DRONE_FLAG = True
    render_all(True)
