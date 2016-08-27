import libtcodpy as libtcod
import gameconfig
from interface import interfaceconfig
from interface.helpers import render_all
from objects.classes import Fighter

def is_blocked(level_map, objects, x, y):
    # test if tile is blocked
    if level_map[x][y].blocked:
        return True
    # now check for any blocking objects
    for obj in objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
    return False

def player_move_or_attack(player, objects, level_map, dx, dy):

    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    #try to find an attackable object there
    target = None
    for obj in objects:
        if obj.fighter and obj.x == x and obj.y == y:
            target = obj
            break

    #attack if target found, move otherwise
    if target is not None:
        player.fighter.attack(target)
    else:
        if not is_blocked(level_map, objects, player.x+dx, player.y+dy):
            player.move(dx, dy)

def handle_keys(player, objects, level_map):
    # primary game controls
    # exit
    if interfaceconfig.key.vk == libtcod.KEY_ESCAPE:
        selected = 0
        return('exit')

    # 8-D movement arrorw interfaceconfig.keys or numpad
    if interfaceconfig.key.vk == libtcod.KEY_UP or interfaceconfig.key.vk == libtcod.KEY_KP8:
        player_move_or_attack(player, objects, level_map, 0, -1)
    elif interfaceconfig.key.vk == libtcod.KEY_DOWN or interfaceconfig.key.vk == libtcod.KEY_KP2:
        player_move_or_attack(player, objects, level_map, 0, 1)
    elif interfaceconfig.key.vk == libtcod.KEY_LEFT or interfaceconfig.key.vk == libtcod.KEY_KP4:
        player_move_or_attack(player, objects, level_map, -1, 0)
    elif interfaceconfig.key.vk == libtcod.KEY_RIGHT or interfaceconfig.key.vk == libtcod.KEY_KP6:
        player_move_or_attack(player, objects, level_map, 1, 0)
    elif interfaceconfig.key.vk == libtcod.KEY_KP7:
        player_move_or_attack(player, objects, level_map, -1, -1)
    elif interfaceconfig.key.vk == libtcod.KEY_KP9:
        player_move_or_attack(player, objects, level_map, 1, -1)
    elif interfaceconfig.key.vk == libtcod.KEY_KP1:
        player_move_or_attack(player, objects, level_map, -1, 1)
    elif interfaceconfig.key.vk == libtcod.KEY_KP3:
        player_move_or_attack(player, objects, level_map, 1, 1)
    elif interfaceconfig.key.vk == libtcod.KEY_KP5:
        #message('You wait a turn for the darkness to close in on you.', libtcod.white)
        pass

    else:
        # additional game commands
        interfaceconfig.key_char = chr(interfaceconfig.key.c)

        # pick up an item
        if interfaceconfig.key_char == 'g':
            for obj in objects:
                if obj.x == player.x and obj.y == player.y and obj.item:
                    obj.item.pick_up()
                    break

        # go down stairs if player is on them
        if interfaceconfig.key_char == ',' or interfaceconfig.key_char == '.':
            if stairs.x == player.x and stairs.y == player.y:
                next_level()

        # display inventory
        if interfaceconfig.key_char == 'i':
            selection = -1
            chosen_item = inventory_menu('Press the key next to an item to use it, or ESC to cancel\n')
            if chosen_item is not None:
                chosen_item.use()

        # drop item
        if interfaceconfig.key_char == 'd':
            chosen_item = inventory_menu('Press the key next to an item to drop it.\n')
            if chosen_item is not None:
                chosen_item.drop()

        # show character info
        if interfaceconfig.key_char == 'c':
            level_up_xp = gameconfig.LEVEL_UP_BASE + player.level * gameconfig.LEVEL_UP_FACTOR
            message_box('Character Information\n\nLevel: ' + str(player.level) + '\nExperience: ' + str(player.fighter.xp) +
                '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(player.fighter.max_hp) +
                '\nAttack: ' + str(player.fighter.power) + '\nDefense: ' + str(player.fighter.defense), 24)

        # toggle fullscreen
        if interfaceconfig.key_char == 'f':
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        return('no turn') # nothing valid happened
    return('playing') # carry on
