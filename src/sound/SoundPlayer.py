import threading
import pyglet
import threading

class DaemonStoppableThread(threading.Thread):

    def __init__(self, sleep_time, target=None,  **kwargs):
        super(DaemonStoppableThread, self).__init__(target=target, **kwargs)
        self.setDaemon(True)
        self.stop_event = threading.Event()
        self.sleep_time = sleep_time
        self.target = target

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.isSet()

    def run(self):
        while not self.stopped():
            if self.target:
                self.target()
            else:
                raise Exception('No target function given')
            self.stop_event.wait(self.sleep_time)

class SoundPlayer:
    def __init__(self, sound):
        self.sound_path = 'data/sound/' + sound + '.wav'
        self.player_thread = DaemonStoppableThread(10, target=self._create_thread)

    def play(self):
        global player_thread
        self.player_thread.start()

    def stop(self):
        self.player_thread.stop()

    def _create_thread(self) :
        music = pyglet.media.load(self.sound_path)
        music.play()
        pyglet.app.run()
