from random import randint
from assets.scripts.g_settings import *
from assets.scripts.render.g_sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='assets/resources/textures/vmodels/pistol/pistol1.png', scale=5, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.scale(img, (self.image.get_width() * SCALE * 5, self.image.get_height() * SCALE * 5))
            for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.shooting = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50
        self.damage_frame = 2
        self.mouse_down = False
        self.double_damage = False
        self.sound = None
        self.is_melee = False

        self.shooting_player_speed = PLAYER_FIRE_SPEED

    def get_sound(self):
        if self.sound is None:
            return None
        if isinstance(self.sound, list):
            random_index = randint(0, len(self.sound) - 1)
            return self.sound[random_index]
        return self.sound

    def change_away(self):
        self.images.rotate(self.frame_counter - self.num_images)
        self.frame_counter = 0
        self.image = self.images[0]
        self.shooting = False
        self.mouse_down = False
        self.game.sound.play('gun/weapswitch.wav')

    def deal_damage(self, play_sound = True):
        # print(f'dealt damage on frame: {self.frame_counter}')
        self.game.player.shot = True
        if self.sound is not None and play_sound:
            self.game.sound.play(self.get_sound())

    def out_of_ammo(self):
        self.images.rotate(self.frame_counter - self.num_images)
        self.frame_counter = 0
        self.image = self.images[0]
        self.shooting = False
        # self.mouse_down = False
        self.game.sound.play('gun/outofammo.wav')

    def animate_shot(self):
        def move_frame(self, amount):
            self.images.rotate(-amount)
            self.image = self.images[0]
            self.frame_counter += amount
            if self.frame_counter >= self.num_images:
                self.shooting = False
                self.frame_counter = 0

        if self.shooting:
            # self.game.player.shot = False
            if self.animation_trigger:
                self.game.player.shot = False
                if self.game.player.ammo < 1 and not self.game.player.weapon.is_melee:
                    self.out_of_ammo()
                    return
                if self.frame_counter == self.damage_frame:
                    #deal damage
                    self.deal_damage()
                    if not self.game.player.weapon.is_melee:
                        self.game.player.ammo -= 1
                    move_frame(self, 1)
                elif self.frame_counter == self.damage_frame + 1:
                    # if mouse down, go back
                    if self.double_damage:
                        self.deal_damage(False)
                    if self.mouse_down:
                        move_frame(self, -2)
                    else:
                        move_frame(self, 1)
                else:
                    move_frame(self, 1)


    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
