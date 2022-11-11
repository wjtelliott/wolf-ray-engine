import pygame as pg
from ..g_settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_texture = self.get_texture('assets/resources/textures/sky1.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('assets/resources/textures/pain.png', G_RES)
        self.game_over_screen = self.get_texture('assets/resources/textures/game_over.png', G_RES)
        self.digit_size = 90
        self.digit_size_offset = self.digit_size // 4
        self.digit_images = [self.get_texture(f'assets/resources/textures/font/{i}.png', [self.digit_size] * 2)
                            for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_player_ammo()

    def draw_player_health(self):

        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size + self.digit_size_offset, HEIGHT - self.digit_size - self.digit_size_offset))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size + self.digit_size_offset, HEIGHT - self.digit_size - self.digit_size_offset))

    def game_over(self):
        self.screen.blit(self.game_over_screen, (0, 0))

    def draw_player_ammo(self):
        ammo = str(self.game.player.ammo)
        for i, char in enumerate(ammo):
            self.screen.blit(self.digits[char], ((WIDTH + i * self.digit_size - self.digit_size_offset) - (self.digit_size * len(ammo)), HEIGHT - self.digit_size - self.digit_size_offset))

    def player_damage(self):
        if self.game.player.health > 0:
            self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 8.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_texture, (-self.sky_offset, 0))
        self.screen.blit(self.sky_texture, (-self.sky_offset + WIDTH, 0))
        self.screen.blit(self.sky_texture, (-self.sky_offset, HALF_HEIGHT))
        self.screen.blit(self.sky_texture, (-self.sky_offset + WIDTH, HALF_HEIGHT))
        pg.draw.rect(self.screen, (30, 30, 30), (0, HALF_HEIGHT + self.game.player.rel_y, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            ox, oy = pos
            oy += self.game.player.rel_y
            self.screen.blit(image, (ox, oy))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('assets/resources/textures/wall1.png'),
            2: self.get_texture('assets/resources/textures/wall2.png'),
            3: self.get_texture('assets/resources/textures/wall3.png'),
            4: self.get_texture('assets/resources/textures/wall4.png'),
            5: self.get_texture('assets/resources/textures/wall5.png'),
        }