import libtcodpy as libtcod
import gameconfig
import textwrap

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

def cli_window(command=None):
    global window
    bgnd_color = libtcod.dark_azure
    fgnd_color = libtcod.light_sky
    if not command: command = prompt + cursor

    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_set_default_foreground(window, fgnd_color)
    # header
    libtcod.console_rect(window, 0, 0, width, height, True, libtcod.BKGND_SET)
    libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, 'HAPPY TERMINAL V1.0 - 1993')
    text = ['Enter a command to begin. Help for options.']
    cli_refresh(text, command) #update screen
    while True:
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cli_refresh(text, command)
            
        if command == 'exit' or command == 'quit':
            text.append('exited')
            return None
        elif command == 'save':
            text.append('saved!')
        elif command == 'drone':
            drone_commander(text)
        elif command == 'help':
            helptext = ['type help for options', 'type save to save', 'type exit to exit', 'press ANY KEY.']
            text[:] = helptext
            cli_refresh(text, command)
        else:
            text.append('invalid command')
        command = prompt + cursor
        cli_refresh(text, command)

def drone_commander(text):
    command = prompt + cursor
    text[:] = []
    text.append('WELCOME TO DRONE COMMANDER V0.75')
    text.append('enter name of drone to drone into.')
    cli_refresh(text, command)
    while True:
        flag = True
        while flag is True:
            command, flag = command_entry(command)
            cli_refresh(text, command)
            
        if command == 'dave':
            text.append('dave is an acceptable name, enter codeword')
        if command == 'exit':
            text.append('DRONE COMMANDER EXITED.')
            return None
        command = prompt + cursor
        cli_refresh(text, command)
        