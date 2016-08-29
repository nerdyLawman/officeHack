import libtcodpy as libtcod

#fighter hp=6, defense=0, power=2, xp=10
jeff = { 'char' : 'D',
    'name' : 'Jeff',
    'color' : libtcod.sky,
    'hp' : 6,
    'defense' : 0,
    'power' : 2,
    'xp' : 10,
    'chance' : 70,
}

sophie = { 'char' : 'E',
    'name' : 'Sophie',
    'color' : libtcod.magenta,
    'hp' : 10,
    'defense' : 0,
    'power' : 3,
    'xp' : 15,
    'chance' : 25,
}

alan = { 'char' : 'A',
    'name' : 'Alan',
    'color' : libtcod.lime,
    'hp' : 30,
    'defense' : 0,
    'power' : 6,
    'xp' : 45,
    'chance' : 5,
}

NPCS = [ jeff, sophie, alan ]
