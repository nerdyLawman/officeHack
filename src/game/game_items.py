from libtcod import libtcodpy as libtcod
from objects.actions import throw_coffee, read_document, floppy_overwrite

floppy_disc =   { 'char' : '!',
    'name' : 'floppy disc',
    'color' : libtcod.light_lime,
    'special' : 'FooBar you F001!',
    'use' : floppy_overwrite,
    'instant': False,
    'chance': 60,
}

paper_document = { 'char' : '#',
    'name' : 'document',
    'color' : libtcod.lightest_sepia,
    'special' : 'I\'ve got a secret to share with you',
    'use' : read_document,
    'instant' : True,
    'chance' : 20,
}

coffee = { 'char' : '0',
    'name' : 'coffee',
    'color' : libtcod.dark_sepia,
    'special' : None,
    'use' : throw_coffee,
    'instant' : False,
    'chance' : 20,
}

ITEMS = [ floppy_disc, paper_document, coffee ]
