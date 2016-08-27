import libtcodpy as libtcod
import gameconfig
from interface.helpers import render_all, message, message_box, menu
from interface.menus import inventory_menu
from objects.classes import Fighter

"""def target_tile(max_range=None):
    global key, mouse
    # returns x, y of a tile selected by a mouseclick
    while True:
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        render_all()

        (x, y) = (mouse.cx, mouse.cy)
        if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and
            (max_range is None or player.distance(x, y) <= max_range)):
            return(x, y)
        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return(None, None)

def target_npc(objects, max_range=None):
    # select NPC in range
    while True:
        (x, y) = target_tile(max_range)
        if x is None:
            return None

        for obj in objects:
            if obj.x == x and obj.y == y and obj.fighter and obj != player:
                return obj

def get_names_under_mouse(objects):
    # return name of object under mouse pointer
    global mouse
    (x, y) = (mouse.cx, mouse.cy)
    names = [obj.name for obj in objects
        if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]
    names = ', '.join(names)
    return names.capitalize()"""

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

def handle_keys(player, objects, level_map, key, mouse):
    # primary game controls
    # exit
    if key.vk == libtcod.KEY_ESCAPE:
        selected = 0
        return('exit')

    # 8-D movement arrorw keys or numpad
    if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
        player_move_or_attack(player, objects, level_map, 0, -1)
    elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
        player_move_or_attack(player, objects, level_map, 0, 1)
    elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
        player_move_or_attack(player, objects, level_map, -1, 0)
    elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
        player_move_or_attack(player, objects, level_map, 1, 0)
    elif key.vk == libtcod.KEY_KP7:
        player_move_or_attack(player, objects, level_map, -1, -1)
    elif key.vk == libtcod.KEY_KP9:
        player_move_or_attack(player, objects, level_map, 1, -1)
    elif key.vk == libtcod.KEY_KP1:
        player_move_or_attack(player, objects, level_map, -1, 1)
    elif key.vk == libtcod.KEY_KP3:
        player_move_or_attack(player, objects, level_map, 1, 1)
    elif key.vk == libtcod.KEY_KP5:
        #message('You wait a turn for the darkness to close in on you.', libtcod.white)
        pass
        
    else:
        # additional game commands
        key_char = chr(key.c)

        # pick up an item
        if key_char == 'g':
            for obj in objects:
                if obj.x == player.x and obj.y == player.y and obj.item:
                    if len(player.player.inventory) >= 26:
                        return('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.pink)
                    else:
                        player.player.add_item_inventory(obj.item)
                        objects.remove(obj.item.owner)
        
        # go down stairs if player is on them
        if key_char == ',' or key_char == '.':
            if stairs.x == player.x and stairs.y == player.y:
                next_level()
        
        # display inventory
        if key_char == 'i':
            selection = -1
            chosen_item = inventory_menu('Press the key next to an item to use it, or ESC to cancel\n', player.player.inventory)
            if chosen_item is not None:
                chosen_item.use(player.fighter)
        
        # drop item
        if key_char == 'd':
            chosen_item = inventory_menu('Press the key next to an item to drop it.\n')
            if chosen_item is not None:
                chosen_item.drop()
        
        # show character info
        if key_char == 'c':
            level_up_xp = gameconfig.LEVEL_UP_BASE + player.level * gameconfig.LEVEL_UP_FACTOR
            message_box('Character Information\n\nLevel: ' + str(player.level) + '\nExperience: ' + str(player.fighter.xp) +
                '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(player.fighter.max_hp) +
                '\nAttack: ' + str(player.fighter.power) + '\nDefense: ' + str(player.fighter.defense), 24)
        
        # toggle fullscreen
        if key_char == 'f':
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        return('no turn') # nothing valid happened
    return('playing') # carry on
