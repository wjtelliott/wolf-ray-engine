from .g_sprite_object import *
from assets.scripts.npc.g_npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'assets/resources/textures/npc'
        self.static_sprite_path = 'assets/resources/textures/static/'
        self.anim_sprite_path = 'assets/resources/textures/anim/'
        self.vmodel_sprite_path = 'assets/resources/textures/vmodels'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # add_sprite(SpriteObject(game))
        # add_sprite(AnimatedSprite(game))

        add_npc(NPC(game))
        add_npc(NPC(game, path='assets/resources/textures/npc/ball/0.png', pos=(7.5, 7), scale=0.75, shift=0, animation_time=280))
        add_npc(NPC(game, path='assets/resources/textures/npc/ball/0.png', pos=(12.5, 7), scale=0.75, shift=0, animation_time=280))
        add_npc(NPC(game, path='assets/resources/textures/npc/ball/0.png', pos=(8.5, 7), scale=0.75, shift=0, animation_time=280))
        add_npc(NPC(game, path='assets/resources/textures/npc/ball/0.png', pos=(3.5, 7), scale=0.75, shift=0, animation_time=280))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)