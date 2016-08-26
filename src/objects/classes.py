import libtcodpy as libtcod
import math
import gameconfig
#from map.helpers import is_blocked  can't do cos looped import

class Object:
    # generic object
    def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None, item=None):
      self.x = x
      self.y = y
      self.char = char
      self.name = name
      self.color = color
      self.blocks = blocks

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
        #if not is_blocked(self.x + dx, self.y + dy):
        if True:
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

    def send_to_back(self, objects):
        objects.remove(self)
        objects.insert(0, self)

class Item:
    # an Object that can be picked up and used
    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        #add to inv and remove from map
        if len(inventory) >= 26:
            return('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.pink)
        else:
            inventory.append(self.owner)
            objects.remove(self.owner)
            return('You picked up a ' + self.owner.name + '!', libtcod.green)

    def use(self):
        if self.use_function is None:
            return('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)

class Fighter:
    # Object with combat-related properties and methods
    def __init__(self, hp, defense, power, xp, death_function=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
        self.death_function = death_function

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
        if self.hp <= 0:
            # if you kill em, gain exp
            if self.owner.name != 'hero':
                #player.fighter.xp += self.xp
                #check_level_up()
                print('death')
            function = self.death_function
            if function is not None:
                function(self.owner)

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            return(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.', libtcod.orange)
        else:
            return(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!', libtcod.cyan)

class Player:
    # the player
    def __init__(self, inventory):
        self.inventory = inventory

    def add_item_inventory(self, item):
        self.inventory.append(item)

class BaseNPC:
    # basic NPC ai
    def take_turn(self, fov_map, player):
        npc = self.owner
        if libtcod.map_is_in_fov(fov_map, npc.x, npc.y):
            if npc.distance_to(player) >= 2:
                npc.move_towards(player.x, player.y)

            elif player.fighter.hp > 0:
                npc.fighter.attack(player)

class ConfusedNPC:
    def __init__(self, old_ai, num_turns=gameconfig.CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
        else:
            self.owner.ai = self.old_ai
            return('The ' + self.owner.name + ' is no longer confused.', libtcod.red)
