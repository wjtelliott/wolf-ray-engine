from assets.scripts.player.g_weapon import *

class SubMachinegun(Weapon):
    def __init__(self, game, path='assets/resources/textures/vmodels/sub/sub1.png', scale=5, animation_time=60):
        super().__init__(game, path, scale, animation_time)
        self.sound = 'gun/rifle2.wav'
        self.damage = 16
        self.shooting_player_speed = PLAYER_FIRE_SPEED_SUB