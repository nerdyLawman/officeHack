import gameconfig
from interface.menus import menu
import libtcodpy as libtcod
import json

from pprint import pprint

current_dialogue = None

def init_dialogue(dialogue, npc):
    global current_dialogue
    parsed_dialogue = json.loads(dialogue)
    current_dialogue = parsed_dialogue
    elements = parsed_dialogue['elements']
    el = get_dialogue_element('init')
    cont_dialogue(el, npc)

def get_dialogue_element(el_id):
    elements = current_dialogue['elements']
    for el in elements:
       if el['id'] == el_id:
           return el

def cont_dialogue(element, npc):
    draw_dialogue_screen(element, npc)
    handle_player_choices(element, npc)

def draw_dialogue_screen(element, npc):
    img = libtcod.image_load(npc.fighter.portrait)
    portrait = libtcod.console_new(50, 20)
    libtcod.console_set_default_background(portrait, gameconfig.MENU_BKGND)
    libtcod.console_set_default_foreground(portrait, libtcod.white)
    libtcod.console_rect(portrait, 0, 0, 50, 20, False, libtcod.BKGND_SET)
    libtcod.console_print_ex(portrait, 10, 10, libtcod.BKGND_NONE, libtcod.LEFT, npc.name)
    libtcod.image_blit_2x(img, portrait, 1, 1, 0, 0, -1, -1) #2x size 16x20
    libtcod.console_blit(portrait, 0, 0, 50, 20, 0, gameconfig.SCREEN_WIDTH/2-25, gameconfig.SCREEN_HEIGHT/2-16, 1.0, 1.0)

def handle_player_choices(element, npc):
    choices = []
    for i in element['choices']:
        choices.append(i['text'])
    if len(element['choices']) == 0:
        choices.append('End.')
    index = menu(element['text'][0], choices)
    if index is None or len(choices) == 0: return None
    for i in element['choices']:
        if i['text'] == choices[index]:
            el = get_dialogue_element(i['followup'])
            if el != None:
                cont_dialogue(el, npc)
            else:
                return
