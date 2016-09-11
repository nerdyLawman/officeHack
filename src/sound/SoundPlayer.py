import gameconfig
from random import randint

class SoundPlayer:
    def __init__(self, sound_arg, **kwargs):
        if gameconfig.SOUND:
            from pygame import mixer
            self.mixer = mixer
            self.mixer.init()
            init_loop = kwargs.get('loop', False)
            if type(sound_arg) is dict:
                sound = sound_arg['name'] + str(randint(1, sound_arg['number']))
            else:
                sound = sound_arg
            if init_loop is not True:
                self.volume = gameconfig.VOLUME['SOUND_FX']
                self.loop = 0
            else:
                self.volume = gameconfig.VOLUME['MUSIC']
                self.loop = -1
                gameconfig.CURRENT_TRACK = self
            self.sound_path = 'data/sound/' + sound + '.wav'
            self.sound = self.mixer.Sound(self.sound_path)
            self.sound.set_volume(self.volume)
        else:
            # if sound is false use empty object as current track
            gameconfig.CURRENT_TRACK = self


    def play(self):
        if hasattr(self, 'sound'):
            self.sound.play(loops = self.loop)

    def stop(self):
        if hasattr(self, 'sound'):
            self.sound.stop()

    def fadeout(self, time):
        if hasattr(self, 'sound'):
            self.sound.fadeout(time)

    def switch_track(self, new_track):
        if hasattr(self, 'sound'):
            self.sound.fadeout(2000)
            self.sound_path = 'data/sound/' + new_track + '.wav'
            self.sound = self.mixer.Sound(self.sound_path)
            self.sound.set_volume(self.volume)
            self.play()
