import gameconfig
import libtcodpy as libtcod
from objects.classes import Object, Player, Fighter

def check_level_up():
    level_up_xp = LEVEL_UP_BASE + player.level + LEVEL_UP_FACTOR
    if player.fighter.xp >= level_up_xp:
        # level up
        player.level += 1
        player.fighter.xp -= level_up_xp
        message('Your skills increase. LEVEL UP! Now at level: ' + str(player.level) + '.', libtcod.yellow)

        choice = 'no selection'
        while choice == 'no selection':
            choice = menu('Level up! Chose a stat to raise!\n',
                ['Constitution: +10 HP', 'Stregnth: +1 STR', 'Agility: +1 DEX'], 24)
        if choice == 0:
            player.fighter.max_hp += 10
            player.fighter.hp += 10
        elif choice == 1:
            player.fighter.power += 1
        elif choice == 2:
            player.fighter.defense += 1
