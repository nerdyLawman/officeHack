from libtcod import libtcodpy as libtcod
import gameconfig
from game import game_messages
from interface.rendering import render_all, message, fetch_message
from interface.menus import inventory_menu, main_menu, message_box, menu
from objects.actions import objects_in_fov
from terminal.cli import cli_window

def handle_keys():
    # primary game controls
    _p = gameconfig.player #for ease of ref

    # Exit ------------------------------------------
    if gameconfig.key.vk == libtcod.KEY_ESCAPE:
        if gameconfig.DRONE_FLAG is True:
            cli_window('exitdrone')
        else:
            choice = main_menu()
            if choice == 2: return 'exit'
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
        fetch_message('WAIT_MESSAGE')
        pass

    else: # additional game commands  -------------------------------------
        gameconfig.key_char = chr(gameconfig.key.c)
        available_commands = [
            'h - HELP MENU',
            'g - GET ITEM',
            'i - INVENTORY',
            'c - SHOW CHARACTER INFO',
            'l - LOOK',
            'd - DROP ITEM',
            ', - GO UP or DOWN STAIRS',
            '. - GO UP or DOWN STAIRS',
            'f - TOGGLE FULLSCREEN',
        ]

        # HELP MENU --------------------------------- [h]
        if gameconfig.key_char == 'h':
            selected_entry = menu(game_messages.HELP_HEADER, available_commands)

        # FOV LOOK ------------------------------- [l]
        elif gameconfig.key_char == 'l':
            options = objects_in_fov()
            selected_object = menu(game_messages.LOOK_HEADER, [obj.name.upper() for obj in options])
            if selected_object is not None: message_box(options[selected_object].info)

        # PICK UP ITEM ------------------------- [g]
        elif gameconfig.key_char == 'g':
            for obj in gameconfig.objects:
                if obj.x == _p.x and obj.y == _p.y and obj.item:
                    if len(_p.player.inventory) >= gameconfig.MAX_INVENTORY: # INVENTORY IS FULL!
                        return(game_messages.FULL_INVENTORY + self.owner.name.upper() + '.', libtcod.pink)
                    else:
                        if obj.item.is_instant is True: obj.item.use()
                        message(_p.player.add_item_inventory(obj.item))

        # DROP ITEM ------------------------- [d]
        elif gameconfig.key_char == 'd':
            chosen_item = inventory_menu(game_message.DROP_HEADER, _p.player.inventory)
            if chosen_item is not None:
                message(_p.player.drop_item_inventory(chosen_item, _p.x, _p.y))

        # INVENTORY ------------------------- [i]
        elif gameconfig.key_char == 'i':
            selection = -1
            chosen_item = inventory_menu(game_messages.INVENTORY_HEADER, _p.player.inventory)
            if chosen_item:
                chosen_item.use()

        # CHARACTER INFO --------------------- [c]
        elif gameconfig.key_char == 'c':
            level_up_xp = gameconfig.LEVEL_UP_BASE + _p.player.level * gameconfig.LEVEL_UP_FACTOR
            message_box(_p.name.upper() + ' Information\n\nLevel: ' + str(_p.player.level) + '\nExperience: ' + str(_p.fighter.xp) +
                '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(_p.fighter.max_hp) +
                '\nAttack: ' + str(_p.fighter.power) + '\nDefense: ' + str(_p.fighter.defense), 24)

        # UP OR DOWN STAIRS --------------------------------------- [,] [.]
        elif gameconfig.key_char == ',' or gameconfig.key_char == '.':
            if gameconfig.stairs_up.x == _p.x and gameconfig.stairs_up.y == _p.y:
                if gameconfig.game_level - 1 > 0:
                    return('stairs up')
            if  gameconfig.stairs_down.x == _p.x and gameconfig.stairs_down.y == _p.y:
                if gameconfig.game_level >= len(gameconfig.game_levels):
                    return('stairs new')
                else:
                    return('stairs down')

        # TOGGLE FULLSCREEN ---------------- [f]
        elif gameconfig.key_char == 'f':
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        return('no turn') # nothing valid happened
    return('playing') # carry on
