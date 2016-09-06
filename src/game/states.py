from libtcod import libtcodpy as libtcod
import shelve
import gameconfig
from game import game_messages
from interface.rendering import render_all, clear_console, message
from game.controls import handle_keys
from maps.mapping import make_map
from objects.Player import Player
from objects.Fighter import Fighter
from objects.Object import Object
from sound.SoundPlayer import SoundPlayer


def new_game():
    # create the player and first level and add them to the game
    player_component = Player(inventory=[])

    fighter_component = Fighter(hp = gameconfig.START_HP,
        defense = gameconfig.START_DEFENSE,
        power = gameconfig.START_POWER,
        xp = 0)
    # create player
    gameconfig.player = Object(0, 0,
        char = gameconfig.HERO_CHAR,
        name = gameconfig.HERO_NAME,
        color = gameconfig.HERO_COLOR,
        blocks=True,
        player = player_component,
        fighter = fighter_component)

    make_map() # create level map

    # add first level to game_levels
    first_level = [gameconfig.objects,
        gameconfig.level_map,
        gameconfig.stairs_up,
        gameconfig.stairs_down,
        gameconfig.color_theme,
        gameconfig.fov_map]
    gameconfig.game_levels.append(first_level)

    # DEBUG ---------------------
    if gameconfig.DEBUG: print(player)

def save_game():
    # open new empty shelve - overwrites old
    file = shelve.open('savegame', 'n')
    file['map'] = gameconfig.level_map
    file['fov'] = gameconfig.fov_map
    file['objects'] = gameconfig.objects
    file['player'] = gameconfig.player
    file['game_msgs'] = gameconfig.game_msgs
    file['stairs_up'] = gameconfig.stairs_up
    file['stairs_down'] = gameconfig.stairs_down
    file['color_theme'] = gameconfig.color_theme
    file['game_level'] = gameconfig.game_level
    file['game_levels'] = gameconfig.game_levels
    file.close()

def load_game():
    # open previously saved shelve
    clear_console(gameconfig.con)
    file = shelve.open('savegame', 'r')
    gameconfig.level_map = file['map']
    gameconfig.fov_map = file['fov']
    gameconfig.objects = file['objects']
    gameconfig.player = file['player']
    gameconfig.game_msgs = file['game_msgs']
    gameconfig.stairs_up = file['stairs_up']
    gameconfig.stairs_down = file['stairs_down']
    gameconfig.color_theme = file['color_theme']
    gameconfig.game_level = file['game_level']
    gameconfig.game_levels = file['game_levels']
    file.close()

def play_game():
    # main game loop
    game_state = 'playing'
    player_action = None
    fov_recompute = True

    # bg music
    intro_song = SoundPlayer(gameconfig.BACKGROUND_MUSIC['level_1'], loop = True)
    intro_song.play()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,gameconfig.key,gameconfig.mouse)

        render_all(fov_recompute)
        player_action = handle_keys()

        # exit
        if player_action == 'exit':
            save_game()
            break

        # levels
        if player_action == 'stairs up': up_level()
        if player_action == 'stairs new': new_level()
        if player_action == 'stairs down': down_level()

        # playing
        if game_state == 'playing' and player_action != 'no turn':
            fov_recompute = True
            # move AI
            for obj in gameconfig.objects:
                if obj.ai: obj.ai.take_turn()

def up_level():
    # go up 1 game level
    gameconfig.game_level -= 1
    golevel = gameconfig.game_level - 1
    gameconfig.objects = gameconfig.game_levels[golevel][0]
    gameconfig.level_map = gameconfig.game_levels[golevel][1]
    gameconfig.stairs_up = gameconfig.game_levels[golevel][2]
    gameconfig.stairs_down = gameconfig.game_levels[golevel][3]
    gameconfig.color_theme = gameconfig.game_levels[golevel][4]
    gameconfig.fov_map = gameconfig.game_levels[golevel][5]
    # player position
    gameconfig.player.x = gameconfig.stairs_down.x
    gameconfig.player.y = gameconfig.stairs_down.y
    clear_console(gameconfig.con)

def down_level():
    # go down 1 game level
    gameconfig.game_level += 1
    golevel = gameconfig.game_level - 1
    gameconfig.objects = gameconfig.game_levels[golevel][0]
    gameconfig.level_map = gameconfig.game_levels[golevel][1]
    gameconfig.stairs_up = gameconfig.game_levels[golevel][2]
    gameconfig.stairs_down = gameconfig.game_levels[golevel][3]
    gameconfig.color_theme = gameconfig.game_levels[golevel][4]
    gameconfig.fov_map = gameconfig.game_levels[golevel][5]
    # player position
    gameconfig.player.x = gameconfig.stairs_up.x
    gameconfig.player.y = gameconfig.stairs_up.y
    clear_console(gameconfig.con)

def new_level():
    # go to new level
    message(gamemessages.LEVEL_REST_MESSAGE, gameconfig.GAME_UPDATE_COLOR)
    gameconfig.player.fighter.heal(gameconfig.player.fighter.max_hp / 2) # heal half HP
    message(gamemessages.LEVEL_CONTINUE_MESSAGE, gameconfig.CAUTION_COLOR)
    gameconfig.game_level += 1

    # create new level
    clear_console(gameconfig.con)
    make_map()
    new_level = [gameconfig.objects,
        gameconfig.level_map,
        gameconfig.stairs_up,
        gameconfig.stairs_down,
        gameconfig.color_theme,
        gameconfig.fov_map]
    gameconfig.game_levels.append(new_level)
