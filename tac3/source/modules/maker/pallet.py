import pygame
from ..display import display
from ..constants import TILE_SIZE, WIDTH, HEIGHT
from ..utils import utils
from ..entities.tiles import TileMap, Tile
from .notify import Interested, Select, Anchor

class Pallet(Interested):
    def __init__(self, tilemap:TileMap): 
        super().__init__() 
        self.size = (WIDTH*0.1, HEIGHT*0.8)
        self.image = pygame.Surface(self.size).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect_orig = self.image.get_rect()
        
        self.anchor = [0,0] 
        self.tilemap = tilemap       
        self.tiles:list[Tile] = []
        self.select:Tile = None
                
        self.x_tiles = int(self.size[0]//TILE_SIZE)
        self.y_tiles = int(self.size[1]//TILE_SIZE)
                
        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)

        self.clear()
        self.update_tiles()
        self.rect.topleft = (WIDTH*0.9, HEIGHT*0.1)         
                


    def clear(self):
        self.image.fill("black")
        self.tiles.clear()
        for linha in range(self.y_tiles):
            pygame.draw.line(self.image, "white", (0,linha * TILE_SIZE), (self.size[0], linha * TILE_SIZE))
        for col in range(self.x_tiles):
            pygame.draw.line(self.image, "white", (col * TILE_SIZE, 0), (col * TILE_SIZE, self.size[1]))
        pygame.draw.rect(self.image, "blue", self.rect_orig, 5)

     
    def update(self, dt): 
        for event in self.events_get():
            if event == Anchor:
                self.clear()             
                self.update_tiles()
            if event == Select: 
                #print(event)               
                self.clear()             
                self.update_tiles()
                self.update_select()

               
    def update_select(self):       
        tile = self.select               
        if tile:   
            #print("select")          
            pygame.draw.rect(self.image, "gold", tile.rect, 3)        
        self.texture_id = utils.update_texture(self.texture_id, self.image)
              

    def update_tiles(self):
        i = 1
        for lin in range(self.y_tiles): 
            if i >= len(self.tilemap.codes): break                      
            for col in range(self.x_tiles):
                if i >= len(self.tilemap.codes): break
                tile = Tile(*self.tilemap.codes[i])               
                if tile: 
                    self.tiles.append(tile)                   
                    l = col*TILE_SIZE - (self.anchor[0]*TILE_SIZE)
                    t = lin*TILE_SIZE - (self.anchor[1]*TILE_SIZE)
                    tile.rect.topleft = (l, t)                    
                    self.image.blit(tile.image, tile.rect)
                i += 1
        self.texture_id = utils.update_texture(self.texture_id, self.image)
   

    def draw(self):
        x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, x,y,w,h) 
       

