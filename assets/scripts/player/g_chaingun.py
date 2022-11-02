from random import randint
from assets.scripts.player.g_weapon import *

class ChainGun(Weapon):
    def __init__(self, game, path='assets/resources/textures/vmodels/chain/chain1.png', scale=5, animation_time=60):
        super().__init__(game, path, scale, animation_time)
        # we will do damage on the damage frame and the one after it.
        # this is intended for this weapon
        self.double_damage = True
        self.sound = ['gun/minigun.wav', 'gun/minigun2.wav', 'gun/minigun3.wav']
        self.damage = 21
        self.shooting_player_speed = PLAYER_FIRE_SPEED_CHAIN