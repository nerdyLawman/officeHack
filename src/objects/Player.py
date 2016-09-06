from libtcod import libtcodpy as libtcod
import gameconfig
from game import game_messages
from interface.menus import message, menu
from maps.helpers import is_blocked

# ---------------------------------------------------------------------
# [ PLAYER CLASS ] ----------------------------------------------------
# ---------------------------------------------------------------------
class Player:
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
                if hasattr(obj.ai, 'interact'): #if interactable
                    obj.ai.interact_function()
                    break

        #attack if target found, move otherwise
        if not is_blocked(self.owner.x+dx, self.owner.y+dy):
            self.owner.move(dx, dy)


    def check_level_up(self):
        level_up_xp = gameconfig.LEVEL_UP_BASE + self.level + gameconfig.LEVEL_UP_FACTOR
        if self.owner.fighter.xp >= level_up_xp:
            # level up
            self.level += 1
            self.owner.fighter.xp -= level_up_xp
            message(game_messages.PLAYER_LEVEL_UP + str(self.level) + '.', libtcod.yellow)

            choice = 'no selection'
            while choice == 'no selection':
                choice = menu('Level up! Chose a stat to raise!\n',
                    ['Constitution: +10 HP', 'Stregnth: +1 STR', 'Agility: +1 DEX'], 24)
            if choice == 0:
                self.owner.fighter.max_hp += 10
                self.owner.fighter.hp += 10
            elif choice == 1:
                self.owner.fighter.power += 1
            elif choice == 2:
                self.owner.fighter.defense += 1


# ---------------------------------------------------------------------
# [ PLAYER INVENTORY ] ------------------------------------------------
# ---------------------------------------------------------------------
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
            return(game_messages.DROPPED_MESSAGE + item.owner.name.upper() + '.')


    def identify_item_inventory(self, item, name):
        inv_item = self.get_inventory_item(item)
        if inv_item:
            identified_item = InventoryItem(name, item)
            self.inventory.append(identified_item)
            return identified_item


    def consume_item_inventory(self, item):
        inv_item = self.get_inventory_item(item)
        if inv_item:
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


# ---------------------------------------------------------------------
# [ PLAYER INVENTORY ITEM ] -------------------------------------------
# ---------------------------------------------------------------------
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
