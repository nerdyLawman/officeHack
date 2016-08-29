import libtcodpy as libtcod
import gameconfig
from interface.helpers import render_all, message, message_box, menu
from interface.menus import inventory_menu, main_menu
#from objects.classes import Fighter

def is_blocked(x, y):
    # test if tile is blocked
    if gameconfig.level_map[x][y].blocked:
        return True
    # now check for any blocking objects
    for obj in gameconfig.objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
    return False

def player_move_or_attack(dx, dy):

    #the coordinates the player is moving to/attacking
    x = gameconfig.player.x + dx
    y = gameconfig.player.y + dy

    #try to find an attackable object there
    target = None
    for obj in gameconfig.objects:
        if obj.fighter and obj.x == x and obj.y == y:
            target = obj
            break

    #attack if target found, move otherwise
    if target is not None:
        gameconfig.player.fighter.attack(target)
    else:
        if not is_blocked(gameconfig.player.x+dx, gameconfig.player.y+dy):
            gameconfig.player.move(dx, dy)

def handle_keys():
    # primary game controls
    # exit
    _player = gameconfig.player
    _stairsU = gameconfig.stairs_up
    _stairsD = gameconfig.stairs_down
    if gameconfig.key.vk == libtcod.KEY_ESCAPE:
        choice = main_menu()
        if choice == 2:
            return 'exit'
        else:
            return 'no turn'

    # 8-D movement arrorw gameconfig.keys or numpad
    if gameconfig.key.vk == libtcod.KEY_UP or gameconfig.key.vk == libtcod.KEY_KP8:
        player_move_or_attack(0, -1)
    elif gameconfig.key.vk == libtcod.KEY_DOWN or gameconfig.key.vk == libtcod.KEY_KP2:
        player_move_or_attack(0, 1)
    elif gameconfig.key.vk == libtcod.KEY_LEFT or gameconfig.key.vk == libtcod.KEY_KP4:
        player_move_or_attack(-1, 0)
    elif gameconfig.key.vk == libtcod.KEY_RIGHT or gameconfig.key.vk == libtcod.KEY_KP6:
        player_move_or_attack(1, 0)
    elif gameconfig.key.vk == libtcod.KEY_KP7:
        player_move_or_attack(-1, -1)
    elif gameconfig.key.vk == libtcod.KEY_KP9:
        player_move_or_attack(1, -1)
    elif gameconfig.key.vk == libtcod.KEY_KP1:
        player_move_or_attack(-1, 1)
    elif gameconfig.key.vk == libtcod.KEY_KP3:
        player_move_or_attack(1, 1)
    elif gameconfig.key.vk == libtcod.KEY_KP5:
        #message('You wait a turn for the darkness to close in on you.', libtcod.white)
        pass

    else:
        # additional game commands
        gameconfig.key_char = chr(gameconfig.key.c)

        # pick up an item
        if gameconfig.key_char == 'g':
            for obj in gameconfig.objects:
                if obj.x == _player.x and obj.y == _player.y and obj.item:

                    if len(_player.player.inventory) >= 26:
                        return('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.pink)
                    else:
                        message(_player.player.add_item_inventory(obj.item))
                        gameconfig.objects.remove(obj.item.owner)
                        gameconfig.item_count -= 1

        # go up down stairs if player is on them
        if gameconfig.key_char == ',' or gameconfig.key_char == '.':
            if _stairsU.x == _player.x and _stairsU.y == _player.y:
                if gameconfig.game_level - 1 > 0:
                    return('stairs up')
            if  _stairsD.x == _player.x and _stairsD.y == _player.y:
                if gameconfig.game_level >= len(gameconfig.game_levels):
                    return('stairs new')
                else:
                    return('stairs down')

        # display inventory
        if gameconfig.key_char == 'i':
            selection = -1
            chosen_item = inventory_menu('Press the key next to an item to use it, or ESC to cancel\n', _player.player.inventory)
            if chosen_item is not None:
                chosen_item.use(_player.fighter)

        # drop item
        if gameconfig.key_char == 'd':
            chosen_item = inventory_menu('Press the key next to an item to drop it.\n')
            if chosen_item is not None:
                chosen_item.drop()

        # show character info
        if gameconfig.key_char == 'c':
            level_up_xp = gameconfig.LEVEL_UP_BASE + _player.player.level * gameconfig.LEVEL_UP_FACTOR
            message_box('Character Information\n\nLevel: ' + str(_player.player.level) + '\nExperience: ' + str(_player.fighter.xp) +
                '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(_player.fighter.max_hp) +
                '\nAttack: ' + str(_player.fighter.power) + '\nDefense: ' + str(_player.fighter.defense), 24)

        # toggle fullscreen
        if gameconfig.key_char == 'f':
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        return('no turn') # nothing valid happened
    return('playing') # carry on
