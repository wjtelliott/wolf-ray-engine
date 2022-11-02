from assets.scripts.player.g_weapon import *

class Pistol(Weapon):
    def __init__(self, game, path='assets/resources/textures/vmodels/pistol/pistol1.png', scale=5, animation_time=200):
        super().__init__(game, path, scale, animation_time)
        self.sound = ['gun/pistol.wav', 'gun/pistol2.wav', 'gun/pistol3.wav']
        self.damage = 32
        self.shooting_player_speed = PLAYER_FIRE_SPEED_PISTOL