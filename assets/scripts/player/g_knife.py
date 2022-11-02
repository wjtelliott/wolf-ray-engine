from assets.scripts.player.g_weapon import *

class Knife(Weapon):
    def __init__(self, game, path='assets/resources/textures/vmodels/knife/knife1.png', scale=5, animation_time=160):
        super().__init__(game, path, scale, animation_time)
        self.is_melee = True
        self.damage = 20