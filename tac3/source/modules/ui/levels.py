#import pygame
import json
from ..constants import TILE_MAP_LEVEL1, TILE_SIZE, FILE_LV1, FILE_LV1_JSON
from ..utils import utils
import numpy as np
import scipy.sparse as sp
from ..entities.tiles import Tile, TileMap #tile_map


class Level():
    def __init__(self):
        pass


class Level1(Level):
    def __init__(self):
        super().__init__()

    def create_first_map(self):
        try:
            map1 = {            
                "height": TILE_MAP_LEVEL1[1],
                "width": TILE_MAP_LEVEL1[0],
                "tilewidth": TILE_SIZE,
                "tileheight": TILE_SIZE,  
                "layers": [
                    {                        
                        "map": FILE_LV1,
                        "height": TILE_MAP_LEVEL1[1],
                        "width": TILE_MAP_LEVEL1[0],
                        "name": "Blocks",
                        "opacity": 1,            
                        "visible": True,
                        "x": 0,
                        "y": 0
                    }
                ],  
                "orientation": "orthogonal",
                "renderorder": "right-down",  
                "type": "map",
                "version": "0.01"
            }
 
            resource = utils.get_full_path(FILE_LV1_JSON)            
            with open(resource, 'w', encoding='utf-8') as file:
                json.dump(map1, file, indent=4)

            self.create_matrix_tile()

        except Exception as e:
            # log
            print(e)


    def create_matrix_tile(self):
        # 1. Create a matrix with mostly zeros
        # (Using sparse array syntax - standard in SciPy)
        dense_matrix = np.zeros((TILE_MAP_LEVEL1[1], TILE_MAP_LEVEL1[0]), dtype=int)
        
                
        # add tiles - floor          
        for lin in range(TILE_MAP_LEVEL1[1]):
            for col in range(TILE_MAP_LEVEL1[0]):               
                # some few bricks and floor
                block_cond_1 = int(TILE_MAP_LEVEL1[0]*0.5) <= col <= int(TILE_MAP_LEVEL1[0]*0.6)
                block_cond_2 = lin == int(TILE_MAP_LEVEL1[1]*0.7)
                
                if lin > int(TILE_MAP_LEVEL1[1]*0.9):
                    dense_matrix[lin,col] = 1                                             
                elif block_cond_1 and block_cond_2:                        
                    dense_matrix[lin,col] = 3 

        dense_matrix[0,0] = 1
        dense_matrix[20,10] = 3
        # 2. Convert to a sparse representation (CSR format)
        sparse_matrix = sp.csr_array(dense_matrix)
        # 3. Save to a compressed .npz file
        sp.save_npz(FILE_LV1, sparse_matrix)
        #np.savetxt('matrix.csv', dense_matrix, delimiter=',')


    def save(self):
        dense_matrix = np.zeros((TILE_MAP_LEVEL1[1], TILE_MAP_LEVEL1[0]), dtype=int)
        for lin in range(TILE_MAP_LEVEL1[1]):
            for col in range(TILE_MAP_LEVEL1[0]):
                tile = self.tiles[lin][col]
                if tile is not None:
                    dense_matrix[lin,col] = tile.id
        sparse_matrix = sp.csr_array(dense_matrix)
        sp.save_npz(FILE_LV1, sparse_matrix)
        print("Level saved to file!")


    def load(self, tile_map):        
        # debug
        # self.create_first_map()

        #self.tiles:list[list[pygame.sprite.DirtySprite]] = []
        self.tiles:list[list[Tile]] = []
        try:
            resource = utils.get_full_path(FILE_LV1_JSON)            
            with open(resource, 'r', encoding='utf-8') as file:
                self.data = json.load(file)

            # 4. Load it back instantly
            dense_matrix = sp.load_npz(FILE_LV1)
            for lin in range(TILE_MAP_LEVEL1[1]):
                line = []           
                for col in range(TILE_MAP_LEVEL1[0]):                    
                    if dense_matrix[lin,col] != 0:
                        self.obj_call(dense_matrix, lin, col, line, tile_map)
                    else: line.append(None)  
                self.tiles.append(line)  

        except FileNotFoundError:
            print(f"Error: The file '{resource}' was not found.")
            # create first map
            self.create_first_map()
            return False
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON format.")
        return True


    def obj_call(self, dense_matrix, lin, col, line, tile_map:TileMap):
        for k, call in enumerate(tile_map.codes):
            if dense_matrix[lin,col] == k:
                id = call[0]
                surf = call[1]
                desc = call[2]
                obj:Tile = Tile(id, surf, desc)
                x, y = col, lin # 2d position
                obj.rect.topleft = (x*TILE_SIZE, y*TILE_SIZE)
                line.append(obj)


#level1 = Level1()
