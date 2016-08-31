import libtcodpy as libtcod

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
    'ai' : 'base',
}

npc_talker = {
    'char' : 'E',
    'color' : libtcod.magenta,
    'hp' : 10,
    'defense' : 0,
    'power' : 3,
    'xp' : 15,
    'chance' : 25,
    'ai' : 'talk',
}

npc_boss = {
    'char' : 'A',
    'color' : libtcod.lime,
    'per_level' : 1,
    'hp' : 30,
    'defense' : 0,
    'power' : 6,
    'xp' : 45,
    'chance' : 5,
    'ai' : 'base',
}

NPC_classes = [ npc_generic_1, npc_talker, npc_boss ]


computer = {
    'char' : '#',
    'name' : 'computer',
    'color' : libtcod.dark_pink,
    'base_col' : libtcod.dark_pink,
    'interact' : 'terminal',
    'chance' : 10,
}

stationary_objects = [computer]
