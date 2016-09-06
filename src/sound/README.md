## SoundPlayer

####Dependencies
Currently, the soundplayer relies on the `pygame` library. To install on OSX Mavericks and above with Homebrew:
- `brew install sdl sdl_image sdl_mixer sdl_ttf portmidi`
- `pip install https://bitbucket.org/pygame/pygame/get/default.tar.gz`

####Using SoundPlayer
- All sound files live in `data/sound`.
- All sounds should be set in `gameconfig.py`. Check `BACKGROUND_MUSIC` and
`SOUND_FX`. To switch out sounds, replace the name of the track _minus_ the
file extension. All tracks should be in .wav format.
- Disable sound and control volume from the sound settings in `gameconfig`
- The SoundPlayer automatically sets `gameconfig.LIVE_TRACK` when the kwarg `loop=True` is passed in.
- Initializing a new sound effect (example): `SoundPlayer(gameconfig.SOUND_FX['dialogue'])`
- Changing the background music (example): `gameconfig.CURRENT_TRACK.switch_track(gameconfig.BACKGROUND_MUSIC['terminal'])`
