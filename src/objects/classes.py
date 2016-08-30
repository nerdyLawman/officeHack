import libtcodpy as libtcod
import math
import gameconfig
from objects.actions import npc_death, player_death, send_to_back
from game.controls import is_blocked
from interface.menus import conversation

class Object:
    # generic object
    def __init__(self, x, y, char, name, color, blocks=False, player=None, fighter=None, ai=None, item=None):
      self.x = x
      self.y = y
      self.char = char
      self.name = name
      self.color = color
      self.blocks = blocks

      self.player = player
      if self.player:
        self.player.owner = self

      self.fighter = fighter
      if self.fighter:
          self.fighter.owner = self

      self.ai = ai
      if self.ai:
          self.ai.owner = self

      self.item = item
      if self.item:
          self.item.owner = self

    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
          self.x += dx
          self.y += dy

    def move_towards(self, target_x, target_y):
      dx = target_x - self.x
      dy = target_y - self.y
      distance = math.sqrt(dx ** 2 + dy ** 2)

      dx = int(round(dx / distance))
      dy = int(round(dx / distance))
      self.move(dx, dy)

    def distance_to(self, other):
      dx = other.x - self.x
      dy = other.y - self.y
      return math.sqrt(dx ** 2 + dy ** 2)

class Player:
    # the player
    def __init__(self, inventory, level=1):
        self.inventory = inventory
        self.level = level

    def add_item_inventory(self, item):
        self.inventory.append(item)
        return("You picked up an " + item.owner.name.upper() + ".")

class Fighter:
    # Object with combat-related properties and methods
    def __init__(self, hp, defense, power, xp):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
        if self.hp <= 0:
            if self.owner.player == None:
                # if you kill em, gain exp
                npc_death(self.owner)
                send_to_back(self.owner)
                #player.fighter.xp += self.xp
                #check_level_up()
            else:
                player_death(self.owner)

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            return(self.owner.name.upper() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.', libtcod.orange)
        else:
            return(self.owner.name.upper() + ' attacks ' + target.name + ' but it has no effect!', libtcod.cyan)

class Talker:
    def take_turn(self):
        topics = [ 'What\s the deal with BECKY?\n',
            'Can you believe this weather we\ve been having?\n',
            'I\'m thinking about getting another iPhone.\n',
            'Can you come take a look at something on my computer for me?\n',
            'Do you think JEFF is acting strange?\n',
            'I can\'t believe they didn\'t offer me the CPM position!\n',
            'Do you like this new coffee better? It\'s ITALIAN.\n',
            'Did you see the picture of my DOG I posted on the office board yet?\n',
            'Did you get up to anything fun last night?\n',
            'Whenever you get around to it, would you mind wiping down the coffee machine?\n',
            'What do you think of LUCY?\n',        
        ]
        npc = self.owner
        if libtcod.map_is_in_fov(gameconfig.fov_map, npc.x, npc.y):
            if npc.distance_to(gameconfig.player) >= 2:
                npc.move_towards(gameconfig.player.x, gameconfig.player.y)
            else:
                depth = libtcod.random_get_int(0, 1, 5)
                while depth > 0:
                    topic = topics[libtcod.random_get_int(0, 1, len(topics)-1)]
                    conversation(topic)
                    depth -= 1
    
class BaseNPC:
    # basic NPC ai
    def take_turn(self):
        npc = self.owner
        if libtcod.map_is_in_fov(gameconfig.fov_map, npc.x, npc.y):
            if npc.distance_to(gameconfig.player) >= 2:
                npc.move_towards(gameconfig.player.x, gameconfig.player.y)

            elif gameconfig.player.fighter.hp > 0:
                npc.fighter.attack(gameconfig.player)


# states of NPCs
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
            return('The ' + self.owner.name.upper() + ' is no longer confused.', libtcod.red)

class Item:
    # an Object that can be picked up and used
    def __init__(self, use_function=None):
        self.use_function = use_function

    def use(self, target):
        if self.use_function is None:
            return('The ' + self.owner.name.upper() + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)
