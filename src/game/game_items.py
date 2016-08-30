import libtcodpy as libtcod
from objects.actions import throw_coffee

floppy_disc =   { 'char' : '!',
    'name' : 'floppy disc',
    'color' : libtcod.light_lime,
    'use' : None,
    'chance': 10
}

paper_document = { 'char' : '#',
    'name' : 'document',
    'color' : libtcod.lightest_sepia,
    'use' : None,
    'chance' : 10
}

coffee = { 'char' : '0',
    'name' : 'coffee',
    'color' : libtcod.dark_sepia,
    'use' : throw_coffee,
    'chance' : 80
}

ITEMS = [ floppy_disc, paper_document, coffee ]
