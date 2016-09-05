import gameconfig
from interface.menus import menu
import libtcodpy as libtcod
import json


class Dialogue:

    def __init__(self, dialogue, npc):
        self.current_dialogue = json.loads(dialogue)
        self.npc = npc
        self.elements = self.current_dialogue['elements']
        self.element = None

    def start(self):
        self._set_current_element('init')
        self._next()

    def get_dialogue_element(self, el_id):
        self.elements = self.current_dialogue['elements']
        for el in self.elements:
            if el['id'] == el_id:
                return el

    def _set_current_element(self, id):
        self.element = self.get_dialogue_element(id)

    def _draw_dialogue_screen(self):
        img = libtcod.image_load(self.npc.fighter.portrait)
        portrait = libtcod.console_new(50, 20)
        libtcod.console_set_default_background(portrait, gameconfig.MENU_BKGND)
        libtcod.console_set_default_foreground(portrait, libtcod.white)
        libtcod.console_rect(portrait, 0, 0, 50, 20, False, libtcod.BKGND_SET)
        libtcod.console_print_ex(portrait, 10, 10, libtcod.BKGND_NONE,
                                 libtcod.LEFT, self.npc.name)
        libtcod.image_blit_2x(img, portrait, 1, 1, 0, 0, -1, -1)
        libtcod.console_blit(portrait, 0, 0, 50, 20, 0,
                             gameconfig.SCREEN_WIDTH/2-25,
                             gameconfig.SCREEN_HEIGHT/2-16, 1.0, 1.0)

    def _handle_player_choices(self):
        choices = []
        for i in self.element['choices']:
            choices.append(i['text'])
        if len(self.element['choices']) == 0:
            choices.append('End.')
        index = menu(self.element['text'][0], choices)
        if index is None or len(choices) == 0:
            return None
        for i in self.element['choices']:
            if i['text'] == choices[index]:
                el = self.get_dialogue_element(i['followup'])
                if el is not None:
                    self._set_current_element(i['followup'])
                    self._next()
                else:
                    return

    def _next(self):
        self._draw_dialogue_screen()
        self._handle_player_choices()
