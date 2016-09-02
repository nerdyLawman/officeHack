import libtcodpy as libtcod
from objects.actions import throw_coffee, read_write_file

floppy_disc =   { 'char' : '!',
    'name' : 'floppy disc',
    'color' : libtcod.light_lime,
    'special' : 'FooBar you F001!',
    'use' : read_write_file,
    'chance': 80,
}

paper_document = { 'char' : '#',
    'name' : 'document',
    'color' : libtcod.lightest_sepia,
    'special' : None,
    'use' : None,
    'chance' : 10,
}

coffee = { 'char' : '0',
    'name' : 'coffee',
    'color' : libtcod.dark_sepia,
    'special' : None,
    'use' : throw_coffee,
    'chance' : 10,
}

ITEMS = [ floppy_disc, paper_document, coffee ]
