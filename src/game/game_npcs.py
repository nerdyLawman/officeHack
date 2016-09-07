from libtcod import libtcodpy as libtcod

male_names = ['Seth', 'Peter', 'Super Hans', 'Jeremy', 'Chad', 'Carl', 'Alan', 'Vincent', 'Darin', 'Art', 'Mr. Frank', 'Bumpus McNasty', 'Todd',]
female_names = ['Sophie', 'Suzie', 'Pam', 'Angela', 'Erin', 'Emily', 'Vicky', 'Marshawn', 'Veronica', 'Kim', 'Kathleen', 'Stephanie', 'Ms. Daphne']

npc_generic_1 = {
    'char' : 'D',
    'color' : libtcod.sky,
    'info' : 'Oh god, this person is so boring, what is there even to say about them? They do hate it when you throw COFFEE in their FACE!',
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
    'info' : 'This is the typer of person who really takes pride in what they\'re doing. It\'s enough to make you sick!',
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
    'info' : 'This person never SHUTS UP! If they get you in a corner they will TALK you HEAD OFF!',
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
    'info' : 'That\'s the BOSS. Best to avoid them and LOOK BUSY at all costs!',
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
    'color' : libtcod.dark_chartreuse,
    'info' : 'A computer TERMINAL where you can do all sorts of useful things like READ/WRITE DISCS, REMOTE LOOK at other STATIONS, and PILOT a DRONE!',
    'base_col' : libtcod.dark_chartreuse,
    'interact' : 'terminal',
    'special' : None,
    'wall' : True,
    'chance' : 80,
}

window = {
    'char' : 'H',
    'name' : 'window',
    'color' : libtcod.sky,
    'info' : 'I wonder what it FEELS like out THERE!',
    'base_col' : libtcod.lightest_cyan,
    'interact' : 'gaze',
    'special' : None,
    'wall' : True,
    'chance' : 30,
}

stationary_objects = [computer]
views = ['data/img/window1.png', 'data/img/window2.png', 'data/img/window3.png']
