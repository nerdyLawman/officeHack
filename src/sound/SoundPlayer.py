import pygame
import gameconfig
from random import randint

class SoundPlayer:
    def __init__(self, sound_arg, **kwargs):
        pygame.mixer.init()
        init_loop = kwargs.get('loop', False)
        if type(sound_arg) is dict:
            sound = sound_arg['name'] + str(randint(1, sound_arg['number']))
        else:
            sound = sound_arg
        if init_loop is not True:
            self.volume = gameconfig.VOLUME['SOUND_FX']
            self.loop = 0
        else:
            gameconfig.CURRENT_TRACK = self
            self.volume = gameconfig.VOLUME['MUSIC']
            self.loop = -1
        self.sound_path = 'data/sound/' + sound + '.wav'
        self.sound = pygame.mixer.Sound(self.sound_path)
        self.sound.set_volume(self.volume)

    def play(self):
        if gameconfig.SOUND is 'enabled':
            self.sound.play(loops = self.loop)

    def stop(self):
        if gameconfig.SOUND is 'enabled':
            self.sound.stop()

    def fadeout(self, time):
        if gameconfig.SOUND is 'enabled':
            self.sound.fadeout(time)

    def switch_track(self, new_track):
        if gameconfig.SOUND is 'enabled':
            self.sound.fadeout(2000)
            self.sound_path = 'data/sound/' + new_track + '.wav'
            self.sound = pygame.mixer.Sound(self.sound_path)
            self.play()
