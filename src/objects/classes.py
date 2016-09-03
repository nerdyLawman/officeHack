import libtcodpy as libtcod
import math
import gameconfig
from objects.actions import npc_death, player_death, drone_death
from interface.menus import conversation, terminal
from interface.rendering import send_to_back
from maps.helpers import is_blocked

class Object:
    # generic object
    def __init__(self, x, y, char, name, color, info="Coming Soon", blocks=False, player=None, fighter=None, ai=None, item=None):
      self.x = x
      self.y = y
      self.char = char
      self.name = name
      self.color = color
      self.info = info
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

    def move_away(self, target_x, target_y):
      dx = target_x - self.x
      dy = target_y - self.y
      distance = math.sqrt(dx ** 2 + dy ** 2)

      dx = int(round(dx / distance)) * -1
      dy = int(round(dx / distance)) * -1
      self.move(dx, dy)

    def distance_to(self, other):
      dx = other.x - self.x
      dy = other.y - self.y
      return math.sqrt(dx ** 2 + dy ** 2)

    def change_ai(self, new_ai):
        old_ai = self.ai
        if new_ai == 'repulsed':
            self.ai = RepulsedNPC(old_ai)
            self.ai.owner = self
        return 'Done'

class Player:
    # the player
    def __init__(self, inventory, level=1):
        self.inventory = inventory
        self.level = level

    def move_or_attack(self, dx, dy):
        #the coordinates the player is moving to/attacking
        x = self.owner.x + dx
        y = self.owner.y + dy

        #try to find an attackable object there
        target = None
        for obj in gameconfig.objects:
            if obj.x == x and obj.y == y:
                if obj.fighter:
                    self.owner.fighter.attack(obj)
                    break
                if hasattr(obj.ai, 'interact'): #if interactable
                    obj.ai.interact_function()
                    break

        #attack if target found, move otherwise
        if not is_blocked(self.owner.x+dx, self.owner.y+dy):
            self.owner.move(dx, dy)

    def add_item_inventory(self, item):
        inv_item = self.get_inventory_item(item)
        if inv_item is not None:
            inv_item.add_count()
        else:
            self.inventory.append(InventoryItem(item.owner.name, item))
        gameconfig.objects.remove(item.owner)
        gameconfig.item_count -= 1
        return("You PICKED UP a " + item.owner.name.upper() + ".")

    def drop_item_inventory(self, item, x, y):
        if self.consume_item_inventory(item):
            item.owner.x = x
            item.owner.y = y
            gameconfig.objects.append(item.owner)
            gameconfig.item_count += 1
            if gameconfig.item_count > gameconfig.level_item_count:
                gameconfig.level_item_count = gameconfig.item_count
            return("You DROPPED a " + item.owner.name.upper() + ".")

    def consume_item_inventory(self, item):
        inv_item = self.get_inventory_item(item)
        if inv_item is not None:
            if inv_item.count > 1:
                inv_item.subtract_count()
            else:
                self.inventory.remove(inv_item)
            return True
        return False

    def get_inventory_item(self, item):
        if len(self.inventory) > 0:
            for i in self.inventory:
                if i.inv_id == item.owner.name:
                    return i
        return None

class Fighter:
    # Object with combat-related properties and methods
    def __init__(self, hp, defense, power, xp, drone=False):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
        self.drone = drone

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
        if self.hp <= 0:
            if self.owner.player == None:
                # if you kill em, gain exp
                npc_death(self.owner)
                #player.fighter.xp += self.xp
                #check_level_up()
            else:
                if self.drone is True:
                    drone_death(self.owner)
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
    def __init__(self, recharge=gameconfig.TALK_RECHARGE):
        self.recharge = recharge

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
        if self.recharge < gameconfig.TALK_RECHARGE:
            self.recharge += 1
        elif libtcod.map_is_in_fov(gameconfig.fov_map, npc.x, npc.y):
            if npc.distance_to(gameconfig.player) >= gameconfig.TALK_RANGE:
                npc.move_towards(gameconfig.player.x, gameconfig.player.y)
            else:
                self.recharge = 0
                depth = libtcod.random_get_int(0, 1, 5)
                while depth > 0:
                    topic = topics[libtcod.random_get_int(0, 1, len(topics)-1)]
                    conversation(topic, self.owner.name)
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


class StationaryNPC:
    # stationary NPC
    def __init__(self, base_color, blink_color=libtcod.white, interact=None):
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
            terminal(self)
        else:
            return None

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

class Item:
    # an Object that can be picked up and used
    def __init__(self, special=None, use_function=None):
        self.special = special
        self.use_function = use_function

    def use(self):
        if self.use_function is None:
            return('The ' + self.owner.name.upper() + ' cannot be used.')
        else:
            if self.use_function(self) != 'cancelled':
                gameconfig.player.player.consume_item_inventory(self)

class InventoryItem:
    # an item listing that goes in the player's inventory
    def __init__(self, inv_id, item, count=1):
        self.inv_id = inv_id
        self.item = item
        self.count = count

    def add_count(self):
        if self.count < 10:
            self.count += 1

    def subtract_count(self):
        if self.count > 0:
            self.count -= 1
