import pygame
from graphics import *
from player import *


BACKGROUNDTILE = 128
TILETYPE = ['air', 'wall']


def create_test_map():
    rows = 15
    cols = 20
    row = 6
    # empty_sprite = pygame.sprite.Sprite(group)
    # empty_sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    # empty_sprite.rect = empty_sprite.image.get_rect()
    tiles = [[Tile() for _ in range(cols)] for k in range(rows)]
    background_tiles = [[0 for _ in range(cols)] for k in range(rows)]
    for col in range(cols):
        tiles[row][col] = Tile('wall', pygame.sprite.Sprite())
        tiles[row][col].sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    wall_image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    chain_tiles = cut_level(load_image('PrtCave.png'), 5, 16, [[2, 11], [2, 12], [2, 13]])
    tiles[5][4] = Tile('wall', pygame.sprite.Sprite())
    tiles[5][4].sprite.image = wall_image
    tiles[5][3] = Tile('wall', pygame.sprite.Sprite())
    tiles[5][3].sprite.image = wall_image
    tiles[4][3] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][3].sprite.image = wall_image
    tiles[4][2] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][2].sprite.image = wall_image
    tiles[4][5] = Tile('wall', pygame.sprite.Sprite())
    tiles[4][5].sprite.image = wall_image
    tiles[3][5] = Tile('wall', pygame.sprite.Sprite())
    tiles[3][5].sprite.image = wall_image
    tiles[3][9] = Tile('wall', pygame.sprite.Sprite())
    tiles[3][9].sprite.image = wall_image
    background_tiles[2][10] = pygame.sprite.Sprite()
    background_tiles[2][10].image = chain_tiles[0]
    for i in range(3, 5):
        background_tiles[i][10] = pygame.sprite.Sprite()
        background_tiles[i][10].image = chain_tiles[1]
    background_tiles[5][10] = pygame.sprite.Sprite()
    background_tiles[5][10].image = chain_tiles[2]

    return tiles, background_tiles


def load_first_cave():
    translator = {'1': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0],
                  'q': cut_level(load_image('PrtCave.png'), 5, 16, [[2, 0]])[0],
                  'w': cut_level(load_image('PrtCave.png'), 5, 16, [[2, 1]])[0],
                  'a': cut_level(load_image('PrtCave.png'), 5, 16, [[3, 0]])[0],
                  's': cut_level(load_image('PrtCave.png'), 5, 16, [[3, 1]])[0],
                  'e': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 2]])[0],
                  'r': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 3]])[0],
                  't': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 4]])[0],
                  'y': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 5]])[0],
                  'd': cut_level(load_image('PrtCave.png'), 5, 16, [[1, 2]])[0],
                  'f': cut_level(load_image('PrtCave.png'), 5, 16, [[1, 3]])[0],
                  'g': cut_level(load_image('PrtCave.png'), 5, 16, [[1, 4]])[0],
                  'h': cut_level(load_image('PrtCave.png'), 5, 16, [[1, 5]])[0],
                  'j': cut_level(load_image('PrtCave.png'), 5, 16, [[2, 3]])[0],
                  'k': cut_level(load_image('PrtCave.png'), 5, 16, [[2, 4]])[0],
                  'n': cut_level(load_image('PrtCave.png'), 5, 16, [[3, 3]])[0],
                  'm': cut_level(load_image('PrtCave.png'), 5, 16, [[3, 4]])[0],
                  'u': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 6]])[0],
                  'i': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 7]])[0],
                  'o': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 8]])[0],
                  'p': cut_level(load_image('PrtCave.png'), 5, 16, [[0, 9]])[0],
                  '[': cut_level(load_image('PrtCave.png'), 5, 16, [[1, 6]])[0],
                  ']': cut_level(load_image('PrtCave.png'), 5, 16, [[1, 7]])[0],
                  }
    with open('data/levels/first_cave.txt', encoding='utf-8') as file:
        file = file.readlines()
        level_map = file[:]
    level_map = [line.replace('\ufeff', '').replace('\n', '') for line in level_map]
    rows = len(level_map)
    cols = len(level_map[0])
    tiles = [[Tile() for _ in range(cols)] for k in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if not level_map[row][col] == '0':
                tiles[row][col].type = 'wall'
                tiles[row][col].sprite = pygame.sprite.Sprite()
                tiles[row][col].sprite.image = translator[level_map[row][col]]
    background_tiles = [[0 for _ in range(cols)] for k in range(rows)]
    return tiles, background_tiles


class Tile:
    def __init__(self, tile_type='air', sprite=0):
        if sprite == 0:
            self.sprite = cut_image_one(load_image('PrtCave.png'), (0, 0), (32, 32))  # TODO: fix default tile sprite
        self.type = tile_type
        self.sprite = sprite


class CollisionTile:
    def __init__(self, tile_type, row, col):
        self.type = tile_type
        self.row = row
        self.col = col


class Map:
    def __init__(self, tiles):
        self.backdrop_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
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

    def background(self, tiles):
        self.background_tiles = tiles
        self.background_exists = True
        for row in range(self.rows):
            for col in range(self.cols):
                if self.background_tiles[row][col] != 0:
                    self.background_tiles[row][col].rect = \
                        self.background_tiles[row][col].image.get_rect()
                    self.background_tiles[row][col].rect.x = col * TILESIZE
                    self.background_tiles[row][col].rect.y = row * TILESIZE
                    self.backdrop_group.add(self.background_tiles[row][col])


    def FixedBackdrop(self, image):
        self.backdrop_exists = True
        self.backdrop_image = image
        backdrop_rows = self.rows // 4 + 1
        backdrop_cold = self.cols // 4 + 1
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
        if self.background_exists:
            self.backdrop_group.update()
        self.foreground_group.update()

    def draw_background(self, screen):
        self.backdrop_group.draw(screen)
        self.background_group.draw(screen)

    def draw(self, screen):
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
