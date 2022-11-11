import pygame as pg
import math
from ..g_settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.headbob = 0
        self.headbob_multitude = 9
        self.headbob_result = 0
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_draw(self):
        self.objects_to_render = []


        def colorize_wall(image, dist):

            return image

            # todo: this is obviously causing issues, we need a better fix!

            img = image.copy()

            # color (blend sub) our image, we must keep this value between 0-255
            color_amount = max(0, min(255, dist))
            img.fill((color_amount, color_amount, color_amount), None, pg.BLEND_RGB_SUB)
            return img

        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset, hb_result = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, (HALF_HEIGHT - proj_height // 2) + (hb_result / depth))
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, hb_result)

            # light the environment close to the player if the player is shooting
            ambient_darkness = 15
            player_shot_light_dist = 4

            if depth < player_shot_light_dist:
                # if the player is shooting, and it is not a melee weapon, reduce darkness effect
                if self.game.player.shot:
                    if not self.game.player.weapon.is_melee:
                        ambient_darkness = 9.5
                
            wall_column = colorize_wall(wall_column, depth * ambient_darkness)

            self.objects_to_render.append((depth, wall_column, wall_pos))
    
    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for _ in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # comment this out to get a camera fish-eye effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            
            # to avoid a /0 error, add a small magic number to our calc
            proj_height = SCREEN_DIST / (depth + 0.0001)


            # if we intend to add elevators or stairs, we can use this proj_look_height to address the player's Z coord later
            proj_look_height = 0

            self.headbob_result = math.sin(self.headbob) * self.headbob_multitude * +self.game.player.is_running

            self.ray_casting_result.append((depth, proj_height, texture, offset, self.headbob_result + proj_look_height))

            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            # pg.draw.rect(self.game.screen, color, 
            #             (ray * SCALE, (HALF_HEIGHT - proj_height // 2) + proj_look_height + (headbob_result * 3), SCALE, proj_height))
            
            ray_angle += DELTA_ANGLE

    #? This could probably be moved to the player file, and accessed from here
    def update_player_headbob(self):
        self.headbob += 0.01 * self.game.delta_time

        # in case the game is played a long time, we want to make sure that
        # we don't have overflow errors. after a long time we can just reset this
        if self.headbob >= 65535: self.headbob = 0

    def update(self):
        self.update_player_headbob()
        self.ray_cast()
        self.get_objects_to_draw()