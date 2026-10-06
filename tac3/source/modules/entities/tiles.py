import pygame
from ..utils import utils
from ..constants import TILE_SIZE, TILE_CROP, FILE_MAP_1


class Tile():
    def __init__(self,
                 id:int, 
                 surf:pygame.Surface,
                 desc:str,
                 w=TILE_SIZE,
                 h=TILE_SIZE):
        
        self.id = id
        self.image = surf
        self.desc = desc

        if w != TILE_CROP or h != TILE_CROP:
            self.image = pygame.transform.smoothscale(self.image, (w,h))
        self.rect = self.image.get_rect()

        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)
       
    def draw(self):
            x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
            utils.draw_textured_quad(self.texture_id, x,y,w,h)


class TileMap():
    def load_sprite_maps(self):
        self.map_items = utils.load_image(FILE_MAP_1)

        # items
        self.floor1 = self.map_items.subsurface((0,208,TILE_CROP,TILE_CROP))
        self.floor2 = self.map_items.subsurface((768,448,TILE_CROP,TILE_CROP))
        self.brick1 = self.map_items.subsurface((320,144,TILE_CROP,TILE_CROP))
        self.brick2 = self.map_items.subsurface((832,400,TILE_CROP,TILE_CROP))

        # novos tiles adicionados (Questão B)
        self.floor3 = self.map_items.subsurface((16,208,TILE_CROP,TILE_CROP))
        self.brick3 = self.map_items.subsurface((336,144,TILE_CROP,TILE_CROP))
        self.block1 = self.map_items.subsurface((32,208,TILE_CROP,TILE_CROP))

        #pygame.image.save(self.floor1,"1.png")
      
        # object codes
        self.codes = [            
            None,   # code by index - 0 draw nothing
            (1, self.floor1, "floor1"),     # id, surface, description
            (2, self.floor2, "floor2"),
            (3, self.brick1, "brick1"),
            (4, self.brick2, "brick2"),
            (5, self.floor3, "floor3"),
            (6, self.brick3, "brick3"),
            (7, self.block1, "block1")
        ]

#tile_map = TileMap()