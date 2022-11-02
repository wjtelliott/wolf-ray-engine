import pygame as pg
from assets.scripts.g_settings import G_SOUND_VOLUME

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'assets/resources/snd/'

    # todo: we need to cache these sounds and replay the sound object made from them
    # todo: instead of creating a new SOUND obj each time this method is called!!
    def play(self, sound_file):
        sound = pg.mixer.Sound(self.path + sound_file)
        sound.set_volume(G_SOUND_VOLUME)
        sound.play()