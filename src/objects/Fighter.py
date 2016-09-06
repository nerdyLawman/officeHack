from libtcod import libtcodpy as libtcod
import gameconfig
from objects.death import npc_death, drone_death, player_death
from sound.SoundPlayer import SoundPlayer


# ---------------------------------------------------------------------
# [ FIGHTER CLASS ] ---------------------------------------------------
# ---------------------------------------------------------------------
class Fighter:
    # Object with combat-related properties and methods
    def __init__(self, hp, defense, power, xp,
        drone=False, codeword=None, gender='M', portrait='data/img/portrait2.png'):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
        self.drone = drone
        self.codeword = codeword
        self.gender = gender
        self.portrait = portrait


    def take_damage(self, damage):
        blip = SoundPlayer(gameconfig.SOUND_FX['attack'])
        blip.play()
        if damage > 0: self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            if self.owner.player == None: return npc_death(self.owner)
            else:
                if self.drone is True: drone_death(self.owner)
                else: player_death(self.owner)
        return None


    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp: self.hp = self.max_hp


    def attack(self, target):
        damage = self.power - target.fighter.defense
        if damage > 0:
            death_xp = target.fighter.take_damage(damage)
            if death_xp is not None:
                gameconfig.player.fighter.xp += death_xp
                gameconfig.player.player.check_level_up()
            return(self.owner.name.upper() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.', libtcod.orange)
        else:
            return(self.owner.name.upper() + ' attacks ' + target.name + ' but it has no effect!', libtcod.cyan)
