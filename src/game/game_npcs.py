from libtcod import libtcodpy as libtcod

male_names = ['Seth', 'Peter', 'Super Hans', 'Jeremy', 'Chad', 'Carl', 'Alan', 'Vincent', 'Darin', 'Art', 'Mr. Frank', 'Bumpus McNasty', 'Todd',]
female_names = ['Sophie', 'Suzie', 'Pam', 'Angela', 'Erin', 'Emily', 'Vicky', 'Marshawn', 'Veronica', 'Kim', 'Kathleen', 'Stephanie', 'Ms. Daphne']

npc_generic_1 = {
    'char' : 'D',
    'color' : libtcod.sky,
    'hp' : 6,
    'defense' : 0,
    'power' : 2,
    'xp' : 10,
    'chance' : 60,
    'ai' : 'base',
}

npc_generic_2 = {
    'char' : 'F',
    'color' : libtcod.darker_sky,
    'hp' : 8,
    'defense' : 0,
    'power' : 3,
    'xp' : 12,
    'chance' : 10,
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

NPC_classes = [ npc_generic_1, npc_generic_2, npc_talker, npc_boss ]


computer = {
    'char' : '#',
    'name' : 'computer',
    'color' : libtcod.dark_pink,
    'base_col' : libtcod.dark_pink,
    'interact' : 'terminal',
    'special' : None,
    'chance' : 80,
}

window = {
    'char' : 'H',
    'name' : 'window',
    'color' : libtcod.sky,
    'base_col' : libtcod.sky,
    'interact' : 'gaze',
    'special' : 'data/img/bg.png',
    'chance' : 30,
}

stationary_objects = [computer, window]
