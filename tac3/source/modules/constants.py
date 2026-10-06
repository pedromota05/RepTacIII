import pygame
import math

# Set up window size and title
# nHD - 1/9 of full HD - 360p (height) - pixel art
#WIDTH, HEIGHT = 640, 360    # constant for PC - scales x2, x3, etc. 16x9 ratio
SCALE = 1   # for pixel art
WIDTH, HEIGHT = 1920//SCALE, 1080//SCALE   # full HD - precisa usar dirty sprites - vetorial

TITLE = "Game TAC3"
FPS = 60

COLOR_TEXT = pygame.Color("#087204")
COLOR_BG = pygame.Color("#5C94FC")

GRAVITY = 1200
SIZE_PLAYER = (60//SCALE, 100//SCALE)

TILE_CROP = 16  # pixels
TILE_SIZE = 32  # pixels
TILE_MAP_LEVEL1 = (500,100)
TILE_MAP_LEVEL2 = (200,700)
#MAP_W = math.ceil(WIDTH / TILE_SIZE)
MAP_H = math.ceil(HEIGHT / TILE_SIZE)

FILE_LV1 = "source/data/lv1.npz"
FILE_LV1_JSON = 'source/data/level1.json'
FILE_MAP_1 = "assets/image/bg-1-1.png"
FILE_PLAYER_1 = "assets/image/player.png"
FILE_SPRITES_PLAYER = "assets/image/sprites3.png"



# editor
