import pygame
from graphics import *
from player import *

BACKGROUNDTILE = 128
TILESIZE = 32
TILETYPE = ['air', 'wall']
WIDTH, HEIGHT = 640, 480


def create_test_map():
    rows = 15
    cols = 20
    row = 6
    # empty_sprite = pygame.sprite.Sprite(group)
    # empty_sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    # empty_sprite.rect = empty_sprite.image.get_rect()
    tiles = [[Tile() for _ in range(cols)] for k in range(rows)]
    for col in range(cols):
        tiles[row][col] = Tile('wall', pygame.sprite.Sprite())
        tiles[row][col].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[5][4] = Tile('wall', pygame.sprite.Sprite())
    tiles[5][4].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[5][3] = Tile('wall', pygame.sprite.Sprite())
    tiles[5][3].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[4][3] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][3].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[4][2] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][2].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[4][5] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][5].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[3][5] = Tile('wall', pygame.sprite.Sprite())
    tiles[3][5].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    tiles[3][9] = Tile('wall', pygame.sprite.Sprite())
    tiles[3][9].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    return tiles


class Tile:
    def __init__(self, tile_type='air', sprite=0):
        if sprite == 0:
            self.sprite = cut_image_one(load_image('PrtCave.png'), (0, 0), (32, 32))
        self.type = tile_type
        self.sprite = sprite


class CollisionTile:
    def __init__(self, tile_type, row, col):
        self.type = tile_type
        self.row = row
        self.col = col


class Map:
    def __init__(self, tiles):
        self.backdrop_exists = False
        self.foreground_group = pygame.sprite.Group()
        self.tiles = tiles
        self.rows = len(self.tiles)  # height / TILESIZE
        self.cols = len(self.tiles[0])  # width / TILESIZE
        for row in range(self.rows):
            for col in range(self.cols):
                if self.tiles[row][col].sprite != 0:
                    self.tiles[row][col].sprite.rect = \
                        self.tiles[row][col].sprite.image.get_rect()
                    self.tiles[row][col].sprite.rect.x = col * TILESIZE
                    self.tiles[row][col].sprite.rect.y = row * TILESIZE
                    self.foreground_group.add(self.tiles[row][col].sprite)

    def FixedBackdrop(self, image):
        self.backdrop_exists = True
        self.backdrop_image = image
        backdrop_rows = self.rows // 4 + 1
        backdrop_cold = self.cols // 4 + 1
        self.backdrop_group = pygame.sprite.Group()
        for row in range(backdrop_rows):
            for col in range(backdrop_cold):
                backdrop_tile = pygame.sprite.Sprite()
                backdrop_tile.image = self.backdrop_image
                backdrop_tile.rect = backdrop_tile.image.get_rect()
                backdrop_tile.rect.x = col * BACKGROUNDTILE
                backdrop_tile.rect.y = row * BACKGROUNDTILE
                self.backdrop_group.add(backdrop_tile)

    def get_colliding_tiles(self, rectangle):
        first_row = rectangle.top / TILESIZE
        last_row = rectangle.bottom / TILESIZE
        first_col = rectangle.left / TILESIZE
        last_col = rectangle.right / TILESIZE
        collision_tiles = []
        for row in range(int(first_row), int(last_row) + 1):  # TODO: check if we need there +1
            for col in range(int(first_col), int(last_col) + 1):
                try:  # all of maps need to be closed, character shouldn't fall outside of map
                    collision_tiles.append(CollisionTile(self.tiles[row][col].type, row, col))
                except IndexError as ie:
                    print(ie)
        return collision_tiles

    def update(self):
        if self.backdrop_exists:
            self.foreground_group.update()
        self.foreground_group.update()

    def draw(self, screen, drawbackground=False):
        if drawbackground:
            self.backdrop_group.draw(screen)
        else:
            self.foreground_group.draw(screen)

# class FixedBackdrop:
#     def __init__(self, image):
#         self.image = image
#         self.rows = 4  # ~~ HEIGHT / BACKGROUNDTILE
#         self.cols = WIDTH / BACKGROUNDTILE  # TODO: make dynamic rows and cols calculating in backdrop
#         self.backdropgroup = pygame.sprite.Group
#         for

# class start_point(screen):
#     def __init__(self, screen, all_sprites):
#         running = True
#         pygame.mixer.music.load('data/music/gestation.mp3')
#         pygame.mixer.music.play(-1)
#
#         pygame.mixer.music.stop()
