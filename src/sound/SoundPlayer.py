import pygame
import gameconfig

class SoundPlayer:
    def __init__(self, sound, **kwargs):
        pygame.mixer.init()
        init_loop = kwargs.get('loop', False)
        if init_loop is not True:
            self.loop = 0
        else:
            gameconfig.CURRENT_TRACK = self
            self.loop = -1
        self.sound_path = 'data/sound/' + sound + '.wav'
        self.sound = pygame.mixer.Sound(self.sound_path)

    def play(self):
        self.sound.play(loops = self.loop)

    def stop(self):
        self.sound.stop()

    def fadeout(self, time):
        self.sound.fadeout(time)

    def switch_track(self, new_track):
        self.sound.fadeout(2000)
        self.sound_path = 'data/sound/' + new_track + '.wav'
        self.sound = pygame.mixer.Sound(self.sound_path)
        self.play()
