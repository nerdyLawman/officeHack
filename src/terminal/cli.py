from libtcod import libtcodpy as libtcod
import time
import gameconfig
import textwrap
import threading
from game import game_messages
from random import randint
from terminal.interactions import remote_control, revert_control, remote_look, floppy_write
from interface.rendering import draw_object

cursor = gameconfig.TERMINAL_CURSOR
prompt = gameconfig.TERMINAL_PROMPT
width = gameconfig.SCREEN_WIDTH
height = gameconfig.SCREEN_HEIGHT
x = gameconfig.SCREEN_WIDTH/2 - width/2
y = gameconfig.SCREEN_HEIGHT/2 - height/2
window = libtcod.console_new(width, height)

class Cursor():
    def __init__(self, x, y, color, char='_'):
        self.x = x
        self.y = y
        self.color = color
        self.char = char

bgnd_color = libtcod.dark_azure
fgnd_color = libtcod.light_sky
cur = Cursor(len(prompt), 1, fgnd_color)

class BlinkingCursor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

    def run(self):
        while self.running is True:
            if cur.color == fgnd_color: cur.color = bgnd_color
            else: cur.color = fgnd_color
            libtcod.console_set_char_background(window, cur.x, cur.y, cur.color, flag=libtcod.BKGND_SET)
            libtcod.console_put_char(window, cur.x, cur.y, '_', flag=libtcod.BKGND_DEFAULT)
            libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
            libtcod.console_flush()
            time.sleep(0.35)

    def stop(self):
        self.running = False


def cli_refresh(text, command, header_height=2):
    libtcod.console_rect(window, 0, header_height, width, height, True, libtcod.BKGND_SET)
    line_pos = 2
    for line in text:
        libtcod.console_print_ex(window, 1, header_height+line_pos, libtcod.BKGND_NONE, libtcod.LEFT, line)
        line_pos += 2
    cur.y = header_height + line_pos
    libtcod.console_print_ex(window, 1, header_height+line_pos, libtcod.BKGND_NONE, libtcod.LEFT, command)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
    libtcod.console_flush()


def command_entry(command):
    key = libtcod.console_wait_for_keypress(True)
    command = command[len(prompt):] #takeout prompt
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
    return prompt + command, True


def cli_window(command=None, selector=None):
    global window, BLINK
    running = True
    BLINK = True

    bc = BlinkingCursor()
    bc.start()

    gameconfig.CURRENT_TRACK.switch_track(gameconfig.BACKGROUND_MUSIC['terminal'])
    bgnd_color = libtcod.dark_azure
    fgnd_color = libtcod.light_sky
    if not command: command = prompt
    special_commands = ['exit', 'save', 'read', 'help', 'drone', 'dronedead', 'exitdrone', 'remote']
    #window = libtcod.console_new(width, height) declared up top as global
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_set_default_foreground(window, fgnd_color)
    # header
    libtcod.console_rect(window, 0, 0, width, height, True, libtcod.BKGND_SET)
    libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, game_messages.TERMINAL_TITLE)
    text = [game_messages.TERMINAL_START_MESSAGE]

    while running:
        cli_refresh(text, command) #update screen
        flag = True
        while flag is True and command not in special_commands:
            command, flag = command_entry(command)
            cur.x = len(command)+1
            cli_refresh(text, command)

        if command != '': text.append(prompt+command)
        if len(text) > height/2 - 7: del text[:2]

        # EXIT -------------------------
        if command == 'exit' or command == 'quit':
            text.append('exited')
            running = False

        # SAVE --------------------------
        elif command == 'save':
            text.append('saved!')

        # READ ----------------------
        elif command == 'read':
            text[:] = []
            if hasattr(selector, 'special'): text.append(selector.special)
            running = file_rw(text)

        # REMOTE -----------------------
        elif command == 'remote':
            text[:] = []
            #running = remote_patch(text)
            run_program('remote')

        # DRONE -------------------------
        elif command == 'drone':
            text[:] = []
            running = drone_commander(text)

        elif command == 'dronedead':
            text[:] = ['Your drone died. EXIT or SELECT ANOTHER.']
            running = drone_commander(text)

        # EXIT DRONE ---------------------
        elif command == 'exitdrone':
            text[:] = []
            running = drone_exit(text)

        # HELP ------------------------
        elif command == 'help':
            helptext = ['type help for options', 'type save to save', 'type exit to exit', 'press ANY KEY.']
            text[:] = helptext
            cli_refresh(text, command)

        # INVALID COMMAND ----------------
        else:
            text.append('invalid command')
        command = prompt
        cur.x = len(command)+1
        if running is False:
            gameconfig.CURRENT_TRACK.switch_track(gameconfig.BACKGROUND_MUSIC['level_1'])

    bc.stop()


# ---------------------------------------------------------------------
# [ FILE I/O ] --------------------------------------------------------
# ---------------------------------------------------------------------
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
    command = prompt
    cur.x = len(command)+1
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
            cur.x = len(command)+1
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
        command = prompt
        cur.x = len(command)+1
    return running


# ---------------------------------------------------------------------
# [ DRONE CONTROL ] ---------------------------------------------------
# ---------------------------------------------------------------------
def valid_drone_name(name):
    valid_names = [drone.name.upper() for drone in gameconfig.level_drones]
    if name.upper() in valid_names: return True
    return False

def fetch_drone(name):
    valid_names = [drone.name.upper() for drone in gameconfig.level_drones]
    if name.upper() in valid_names: return gameconfig.level_drones[valid_names.index(name.upper())]
    return None

def drone_commander(text):
    text.insert(0, 'WELCOME TO DRONE COMMANDER V0.75')
    text.insert(1, 'enter name of drone to drone into.')
    command = prompt
    cur.x = len(command)+1
    selected_drone = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cur.x = len(command)+1
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
        command = prompt
        cur.x = len(command)+1

    if selected_drone: remote_control(selected_drone)
    return running

def drone_exit(text):
    text.append('WELCOME TO DRONE COMMANDER V0.75')
    text.append('QUIT or RESUME')
    command = prompt
    cur.x = len(command)+1
    selected_drone = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cur.x = len(command)+1
            cli_refresh(text, command)
        text.append(prompt+command)
        if command == 'exit' or command == 'quit':
            revert_control(gameconfig.player, gameconfig.real_player)
            gameconfig.DRONE_FLAG = False
            # will eventually have to do some housekeeping for the poor drone
            running = False
        elif command == 'resume':
            running = False
        command = prompt
        cur.x = len(command)+1
    return running


# ---------------------------------------------------------------------
# [ REMOTE HACKING ] --------------------------------------------------
# ---------------------------------------------------------------------
def valid_station_name(name):
    valid_names = [station.name.upper() for station in gameconfig.level_terminals]
    if name.upper() in valid_names: return True
    return False


def fetch_station(name):
    valid_names = [station.name.upper() for station in gameconfig.level_terminals]
    if name.upper() in valid_names: return gameconfig.level_terminals[valid_names.index(name.upper())]
    return None


def remote_program(command):
    if command == 'random':
        if len(gameconfig.level_terminals) > 1:
            gameconfig.level_terminals.remove(gameconfig.player_at_computer)
            remote_look(gameconfig.level_terminals[randint(0, len(gameconfig.level_terminals)-1)])
            gameconfig.level_terminals.append(gameconfig.player_at_computer)
            running = False
        else:
            return('No other terminal stations on this level')
    elif command == 'listing' or command == 'list':
        if len(gameconfig.level_terminals) > 1:
            return([station.name.upper() for station in gameconfig.level_terminals])
        else:
            return('no other stations on this level')

def remote_patch(text):
    text.append('WELCOME TO REMOTE LOOK V0.75')
    text.append('enter name of station to patch.')
    command = prompt
    cur.x = len(command)+1
    selected_station = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cur.x = len(command)+1
            cli_refresh(text, command)
        #if valid_station_name(command):
        text.append(prompt+command)
        if command == 'random':
            if len(gameconfig.level_terminals) > 1:
                gameconfig.level_terminals.remove(gameconfig.player_at_computer)
                selected_station = gameconfig.level_terminals[randint(0, len(gameconfig.level_terminals)-1)]
                gameconfig.level_terminals.append(gameconfig.player_at_computer)
                running = False
            else:
                text.append('No other terminal stations on this level')
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
        command = prompt
        cur.x = len(command)+1

    if selected_station: remote_look(selected_station)
    return running


def run_program(program):
    text = []
    text.append('WELCOME TO ' + program + ' NAME')
    #text.append('enter name of station to patch.')
    command = prompt
    cur.x = len(command)+1
    selected_station = None
    running = True
    while running:
        cli_refresh(text, command)
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cur.x = len(command)+1
            cli_refresh(text, command)
            #specific program stuff
            if program == 'remote':
                text.append(remote_program(command))
            if command == 'exit':
                text.append('PROGRAM EXITED.')
                return None
            else:
                text.append('Invalid entry.')
            command = prompt
            cur.x = len(command)+1
