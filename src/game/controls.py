import libtcodpy as libtcod
import gameconfig
from interface.helpers import render_all, message, message_box, menu
from interface.menus import inventory_menu, main_menu
from objects.actions import objects_in_fov

def is_blocked(x, y):
    # test if tile is blocked
    if gameconfig.level_map[x][y].blocked:
        return True
    # now check for any blocking objects
    for obj in gameconfig.objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
    return False

def handle_keys():
    # primary game controls
    # exit
    _p = gameconfig.player
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
        _p.player.move_or_attack(0, -1)
    elif gameconfig.key.vk == libtcod.KEY_DOWN or gameconfig.key.vk == libtcod.KEY_KP2:
        _p.player.move_or_attack(0, 1)
    elif gameconfig.key.vk == libtcod.KEY_LEFT or gameconfig.key.vk == libtcod.KEY_KP4:
        _p.player.move_or_attack(-1, 0)
    elif gameconfig.key.vk == libtcod.KEY_RIGHT or gameconfig.key.vk == libtcod.KEY_KP6:
        _p.player.move_or_attack(1, 0)
    elif gameconfig.key.vk == libtcod.KEY_KP7:
        _p.player.move_or_attack(-1, -1)
    elif gameconfig.key.vk == libtcod.KEY_KP9:
        _p.player.move_or_attack(1, -1)
    elif gameconfig.key.vk == libtcod.KEY_KP1:
        _p.player.move_or_attack(-1, 1)
    elif gameconfig.key.vk == libtcod.KEY_KP3:
        _p.player.move_or_attack(1, 1)
    elif gameconfig.key.vk == libtcod.KEY_KP5:
        message('You wait a turn for the darkness to close in on you.', libtcod.white)
        pass

    else:
        # additional game commands
        gameconfig.key_char = chr(gameconfig.key.c)
        available_commands = ['g - GET ITEM', 'i - INVENTORY', 'l - LOOK', 'd - DROP ITEM',
            ', OR . - GO UP or DOWN STAIRS', 'c - SHOW CHARACTER INFO', 'f - TOGGLE FULLSCREEN']

        # help menu
        if gameconfig.key_char == 'h':
            header = "PRESS the key next to any of the OPTIONS for more INFORMATION."
            menu(header, available_commands)

        # FOV look
        if gameconfig.key_char == 'l':
            header = "SELECT an OBJECT in you FOV for more INFORMATION.\n"
            options = objects_in_fov()
            if len(options) == 0:
                options.append('Nothing to see here.')
            menu(header, options)

        # pick up an item
        if gameconfig.key_char == 'g':
            for obj in gameconfig.objects:
                if obj.x == _p.x and obj.y == _p.y and obj.item:

                    if len(_p.player.inventory) >= 26:
                        return('Your INVENTORY is FULL! Cannot PICK UP ' + self.owner.name.upper() + '.', libtcod.pink)
                    else:
                        message(_p.player.add_item_inventory(obj.item))
                        gameconfig.objects.remove(obj.item.owner)
                        gameconfig.item_count -= 1

        # display inventory
        if gameconfig.key_char == 'i':
            selection = -1
            chosen_item = inventory_menu('PRESS the KEY next to an ITEM to USE it, or ESC to CANCEL', _p.player.inventory)
            if chosen_item is not None:
                chosen_item.use()

        # drop item
        if gameconfig.key_char == 'd':
            chosen_item = inventory_menu('PRESS the KEY next to an ITEM to DROP it.')
            if chosen_item is not None:
                chosen_item.drop()

        # go up down stairs if player is on them
        if gameconfig.key_char == ',' or gameconfig.key_char == '.':
            if gameconfig.stairs_up.x == _p.x and gameconfig.stairs_up.y == _p.y:
                if gameconfig.game_level - 1 > 0:
                    return('stairs up')
            if  gameconfig.stairs_down.x == _p.x and gameconfig.stairs_down.y == _p.y:
                if gameconfig.game_level >= len(gameconfig.game_levels):
                    return('stairs new')
                else:
                    return('stairs down')

        # show character info
        if gameconfig.key_char == 'c':
            level_up_xp = gameconfig.LEVEL_UP_BASE + _p.player.level * gameconfig.LEVEL_UP_FACTOR
            message_box('Character Information\n\nLevel: ' + str(_p.player.level) + '\nExperience: ' + str(_p.fighter.xp) +
                '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(_p.fighter.max_hp) +
                '\nAttack: ' + str(_p.fighter.power) + '\nDefense: ' + str(_p.fighter.defense), 24)

        # toggle fullscreen
        if gameconfig.key_char == 'f':
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        return('no turn') # nothing valid happened
    return('playing') # carry on
