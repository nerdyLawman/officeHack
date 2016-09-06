from libtcod import libtcodpy as libtcod
import gameconfig
from dialogue import dialogues
from dialogue.Dialogue import Dialogue
from interface.menus import terminal_menu

# ---------------------------------------------------------------------
# [ BASE NPC ] --------------------------------------------------------
# ---------------------------------------------------------------------
class BaseNPC:
    # basic NPC ai
    def take_turn(self):
        npc = self.owner
        if libtcod.map_is_in_fov(gameconfig.fov_map, npc.x, npc.y):
            if npc.distance_to(gameconfig.player) >= 2:
                npc.move_towards(gameconfig.player.x, gameconfig.player.y)
            elif gameconfig.player.fighter.hp > 0:
                npc.fighter.attack(gameconfig.player)


# ---------------------------------------------------------------------
# [ TALKER NPC ] ------------------------------------------------------
# ---------------------------------------------------------------------
class TalkerNPC:
    # an NPC that just wont shut up
    def __init__(self, recharge=gameconfig.TALK_RECHARGE):
        self.recharge = recharge

    def take_turn(self):
        npc = self.owner
        if self.recharge < gameconfig.TALK_RECHARGE:
            self.recharge += 1
        elif libtcod.map_is_in_fov(gameconfig.fov_map, npc.x, npc.y):
            if npc.distance_to(gameconfig.player) >= gameconfig.TALK_RANGE:
                npc.move_towards(gameconfig.player.x, gameconfig.player.y)
            else:
                self.recharge = 0
                depth = libtcod.random_get_int(0, 1, 5)
                while depth > 0:
                    dialogue_str = dialogues.level_1[libtcod.random_get_int(0, 1, len(dialogues.level_1)-1)]
                    dialogue = Dialogue(dialogue_str, npc)
                    dialogue.start()
                    depth -= 1


# ---------------------------------------------------------------------
# [ STATIONARY NPC ] --------------------------------------------------
# ---------------------------------------------------------------------
class StationaryNPC:
    # stationary NPC
    def __init__(self, base_color, blink_color=gameconfig.WHITE, interact=None):
        self.blink_color = blink_color
        self.base_color = base_color
        self.interact = interact

    def take_turn(self):
        if self.owner.color == self.blink_color:
            self.owner.color = self.base_color
        else:
            self.owner.color = self.blink_color

    def interact_function(self):
        if self.interact == 'terminal':
            terminal_menu(self)
        else:
            return None


# ---------------------------------------------------------------------
# [ NPC STATES ] ------------------------------------------------------
# ---------------------------------------------------------------------
class ConfusedNPC:
    # an NPC that is totally out of control!
    def __init__(self, old_ai, num_turns=gameconfig.CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
        else:
            self.owner.ai = self.old_ai
            return('The ' + self.owner.name.upper() + ' is no longer CONFUSED.', libtcod.red)


class RepulsedNPC:
    # an NPC that is totally out of control!
    def __init__(self, old_ai, num_turns=gameconfig.REPULSED_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.move_away(gameconfig.player.x, gameconfig.player.y)
            self.num_turns -= 1
        else:
            self.owner.ai = self.old_ai
            return('The ' + self.owner.name.upper() + ' is no longer REPULSED.', libtcod.red)