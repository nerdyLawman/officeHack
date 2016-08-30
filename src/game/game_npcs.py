import libtcodpy as libtcod
import random

names = ['Seth', 'Peter', 'Ms. Suzy', 'Mary', 'Mark', 'Sophie', 'Alan',
        'Jeff', 'Martin', 'Mr. Frank', 'Donna', 'Deanie', 'Dr. Tod']

#fighter hp=6, defense=0, power=2, xp=10
npc_generic_1 = {
    'char' : 'D',
    'color' : libtcod.sky,
    'hp' : 6,
    'defense' : 0,
    'power' : 2,
    'xp' : 10,
    'chance' : 70,
}

npc_generic_2 = {
    'char' : 'E',
    'color' : libtcod.magenta,
    'hp' : 10,
    'defense' : 0,
    'power' : 3,
    'xp' : 15,
    'chance' : 25,
}

npc_generic_3 = {
    'char' : 'A',
    'color' : libtcod.lime,
    'hp' : 30,
    'defense' : 0,
    'power' : 6,
    'xp' : 45,
    'chance' : 5,
}

NPC_classes = [ npc_generic_1, npc_generic_2, npc_generic_3 ]

def get_npc():
    npc_class = random.choice(NPC_classes)
    npc_class['name'] = random.choice(names)
    return npc_class
