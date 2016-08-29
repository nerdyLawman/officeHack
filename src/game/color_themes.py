import libtcodpy as libtcod

# THEMES
DEFAULT_THEME = { 'color_dark_wall' : libtcod.Color(0, 0, 100),
    'color_light_wall' : libtcod.Color(130, 110, 50),
    'color_dark_ground' : libtcod.Color(50, 50, 100),
    'color_light_ground' : libtcod.Color(200, 180, 50),
}

DARK_THEME = {'color_dark_wall' : libtcod.darker_gray,
    'color_light_wall' : libtcod.gray,
    'color_dark_ground' : libtcod.darkest_gray,
    'color_light_ground' : libtcod.dark_gray,
}

RED_THEME = {'color_dark_wall' : libtcod.darker_red,
    'color_light_wall' : libtcod.red,
    'color_dark_ground' : libtcod.darker_flame,
    'color_light_ground' : libtcod.flame,
}

BLUE_THEME = {'color_dark_wall' : libtcod.darker_azure,
    'color_light_wall' : libtcod.sky,
    'color_dark_ground' : libtcod.darker_han,
    'color_light_ground' : libtcod.azure,
}

COLOR_THEMES = [ DEFAULT_THEME, DARK_THEME, RED_THEME, BLUE_THEME ]
