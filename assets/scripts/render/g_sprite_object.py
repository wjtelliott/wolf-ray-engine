import pygame as pg
from assets.scripts.g_settings import *
import os
from collections import deque

class SpriteObject:
    # todo: we need a default sprite here to draw rather than e1 or null
    def __init__(self, game, path='assets/resources/textures/e1.png', pos=(10.5, 3.5), scale=0.75, shift=-0.15, player = None):
        self.game = game

        # we will sometime explicitly pass the player object here. sloppy, but sometimes its not in game.player memory yet
        # IE, player weapon sprite
        self.player = player if player is not None else game.player


        self.x, self.y = pos
        self.path = path
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1

        # we can keep track of these half-widths and such instead of calculating them every time
        # every little bit of computation saving we can do, i'll take it!
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # We can smoothscale here, but we want the pixelated look
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + (self.game.raycasting.headbob_result / (SCREEN_DIST / 2) + height_shift)

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)

        # make sure object is in screen before trying to render
        if -self.IMAGE_WIDTH * 3 < self.screen_x < (WIDTH + self.IMAGE_WIDTH * 3) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    # todo: we need a default animated sprite here to draw instead of vmodel pistol or null
    def __init__(self, game, path='assets/resources/textures/vmodels/pistol/pistol1.png',
                pos=(1.5, 5), scale=1.0, shift=0.0, animation_time=60):
        super().__init__(game, path, pos, scale, shift)

        # lower the animation time, the faster they will play
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()

        # ? We might need to check if we are even drawing this entity to the screen before updating animations?
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
    

    
    """
        Right now we are grabbing images based on folder, sorted by file name

        example:
        anims
        \_ enemy
            \_ idle
                \_ 0.png
            \_ attack
                \_ 0.png
                \_ 1.png
        \_ weapon
            \_ pistol
                \_ 0.png
                \_ 1.png
                \_ 2.png
                etc....

        While this works very simply, we will eventually want to transition to a spritesheet method
    """
    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images