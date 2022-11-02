import pygame as pg
import sys
from assets.scripts.g_settings import *
from assets.scripts.episodes.g_shared import *
from assets.scripts.player.g_player import *
from assets.scripts.render.g_raycast import *
from assets.scripts.render.g_object_render import *
from assets.scripts.render.g_sprite_object import *
from assets.scripts.render.g_object_handler import *
from assets.scripts.player.g_pistol import *
from assets.scripts.player.g_submachine import *
from assets.scripts.player.g_chaingun import *
from assets.scripts.player.g_knife import *
from assets.scripts.snd.g_sound import *
from assets.scripts.npc.g_pathfinding import *

# we can use perf_counter and perf_counter_ns here
# to test some functions and find bottlenecks if needed
# from time import perf_counter

class Game:
    def __init__(self):

        # Start PYGAME, hide the mouse
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(G_RES)

        # Clock and global event trigger. Make sure we set the global event to False
        # at the end of each game tick. We only want functions to see the trigger once per update
        self.clock = pg.time.Clock()
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, GLOBAL_TRIGGER_TIME)

        # We can use our delta time here to make sure we can keep player
        # movement consistent thru game updates with varying FPS latency
        self.delta_time = 1


        # Start a new game
        self.new_game()

    def new_game(self):

        # Generate a new map. This is only initializing our g-shared test map for the time being
        self.map = Map(self)

        # Init player. init weapons is used to give the player all weapons for now
        self.player = Player(self)
        self.player.init_weapons()

        # rendering
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.sound = Sound(self)

        # pathing has to init after objects i think...
        self.pathfinding = PathFinding(self)

    def update(self):

        # todo: move player object and functions to the map object???
        self.player.update()

        # Cast rays before we try and render anything else
        self.raycasting.update()
        self.object_handler.update()
        pg.display.flip()

        pg.display.set_caption(f'FPS COUNTER : {self.clock.get_fps() :.1f}')
        #pg.display.set_caption(f'Game title here...')

        # Update clock delta and global trigger
        self.delta_time = self.clock.tick(G_FPS)     
        self.global_trigger = False

    def draw(self):
        # Render player last. vmodels will need to be drawn in front of scene
        self.object_renderer.draw()
        self.player.draw()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                self.player.single_fire_event(event)
            elif event.type == pg.KEYDOWN:
                self.player.change_weapon_event(event)
            elif event.type == self.global_event:
                self.global_trigger = True

    # main game loop
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
