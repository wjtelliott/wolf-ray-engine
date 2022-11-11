import pygame as pg
import math
from ..g_settings import *
from assets.scripts.player.g_knife import *
from assets.scripts.player.g_pistol import *
from assets.scripts.player.g_submachine import *
from assets.scripts.player.g_chaingun import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.is_running = False
        self.shot = False
        self.currentWeapon = 0
        self.hasKnife = True
        self.hasPistol = True
        self.hasSub = True
        self.hasChain = True
        self.knife = None
        self.pistol = None
        self.sub = None
        self.chain = None
        self.health = PLAYER_MAX_HEALTH
        self.ammo = 50
        self.rel = MOUSE_MAX_REL
        self.rel_y = MOUSE_MAX_REL

        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

        self.weapon_sway = 0

    def update_weapon_sway(self):
        self.weapon_sway += 0.0065 * self.game.delta_time
        if self.weapon_sway >= 65535:
            self.weapon_sway = 0


    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
        return False

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def init_weapons(self):
        self.knife = Knife(self.game)
        self.pistol = Pistol(self.game)
        self.sub = SubMachinegun(self.game)
        self.chain = ChainGun(self.game)
        self.weapon = self.knife

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.ammo < 1 and not self.weapon.is_melee:
                    self.weapon.out_of_ammo()
                else:
                    self.weapon.mouse_down = True
                    self.weapon.shooting = True
            # if event.button == 1 and not self.shot and not self.game.weapon.shooting:
            #     self.shot = True
            #     self.game.weapon.shooting = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.weapon.mouse_down = False

    def get_damage(self, amount):
        self.health -= amount
        self.game.object_renderer.player_damage()
        self.check_game_over()
        # pain noise

    def try_change_weapon(self, weapon_index):
        allow_change = False
        match weapon_index:
            case 0:
                if self.hasKnife:
                    allow_change = True
            case 1:
                if self.hasPistol:
                    allow_change = True
            case 2:
                if self.hasSub:
                    allow_change = True
            case 3:
                if self.hasChain:
                    allow_change = True
        return allow_change

    def change_weapon_event(self, event):
        if event.unicode.isdigit():
            if int(event.unicode) > 0 and int(event.unicode) < 5 and int(event.unicode) - 1 != self.currentWeapon:
                if self.try_change_weapon(int(event.unicode) - 1):
                    self.currentWeapon = int(event.unicode) - 1
                    self.weapon.change_away()
                    self.change_weapon()
        else:
            if event.unicode == 'q' or event.unicode == 'e':
                direction = -1 if event.unicode == 'q' else 1
                counter = self.currentWeapon + direction
                while (counter >= 0 and counter <= 3):
                    if self.try_change_weapon(counter):
                        self.currentWeapon = counter
                        self.weapon.change_away()
                        self.change_weapon()
                        break
                    counter += direction
        
    def change_weapon(self):
        match self.currentWeapon:
            case 0:
                self.weapon = self.knife
            case 1:
                self.weapon = self.pistol
            case 2:
                self.weapon = self.sub
            case 3:
                self.weapon = self.chain
    
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = (PLAYER_SPEED if not self.weapon.shooting else self.weapon.shooting_player_speed) * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        self.is_running = +keys[pg.K_w] or +keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d]
        dx = ((speed_cos * +keys[pg.K_w]) + (-speed_cos * +keys[pg.K_s]) + (speed_sin * +keys[pg.K_a]) + (-speed_sin * +keys[pg.K_d]))
        dy = ((speed_sin * +keys[pg.K_w]) + (-speed_sin * +keys[pg.K_s]) + (-speed_cos * +keys[pg.K_a]) + (speed_cos * +keys[pg.K_d]))

        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < 20 or my > 200:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel, rel_y = pg.mouse.get_rel()
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))

        #self.rel_y = pg.mouse.get_rel()[1]
        self.rel_y += rel_y * MOUSE_SENSITIVITY * 500 * self.game.delta_time * -1
        self.rel_y = max(-MOUSE_MAX_REL_Y, min(MOUSE_MAX_REL_Y, self.rel_y))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #             (self.x * 100 + WIDTH * math.cos(self.angle),
        #             self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        # pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
        if self.weapon is not None:
            self.weapon.draw()

    def update(self):
        self.movement()
        self.mouse_control()
        if self.weapon is not None:
            self.weapon.update()
        self.recover_health()
        self.update_weapon_sway()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)