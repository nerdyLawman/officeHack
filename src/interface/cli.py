import libtcodpy as libtcod
import gameconfig
import textwrap

def cli_refresh(window, width, height, x, y, text, header_height=2):
    libtcod.console_rect(window, 0, header_height, width, height, True, libtcod.BKGND_SET)
    libtcod.console_print_ex(window, 1, header_height+1, libtcod.BKGND_NONE, libtcod.LEFT, text)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)
    libtcod.console_flush()

def cli_window(text=None):
    bgnd_color = libtcod.dark_azure
    fgnd_color = libtcod.light_sky
    cursor = '_'
    if not text: text = cursor
    width = gameconfig.SCREEN_WIDTH
    height = gameconfig.SCREEN_HEIGHT
    x = gameconfig.SCREEN_WIDTH/2 - width/2
    y = gameconfig.SCREEN_HEIGHT/2 - height/2

    window = libtcod.console_new(width, height)
    libtcod.console_set_default_background(window, bgnd_color)
    libtcod.console_set_default_foreground(window, fgnd_color)
    # header
    libtcod.console_rect(window, 0, 0, width, height, True, libtcod.BKGND_SET)
    libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, 'HAPPY TERMINAL V1.0 - 1993')
    cli_refresh(window, width, height, x, y, text) #update screen

    while True:
        while True:
            key = libtcod.console_wait_for_keypress(True)
            text = text[:-1] #takeout cursor
            if key.vk == libtcod.KEY_ESCAPE:
                return None
            if key.vk == libtcod.KEY_BACKSPACE:
                text = text[:-1]
            if key.vk == libtcod.KEY_SPACE:
                text += ' '
            if key.vk == libtcod.KEY_ENTER:
                break
            if key.c >= 64 and key.c <= 127:
                text += chr(key.c)

            text += cursor #redraw cursor
            cli_refresh(window, width, height, x, y, text)

        if text == 'exit':
            print('exited')
            return None
        if text == 'save':
            print('saved!')
            return None
        if text == 'help':
            helptext = 'type help for options\ntype save to save\ntype exit to exit\n\npress ANY KEY.'
            cli_refresh(window, width, height, x, y, helptext)
            text = cursor
        libtcod.console_wait_for_keypress(True)
        cli_refresh(window, width, height, x, y, text)
