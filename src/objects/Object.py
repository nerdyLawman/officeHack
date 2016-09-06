import gameconfig
import math
from maps.helpers import is_blocked
from objects.Ai import RepulsedNPC

# ---------------------------------------------------------------------
# [ BASE OBJECT ] -----------------------------------------------------
# ---------------------------------------------------------------------
class Object:
    def __init__(self, x, y, char, name, color, info="Coming Soon",
        blocks=False, player=None, fighter=None, ai=None, item=None):
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
