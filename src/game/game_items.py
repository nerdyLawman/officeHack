from libtcod import libtcodpy as libtcod
from objects.actions import throw_coffee, read_document, floppy_overwrite

floppy_disc =   { 'char' : '!',
    'name' : 'floppy disc',
    'color' : libtcod.light_lime,
    'info' : 'A FLOPPY DISC which may have FILES already on it or can be USED to SAVE important INFORMATION!',
    'special' : 'FooBar you F001!',
    'use' : floppy_overwrite,
    'instant': False,
    'chance': 60,
}

paper_document = { 'char' : '#',
    'name' : 'document',
    'color' : libtcod.lightest_sepia,
    'info' : 'There are stacks of PAPER littered all over this OFFICE BUILDING!',
    'special' : 'I\'ve got a secret to share with you',
    'use' : read_document,
    'instant' : True,
    'chance' : 20,
}

coffee = { 'char' : '0',
    'name' : 'coffee',
    'color' : libtcod.dark_sepia,
    'info' : 'Ahhhh lovely, lovely COFFEE. Ouch! It\'s VERY HOT!',
    'special' : None,
    'use' : throw_coffee,
    'instant' : False,
    'chance' : 20,
}

ITEMS = [ floppy_disc, paper_document, coffee ]
