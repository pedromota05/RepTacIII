import pygame
from .display import display
from .game import game
from .events.io import io_events
from .events.actions import game_events
from OpenGL.GL import *
from .config.sounds import sounds

class GameEngine:
    """A Engine Pura: Controla o ciclo de vida, janelas, eventos e loops."""
    def __init__(self):
        #pygame.init() # load all modules       
        #pygame.joystick.init()        
        
        display.create_display()   
        sounds.load_assets()
        game.init_assets()
        #menu.create()        
        #options.create()        

    def run(self):
        # main menu - editor or game         
        game.start()
        """O Game Loop Principal"""
        try:           
            while game.running:
                dt = display.game_tick()                
                self.handle_events()
                self.update(dt)
                self.draw()
        except Exception as e:
            print(e)            # log here
            game.stop()

    def handle_events(self):
        """Loop de Eventos: Inputs globais do sistema e interrupções"""
        io_events()
        game_events()

    def update(self, dt):
        """Loop de Atualização: Onde a lógica matemática acontece"""
        # new thread!                
        # check_collisions()
        game.player.update(dt)
        game.panel.update(dt)
            
    def draw(self):
        """Loop de Renderização: Onde desenhamos na tela"""                 
        # Render Phase
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # ordem importa - cada layer por vez - pode organizar
        game.bg.draw()
        game.panel.draw()
        game.player.draw()

        pygame.display.flip()
        # forçar sincronização de hardware CPU e GPU - chamadas assincronas
        #glFinish()
        
engine = GameEngine() # singleton 