import pygame
from ..display import display
from ..constants import SCALE
from ..utils import utils

class Panel():
    def __init__(self):  
        pygame.font.init()              
        self.delay:int = 1
        self.counter = self.delay       
        fps_text = f"FPS:{str(int(display.clock.get_fps()))}"   

        # Initialize a font (system default or custom font file)
        #self.font = pygame.font.SysFont("Arial", 14)
        self.font = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 200)        
        self.image = self.font.render(fps_text, True, pygame.Color("green")) 
        #self.image = pygame.transform.smoothscale_by(self.image, 1/(SCALE))
        self.rect = self.image.get_rect()

        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)
        
        #self.dirty = 1 # Draw once initially
        #self._layer = LAYER_PLAYER
        
    
    def update(self, dt):        
        self.counter += dt 
        if self.counter >= self.delay:                      
            # clock.get_fps() returns a float, so we convert it to an int, then a string
            fps = display.clock.get_fps()
            valor = int(min(fps,10000))
            fps_text = f"FPS:{valor}"
            # Render the text (Text, Anti-aliasing, Color)
            self.image = self.font.render(fps_text, True, pygame.Color("green"))
            self.image = pygame.transform.smoothscale_by(self.image, 1/(SCALE*4)) 
            self.rect = self.image.get_rect()    
            self.texture_id = utils.surface_to_texture(self.image)    
            self.counter = 0
            #self.dirty = 1


    def draw(self):
        x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, x,y,w,h) 
       

#panel = Panel()
