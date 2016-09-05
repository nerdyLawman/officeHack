from libtcod import libtcodpy as libtcod
import gameconfig
import textwrap
from random import randint
from terminal.interactions import remote_control, revert_control, remote_look, floppy_write

cursor = '_'
prompt = '$'
width = gameconfig.SCREEN_WIDTH
height = gameconfig.SCREEN_HEIGHT
x = gameconfig.SCREEN_WIDTH/2 - width/2
y = gameconfig.SCREEN_HEIGHT/2 - height/2

def cli_refresh(text, command, header_height=2):
    libtcod.console_rect(window, 0, header_height, width, height, True, libtcod.BKGND_SET)
    line_pos = 2
    for line in text:
        libtcod.console_print_ex(window, 1, header_height+line_pos, libtcod.BKGND_NONE, libtcod.LEFT, line)
        line_pos += 2
    libtcod.console_print_ex(window, 1, header_height+line_pos, libtcod.BKGND_NONE, libtcod.LEFT, command)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
    libtcod.console_flush()

def command_entry(command):
    key = libtcod.console_wait_for_keypress(True)
    command = command[len(prompt):-1] #takeout cursor
    if key.vk == libtcod.KEY_ESCAPE:
        return command, False
    if key.vk == libtcod.KEY_BACKSPACE:
        command = command[:-1]
    if key.vk == libtcod.KEY_SPACE:
        command += ' '
    if key.vk == libtcod.KEY_ENTER:
        return command, False
    if key.c >= 64 and key.c <= 127:
        command += chr(key.c)

    return prompt + command + cursor, True #redraw cursor

def cli_window(command=None, selector=None):
    global window
    running = True
    bgnd_color = libtcod.dark_azure
    fgnd_color = libtcod.light_sky
    if not command: command = prompt + cursor
    special_commands = ['exit', 'save', 'read', 'help', 'drone', 'exitdrone', 'remote']
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_set_default_foreground(window, fgnd_color)
    # header
    libtcod.console_rect(window, 0, 0, width, height, True, libtcod.BKGND_SET)
    libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, 'HAPPY TERMINAL V1.0 - 1993')
    text = ['Enter a command to begin. Help for options.']
    while running:
        cli_refresh(text, command) #update screen
        flag = True
        while flag is True and command not in special_commands:
            command, flag = command_entry(command)
            cli_refresh(text, command)
        
        if command != '': text.append(prompt+command)    
        if len(text) > height/2 - 7: del text[:2]
        
        if command == 'exit' or command == 'quit':
            text.append('exited')
            running = False
        
        elif command == 'save':
            text.append('saved!')
        
        elif command == 'read':
            text[:] = []
            if hasattr(selector, 'special'): text.append(selector.special)
            running = file_rw(text)
        
        elif command == 'remote':
            text[:] = []
            running = remote_patch(text)
        
        elif command == 'drone':
            text[:] = []
            running = drone_commander(text)
        
        elif command == 'exitdrone':
            text[:] = []
            running = drone_exit(text)
        
        elif command == 'help':
            helptext = ['type help for options', 'type save to save', 'type exit to exit', 'press ANY KEY.']
            text[:] = helptext
            cli_refresh(text, command)
        
        else:
            text.append('invalid command')
        command = prompt + cursor
        
        if running is True: cli_refresh(text, command)

def valid_disc_name(name):
    valid_names = [disc.inv_id.upper() for disc in gameconfig.saved_discs]
    if name.upper() in valid_names: return True
    return False

def insert_disc(name):
    valid_names = [disc.inv_id.upper() for disc in gameconfig.saved_discs]
    if name.upper() in valid_names: return gameconfig.saved_discs[valid_names.index(name.upper())]
    return None

def file_rw(text, infloppy=None):
    #if in_computer()
    text.append('WELCOME TO DRONE FILE RW V0.75')
    command = prompt + cursor
    if infloppy: floppy = infloppy
    else: floppy = next((inv for inv in gameconfig.player.player.inventory if inv.inv_id == 'floppy disc'), None)
    running = True
    save_flag = False
        
    if floppy is None:
        text.append('SELECT FLOPPY TO LOAD.')
    else:
        save_flag = True
        text.append('FLOPPY CONTENTS: ' + floppy.item.special)
        text.append('enter name to save floppy as:')
    
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cli_refresh(text, command)
        text.append(prompt+command)
        if save_flag:
            floppy_write(floppy, command + ' disc')
            text.append('saved floppy as: ' + command + ' disc.')
            save_flag = False
        else:
            if command == 'exit' or command == 'quit':
                running = False
            elif command == 'list' or command == 'listing':
                for disc in gameconfig.saved_discs:
                    text.append(disc.inv_id)
            elif command == 'identify':
                floppy = next((inv for inv in gameconfig.player.player.inventory if inv.inv_id == 'floppy disc'), None)
                if floppy: text.append('FLOPPY CONTENTS: ' + floppy.item.special)
                else: text.append('no unidentified discs')
            elif valid_disc_name(command):
                floppy = insert_disc(command)
                text.append('FLOPPY CONTENTS: ' + floppy.item.special)
            else:
                text.append('invalid command')
        command = prompt + cursor
        if running is True: cli_refresh(text, command)
    return running


def valid_drone_name(name):
    valid_names = [drone.name.upper() for drone in gameconfig.level_drones]
    if name.upper() in valid_names: return True
    return False

def fetch_drone(name):
    valid_names = [drone.name.upper() for drone in gameconfig.level_drones]
    if name.upper() in valid_names: return gameconfig.level_drones[valid_names.index(name.upper())]
    return None

def drone_commander(text):
    text.append('WELCOME TO DRONE COMMANDER V0.75')
    text.append('enter name of drone to drone into.')
    command = prompt + cursor
    selected_drone = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cli_refresh(text, command)
        text.append(prompt+command)
        if selected_drone:
            if command == 'spam':
                running = False
            else:
                text.append('INCORRECT CODE')
                text.append('Select another DRONE.')
                selected_drone = None
        else:    
            if valid_drone_name(command):
                selected_drone = fetch_drone(command)
                text.append(command.upper() + ' is an acceptable name, enter codeword')
            elif command == 'listing' or command == 'list':
                if len(gameconfig.level_drones) > 0:
                    for drone in gameconfig.level_drones:
                        text.append(drone.name.upper())
                else:
                    text.append('No DRONES on this level.')
            elif command == 'exit':
                text.append('DRONE COMMANDER EXITED.')
                return False
            else:
                text.append('No DRONES match this entry.')
        command = prompt + cursor
        if running is True: cli_refresh(text, command)
        
    if selected_drone: remote_control(selected_drone)
    return running

def drone_exit(text):
    text.append('WELCOME TO DRONE COMMANDER V0.75')
    text.append('QUIT or RESUME')
    command = prompt + cursor
    selected_drone = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cli_refresh(text, command)
        text.append(prompt+command)
        if command == 'exit' or command == 'quit':
            revert_control(gameconfig.player, gameconfig.real_player)
            gameconfig.DRONE_FLAG = False
            # will eventually have to do some housekeeping for the poor drone
            running = False
        elif command == 'resume':
            running = False
        command = prompt + cursor
        if running is True: cli_refresh(text, command)
    return running

def valid_station_name(name):
    valid_names = [station.name.upper() for station in gameconfig.level_terminals]
    if name.upper() in valid_names: return True
    return False

def fetch_station(name):
    valid_names = [station.name.upper() for station in gameconfig.level_terminals]
    if name.upper() in valid_names: return gameconfig.level_terminals[valid_names.index(name.upper())]
    return None

def remote_patch(text):
    text.append('WELCOME TO REMOTE LOOK V0.75')
    text.append('enter name of station to patch.')
    command = prompt + cursor
    selected_station = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cli_refresh(text, command)
        #if valid_station_name(command):
        text.append(prompt+command)
        if command == 'random':
            selected_station = gameconfig.level_terminals[randint(0, len(gameconfig.level_terminals)-1)]
            running = False
        elif command == 'listing' or command == 'list':
            if len(gameconfig.level_terminals) > 1:
                for station in gameconfig.level_terminals:
                    text.append(station.name.upper())
            else:
                text.append('no other stations on this level')
        elif command == 'exit':
            text.append('REMOTE LOOK EXITED.')
            return None
        else:
            text.append('Invalid entry.')
        command = prompt + cursor
        if running is True: cli_refresh(text, command)
    
    if selected_station: remote_look(selected_station)
    return running
        