import pygame
from ..constants import WIDTH, HEIGHT, COLOR_BG
from ..utils import utils
from ..entities.tiles import Tile

class Background():
    def __init__(self, color=COLOR_BG):
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(color) 
        
        self.rect = self.image.get_rect()

        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)        
        

    def add_cenario(self, tiles:list[list[Tile]]):
        for line in tiles:
            for tile in line:
                if tile: self.image.blit(tile.image, tile.rect)

        self.texture_id = utils.surface_to_texture(self.image)
        

    def draw(self):
        x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, x,y,w,h)
        
#bg = Background()