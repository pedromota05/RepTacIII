import pygame
import sys, os
from ..display import display
from .info import Info
from .grid import Grid
from ..entities.tiles import TileMap, Tile
from OpenGL.GL import *
from ..ui.background import Background
from ..ui.levels import Level1
from ..constants import TILE_MAP_LEVEL1, TILE_SIZE, WIDTH, HEIGHT
from .notify import Notify, Anchor, Select, Fill
from .pallet import Pallet
from .navigation import NavButtons

class Editor:
    def run(self):
            self.running = True 
            display.create_display()
            self.bg = Background("Black")

            # load tiles
            self.tile_map = TileMap()        
            self.tile_map.load_sprite_maps()
            self.level1 = Level1()
            if not self.level1.load(self.tile_map):
                self.level1.load(self.tile_map)
            
            self.grid = Grid(self.level1)
            self.pallet = Pallet(self.tile_map)
            self.info = Info(self.grid, self.pallet)
            self.nav = NavButtons(self.grid)

            #self.notify = Notify([self.grid, self.info])
            self.notify_anchor = Notify([self.grid, self.info], Anchor)
            self.notify_select = Notify([self.pallet], Select)
            self.notify_fill = Notify([self.grid], Fill)
            
            
            
            """O Game Loop Principal"""
            #try:           
            while self.running:
                dt = display.game_tick()   
                self.handle_events()
                self.update(dt)
                self.draw()
            '''except Exception as e:
                print(e)            # log here
                self.running = False
                pygame.quit()
                sys.exit()'''


    def handle_events(self):
        """Loop de Eventos: Inputs globais do sistema e interrupções"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            # mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    x = (x / display.size[0]) * WIDTH
                    y = (y / display.size[1]) * HEIGHT
                    if self.info.rect_save_btn.collidepoint(x, y):
                        self.grid.level.save()
                        
                    if self.pallet.rect.collidepoint(x,y):
                        for tile in self.pallet.tiles:
                            l = self.pallet.rect.left + tile.rect.left
                            t = self.pallet.rect.top + tile.rect.top                        
                            r = pygame.rect.Rect(l,t, tile.rect.w, tile.rect.h)
                            if r.collidepoint(x,y):
                                self.pallet.select = tile
                                self.notify_select.event()  
                                break  
                    
                    self.place_tile(x, y)

                elif event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    x = (x / display.size[0]) * WIDTH
                    y = (y / display.size[1]) * HEIGHT
                    self.remove_tile(x, y)

        #game_events()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_anchor(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move_anchor(1, 0)
        if keys[pygame.K_UP]:
            self.move_anchor(0, -1)
        if keys[pygame.K_DOWN]:
            self.move_anchor(0, 1)

        # mouse mantido pressionado
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            x,y = pygame.mouse.get_pos()
            x = (x / display.size[0]) * WIDTH
            y = (y / display.size[1]) * HEIGHT
            direction = self.nav.collide(x, y)
            if direction:
                self.move_anchor(*direction)
            else:
                if not self.info.rect_save_btn.collidepoint(x, y) and not self.pallet.rect.collidepoint(x, y):
                    self.place_tile(x, y)

        elif mouse_pressed[2]:
            x,y = pygame.mouse.get_pos()
            x = (x / display.size[0]) * WIDTH
            y = (y / display.size[1]) * HEIGHT
            self.remove_tile(x, y)


    def place_tile(self, x, y):
        if self.grid.rect.collidepoint(x, y) and self.pallet.select:
            for tile in self.grid.tiles:
                if tile.rect.collidepoint(x, y):
                    col, lin = tile.desc.split(",")
                    col, lin = int(col), int(lin)

                    map_col = col + self.grid.anchor[0]
                    map_lin = lin + self.grid.anchor[1]

                    selected = self.pallet.select
                    placed = Tile(selected.id, selected.image, selected.desc)
                    left = map_col * TILE_SIZE
                    top = map_lin * TILE_SIZE

                    placed.rect.topleft = (left, top)
                    
                    # Evita spam de eventos se o tile já é do mesmo tipo
                    current_tile = self.grid.level.tiles[map_lin][map_col]
                    if not current_tile or current_tile.id != placed.id:
                        self.grid.level.tiles[map_lin][map_col] = placed
                        self.notify_fill.event()
                    break

    def remove_tile(self, x, y):
        if self.grid.rect.collidepoint(x, y):
            for tile in self.grid.tiles:
                if tile.rect.collidepoint(x, y):
                    col, lin = tile.desc.split(",")
                    col, lin = int(col), int(lin)

                    map_col = col + self.grid.anchor[0]
                    map_lin = lin + self.grid.anchor[1]

                    if self.grid.level.tiles[map_lin][map_col] is not None:
                        self.grid.level.tiles[map_lin][map_col] = None
                        self.notify_fill.event()
                    break

    def move_anchor(self, dx:int, dy:int):
        """Move a âncora da grid respeitando os limites do mapa"""
        max_x = TILE_MAP_LEVEL1[0] - self.grid.x_tiles
        max_y = TILE_MAP_LEVEL1[1] - self.grid.y_tiles
        new_x = min(max(self.grid.anchor[0] + dx, 0), max_x)
        new_y = min(max(self.grid.anchor[1] + dy, 0), max_y)
        if [new_x, new_y] != self.grid.anchor:
            self.grid.anchor[0] = new_x
            self.grid.anchor[1] = new_y
            self.notify_anchor.event()
        

    def update(self, dt):
        """Loop de Atualização: Onde a lógica matemática acontece"""
        # new thread!                
        # check_collisions()
        #game.player.update(dt)
        self.info.update(dt, self.grid, self.pallet)
        self.grid.update(dt)
        self.pallet.update(dt)

            
    def draw(self):
        """Loop de Renderização: Onde desenhamos na tela"""                 
        # Render Phase
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # ordem importa - cada layer por vez - pode organizar
        self.bg.draw()
        self.info.draw()
        self.grid.draw()
        self.pallet.draw()
        self.nav.draw()
        
        pygame.display.flip()
        # forçar sincronização de hardware CPU e GPU - chamadas assincronas
        #glFinish()


editor = Editor()