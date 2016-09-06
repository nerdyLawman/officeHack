import pygame

class SoundPlayer:
    def __init__(self, sound, *loop):
        pygame.mixer.init()
        self.loop = 0
        self.sound_path = 'data/sound/' + sound + '.wav'
        self.sound = pygame.mixer.Sound(self.sound_path)

    def play(self):
        self.sound.play(loops = self.loop)

    def stop(self):
        self.sound.stop()
