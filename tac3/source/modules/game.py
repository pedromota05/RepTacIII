import pygame
import sys
from .entities.player import Player
from .ui.background import Background
#from .display import display
from .entities.tiles import TileMap
from .ui.levels import Level1
from .ui.panel import Panel
from .config.sounds import sounds


class Game():
    def __init__(self):
        self.running = False

    def init_assets(self): 
        self.bg = Background()
        self.player = Player()
        self.panel = Panel()
        
        # load tiles
        self.tile_map = TileMap()        
        self.tile_map.load_sprite_maps()
        self.level1 = Level1()
        if not self.level1.load(self.tile_map):
            self.level1.load(self.tile_map)

        self.bg.add_cenario(self.level1.tiles)

              

    def start(self):
        self.running = True 
        sounds.play_music()


    def stop(self):
        self.running = False
        pygame.quit()
        sys.exit()



game = Game() 