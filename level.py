import pygame
from graphics import *
from player import *

TILESIZE = 32
TILETYPE = ['air', 'wall']


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
    tiles[4][3] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][3].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
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
        self.foreground_group = pygame.sprite.Group()
        self.tiles = tiles
        self.rows = 15  # height / TILESIZE
        self.cols = 20  # width / TILESIZE
        for row in range(self.rows):
            for col in range(self.cols):
                if self.tiles[row][col].sprite != 0:
                    self.tiles[row][col].sprite.rect = \
                        self.tiles[row][col].sprite.image.get_rect()
                    self.tiles[row][col].sprite.rect.x = col * TILESIZE
                    self.tiles[row][col].sprite.rect.y = row * TILESIZE
                    self.foreground_group.add(self.tiles[row][col].sprite)

    def get_colliding_tiles(self, x, y, width, height):
        rectangle = Rectangle(x, y, width, height)
        first_row = rectangle.top / TILESIZE
        last_row = rectangle.bottom / TILESIZE
        first_col = rectangle.left / TILESIZE
        last_col = rectangle.right / TILESIZE
        collision_tiles = []
        for row in range(first_row, last_row + 1):  # TODO: check if we need there +1
            for col in range(first_col, last_col + 1):
                collision_tiles.append(CollisionTile(self.tiles[row][col].type, row, col))
        return collision_tiles

    def update(self):
        self.foreground_group.update()

    def draw(self, screen):
        self.foreground_group.draw(screen)



# class start_point(screen):
#     def __init__(self, screen, all_sprites):
#         running = True
#         pygame.mixer.music.load('data/music/gestation.mp3')
#         pygame.mixer.music.play(-1)
#
#         pygame.mixer.music.stop()
